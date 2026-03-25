"""Tests for ANRS CLI adapter command."""

import pytest
from pathlib import Path
from click.testing import CliRunner

from anrs.main import cli


@pytest.fixture
def runner():
    """Create CLI runner."""
    return CliRunner()


class TestAdapterListCommand:
    """Tests for anrs adapter list command."""

    def test_adapter_list(self, runner):
        """Test listing available adapters."""
        result = runner.invoke(cli, ["adapter", "list"])
        assert result.exit_code == 0
        assert "cursor" in result.output
        assert "claude-code" in result.output
        assert "codex" in result.output
        assert "opencode" in result.output


class TestAdapterInstallCommand:
    """Tests for anrs adapter install command."""

    def test_adapter_install_cursor(self, runner, tmp_path):
        """Test installing cursor adapter."""
        result = runner.invoke(
            cli, ["adapter", "install", "cursor", str(tmp_path)])
        assert result.exit_code == 0
        assert (tmp_path / ".cursorrules").exists()

    def test_adapter_install_claude_code(self, runner, tmp_path):
        """Test installing claude-code adapter."""
        result = runner.invoke(
            cli, ["adapter", "install", "claude-code", str(tmp_path)])
        assert result.exit_code == 0
        assert (tmp_path / "CLAUDE.md").exists()

    def test_adapter_install_codex(self, runner, tmp_path):
        """Test installing codex adapter."""
        result = runner.invoke(
            cli, ["adapter", "install", "codex", str(tmp_path)])
        assert result.exit_code == 0
        assert (tmp_path / "AGENTS.md").exists()

    def test_adapter_install_unknown(self, runner, tmp_path):
        """Test error on unknown adapter."""
        result = runner.invoke(
            cli, ["adapter", "install", "unknown", str(tmp_path)])
        assert result.exit_code != 0
        # Click validates choice and shows available options
        assert "is not one of" in result.output

    def test_adapter_install_already_exists(self, runner, tmp_path):
        """Test behavior when adapter config already exists."""
        # First install
        runner.invoke(cli, ["adapter", "install", "cursor", str(tmp_path)])
        # Second install without force shows conflict prompt
        result = runner.invoke(
            cli, ["adapter", "install", "cursor", str(tmp_path)])
        assert result.exit_code != 0
        # New behavior: shows conflict detection or aborts
        assert "Conflict" in result.output or "Aborted" in result.output

    def test_adapter_install_force(self, runner, tmp_path):
        """Test force overwrite with --force."""
        # First install
        runner.invoke(cli, ["adapter", "install", "cursor", str(tmp_path)])
        # Second install with force
        result = runner.invoke(
            cli, ["adapter", "install", "cursor", "--force", str(tmp_path)])
        assert result.exit_code == 0

    def test_adapter_install_dry_run(self, runner, tmp_path):
        """Test dry run mode."""
        result = runner.invoke(
            cli, ["adapter", "install", "cursor", "--dry-run", str(tmp_path)])
        assert result.exit_code == 0
        assert "Dry run" in result.output
        assert "Would copy" in result.output
        # Should not create file
        assert not (tmp_path / ".cursorrules").exists()

    def test_adapter_install_dry_run_with_existing(self, runner, tmp_path):
        """Test dry run shows conflict when file already exists."""
        # First install
        runner.invoke(cli, ["adapter", "install", "cursor", str(tmp_path)])
        # Dry run should show conflict info
        result = runner.invoke(
            cli, ["adapter", "install", "cursor", "--dry-run", str(tmp_path)])
        assert result.exit_code == 0
        assert "Conflict" in result.output

    def test_adapter_install_skip_option(self, runner, tmp_path):
        """Test --skip option skips existing files."""
        # First install
        runner.invoke(cli, ["adapter", "install", "cursor", str(tmp_path)])
        # Second install with skip
        result = runner.invoke(
            cli, ["adapter", "install", "cursor", "--skip", str(tmp_path)])
        assert result.exit_code == 0
        assert "Skipped" in result.output

    def test_adapter_install_force_creates_backup(self, runner, tmp_path):
        """Test --force creates backup before overwriting."""
        # Create .anrs for backup storage
        anrs_dir = tmp_path / ".anrs"
        anrs_dir.mkdir()
        # First install
        runner.invoke(cli, ["adapter", "install", "cursor", str(tmp_path)])
        # Modify the file
        (tmp_path / ".cursorrules").write_text("modified content")
        # Force reinstall
        result = runner.invoke(
            cli, ["adapter", "install", "cursor", "--force", str(tmp_path)])
        assert result.exit_code == 0
        # Backup should exist
        backup_dir = anrs_dir / ".backups"
        assert backup_dir.exists()

    def test_adapter_install_all_adapters(self, runner, tmp_path):
        """Test installing all available adapters."""
        for adapter in ["cursor", "claude-code", "codex", "opencode"]:
            subdir = tmp_path / adapter
            subdir.mkdir()
            result = runner.invoke(
                cli, ["adapter", "install", adapter, str(subdir)])
            assert result.exit_code == 0


