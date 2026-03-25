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
        result = runner.invoke(cli, ["adapter", "install", "cursor", str(tmp_path)])
        assert result.exit_code == 0
        assert (tmp_path / ".cursorrules").exists()
    
    def test_adapter_install_claude_code(self, runner, tmp_path):
        """Test installing claude-code adapter."""
        result = runner.invoke(cli, ["adapter", "install", "claude-code", str(tmp_path)])
        assert result.exit_code == 0
        assert (tmp_path / "CLAUDE.md").exists()
    
    def test_adapter_install_codex(self, runner, tmp_path):
        """Test installing codex adapter."""
        result = runner.invoke(cli, ["adapter", "install", "codex", str(tmp_path)])
        assert result.exit_code == 0
        assert (tmp_path / "AGENTS.md").exists()
    
    def test_adapter_install_unknown(self, runner, tmp_path):
        """Test error on unknown adapter."""
        result = runner.invoke(cli, ["adapter", "install", "unknown", str(tmp_path)])
        assert result.exit_code != 0
        assert "Unknown adapter" in result.output
    
    def test_adapter_install_already_exists(self, runner, tmp_path):
        """Test error when adapter config already exists."""
        # First install
        runner.invoke(cli, ["adapter", "install", "cursor", str(tmp_path)])
        # Second install should fail
        result = runner.invoke(cli, ["adapter", "install", "cursor", str(tmp_path)])
        assert result.exit_code != 0
        assert "already exists" in result.output
    
    def test_adapter_install_force(self, runner, tmp_path):
        """Test force overwrite with --force."""
        # First install
        runner.invoke(cli, ["adapter", "install", "cursor", str(tmp_path)])
        # Second install with force
        result = runner.invoke(cli, ["adapter", "install", "cursor", "--force", str(tmp_path)])
        assert result.exit_code == 0