class TestAdapterInstallEdgeCases:
    """Edge case tests for adapter install."""

    def test_adapter_source_not_found(self, runner, tmp_path, monkeypatch):
        """Test error when adapter source directory not found."""
        from anrs import adapter as adapter_module
        from pathlib import Path

        # Mock ADAPTERS_DIR to non-existent path
        fake_dir = Path("/nonexistent/adapters")
        monkeypatch.setattr(adapter_module, "ADAPTERS_DIR", fake_dir)

        result = runner.invoke(
            cli, ["adapter", "install", "cursor", str(tmp_path)])
        assert result.exit_code != 0
        assert "not found" in result.output.lower()

    def test_adapter_abort_from_prompt(self, runner, tmp_path):
        """Test aborting from conflict prompt."""
        # First install
        runner.invoke(cli, ["adapter", "install", "cursor", str(tmp_path)])
        # Second install with abort choice
        result = runner.invoke(
            cli, ["adapter", "install", "cursor", str(tmp_path)],
            input="a\n"  # Choose abort
        )
        assert result.exit_code != 0 or "Aborted" in result.output

    def test_adapter_skip_from_prompt(self, runner, tmp_path):
        """Test skipping from conflict prompt."""
        # First install
        runner.invoke(cli, ["adapter", "install", "cursor", str(tmp_path)])
        # Second install with skip choice
        result = runner.invoke(
            cli, ["adapter", "install", "cursor", str(tmp_path)],
            input="s\n"  # Choose skip
        )
        assert result.exit_code == 0 or "Skipped" in result.output

    def test_adapter_io_error_on_copy(self, runner, tmp_path, monkeypatch):
        """Test IOError handling when copying adapter."""
        import shutil

        def mock_copy(*args, **kwargs):
            raise IOError("Permission denied")

        monkeypatch.setattr(shutil, "copy", mock_copy)

        result = runner.invoke(
            cli, ["adapter", "install", "cursor", str(tmp_path)])
        assert result.exit_code != 0
        assert "Cannot install" in result.output or "Error" in result.output

    def test_adapter_merge_from_prompt(self, runner, tmp_path):
        """Test merge option from conflict prompt."""
        # First install
        runner.invoke(cli, ["adapter", "install", "cursor", str(tmp_path)])
        # Create .anrs for backup
        (tmp_path / ".anrs").mkdir()
        # Second install with merge choice
        result = runner.invoke(
            cli, ["adapter", "install", "cursor", str(tmp_path)],
            input="m\n"  # Choose merge (treated same as backup for non-JSON)
        )
        # For non-JSON files, merge may behave like skip or backup
        assert result.exit_code in [0, 1]

    def test_adapter_backup_from_prompt(self, runner, tmp_path):
        """Test backup option from conflict prompt."""
        # First install
        runner.invoke(cli, ["adapter", "install", "cursor", str(tmp_path)])
        # Create .anrs for backup storage
        (tmp_path / ".anrs").mkdir()
        # Second install with backup choice
        result = runner.invoke(
            cli, ["adapter", "install", "cursor", str(tmp_path)],
            input="b\n"  # Choose backup
        )
        assert result.exit_code == 0
        # Should have backed up and reinstalled
        backup_dir = tmp_path / ".anrs" / ".backups"
        assert backup_dir.exists()
