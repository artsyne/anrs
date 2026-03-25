"""Tests for ANRS CLI init command."""

import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from click import ClickException

from anrs.main import cli
from anrs.init_cmd import (
    get_manifest,
    resolve_manifest,
    init_state_transform,
    init_config_transform,
    install_adapter,
    copy_template_file,
    detect_conflicts,
    install_file_with_strategy,
)
from anrs.backup import ConflictStrategy


@pytest.fixture
def runner():
    """Create CLI runner."""
    return CliRunner()


@pytest.fixture
def temp_dir(tmp_path):
    """Create a temporary directory for testing."""
    return tmp_path


class TestGetManifest:
    """Tests for get_manifest function."""

    def test_get_minimal_manifest(self):
        """Test loading minimal manifest."""
        manifest = get_manifest("minimal")
        assert manifest["name"] == "minimal"
        assert manifest["level"] == 0
        assert "files" in manifest
        assert "directories" in manifest

    def test_get_standard_manifest(self):
        """Test loading standard manifest."""
        manifest = get_manifest("standard")
        assert manifest["name"] == "standard"
        assert manifest["level"] == 1
        assert manifest["extends"] == "minimal"

    def test_get_full_manifest(self):
        """Test loading full manifest."""
        manifest = get_manifest("full")
        assert manifest["name"] == "full"
        assert manifest["level"] == 2
        assert manifest["extends"] == "standard"

    def test_get_unknown_manifest(self):
        """Test error on unknown manifest."""
        from click import ClickException
        with pytest.raises(ClickException):
            get_manifest("unknown")

    def test_get_manifest_json_error(self, temp_dir, monkeypatch):
        """Test handling of corrupted manifest JSON."""
        from anrs import init_cmd
        # Create a corrupted manifest
        corrupted = temp_dir / "manifests"
        corrupted.mkdir()
        (corrupted / "broken.json").write_text("{invalid json}")
        monkeypatch.setattr(init_cmd, "TEMPLATES_DIR", temp_dir)

        with pytest.raises(ClickException) as exc:
            get_manifest("broken")
        assert "Corrupted" in str(exc.value)


class TestResolveManifest:
    """Tests for resolve_manifest function."""

    def test_resolve_minimal(self):
        """Test resolving minimal manifest (no inheritance)."""
        manifest = resolve_manifest("minimal")
        assert len(manifest["files"]) == 3  # ENTRY, state, config
        assert ".anrs" in manifest["directories"]

    def test_resolve_standard(self):
        """Test resolving standard manifest (extends minimal)."""
        manifest = resolve_manifest("standard")
        # Should have minimal files + standard files
        assert len(manifest["files"]) > 3
        # Should have minimal dirs + standard dirs
        assert ".anrs/plans/active" in manifest["directories"]

    def test_resolve_full(self):
        """Test resolving full manifest (extends standard)."""
        manifest = resolve_manifest("full")
        # Should have all files from minimal + standard + full
        assert len(manifest["files"]) >= 6
        # Should have harness directory (inside .anrs/)
        assert ".anrs/harness" in manifest["directories"]


class TestTransforms:
    """Tests for template transform functions."""

    def test_init_state_transform(self):
        """Test state template transformation."""
        template = '{"metadata": {"created_at": "", "updated_at": ""}}'
        result = init_state_transform(template, "test-project")
        data = json.loads(result)
        assert data["metadata"]["created_at"] != ""
        assert data["metadata"]["updated_at"] != ""

    def test_init_config_transform(self):
        """Test config template transformation."""
        template = '{"project": {"name": "", "description": ""}}'
        result = init_config_transform(template, "test-project")
        data = json.loads(result)
        assert data["project"]["name"] == "test-project"


class TestInitCommand:
    """Tests for anrs init command."""

    def test_init_minimal(self, runner, temp_dir):
        """Test initializing with minimal level."""
        result = runner.invoke(
            cli, ["init", "--level", "minimal", str(temp_dir)])
        assert result.exit_code == 0
        assert (temp_dir / ".anrs").exists()
        assert (temp_dir / ".anrs" / "ENTRY.md").exists()
        assert (temp_dir / ".anrs" / "state.json").exists()
        assert (temp_dir / ".anrs" / "config.json").exists()

    def test_init_standard(self, runner, temp_dir):
        """Test initializing with standard level (default)."""
        result = runner.invoke(cli, ["init", str(temp_dir)])
        assert result.exit_code == 0
        assert (temp_dir / ".anrs").exists()
        assert (temp_dir / ".anrs" / "plans" / "active").exists()
        assert (temp_dir / ".anrs" / "plans" / "backlog").exists()

    def test_init_full(self, runner, temp_dir):
        """Test initializing with full level."""
        result = runner.invoke(cli, ["init", "--level", "full", str(temp_dir)])
        assert result.exit_code == 0
        assert (temp_dir / ".anrs" / "skills").exists()
        assert (temp_dir / ".anrs" / "failure-cases").exists()
        assert (temp_dir / ".anrs" / "harness").exists()  # harness inside .anrs/

    def test_init_already_exists(self, runner, temp_dir):
        """Test error when .anrs already exists without --force or --merge."""
        # First init
        runner.invoke(cli, ["init", str(temp_dir)])
        # Second init without force should prompt for conflict resolution
        # When no input provided, it aborts
        result = runner.invoke(cli, ["init", str(temp_dir)])
        assert result.exit_code != 0
        # New behavior: shows conflict detection table
        assert "Existing Files Detected" in result.output or "Aborted" in result.output

    def test_init_force(self, runner, temp_dir):
        """Test force overwrite with --force."""
        # First init
        runner.invoke(cli, ["init", str(temp_dir)])
        # Second init with force (provide 'y' for confirmation)
        result = runner.invoke(
            cli, ["init", "--force", str(temp_dir)], input="y\n")
        assert result.exit_code == 0

    def test_init_dry_run(self, runner, temp_dir):
        """Test dry run mode."""
        result = runner.invoke(cli, ["init", "--dry-run", str(temp_dir)])
        assert result.exit_code == 0
        assert "Dry run" in result.output
        # Should not create files
        assert not (temp_dir / ".anrs").exists()

    def test_init_state_json_content(self, runner, temp_dir):
        """Test that state.json is properly initialized."""
        runner.invoke(cli, ["init", str(temp_dir)])
        state_path = temp_dir / ".anrs" / "state.json"
        with open(state_path) as f:
            state = json.load(f)
        assert state["status"] == "idle"
        assert state["current_task"] is None
        assert "created_at" in state["metadata"]

    def test_init_config_json_content(self, runner, temp_dir):
        """Test that config.json is properly initialized."""
        runner.invoke(cli, ["init", str(temp_dir)])
        config_path = temp_dir / ".anrs" / "config.json"
        with open(config_path) as f:
            config = json.load(f)
        assert config["project"]["name"] == temp_dir.name

    def test_init_with_adapter(self, runner, temp_dir):
        """Test init with adapter."""
        result = runner.invoke(
            cli, ["init", "--adapter", "cursor", str(temp_dir)])
        assert result.exit_code == 0
        assert (temp_dir / ".cursorrules").exists()

    def test_init_merge_option(self, runner, temp_dir):
        """Test init with --merge option preserves user data."""
        # First init
        runner.invoke(cli, ["init", str(temp_dir)])
        # Modify state
        state_path = temp_dir / ".anrs" / "state.json"
        state = json.loads(state_path.read_text())
        state["status"] = "active"
        state_path.write_text(json.dumps(state))
        # Re-init with merge
        result = runner.invoke(
            cli, ["init", "--merge", str(temp_dir)])
        assert result.exit_code == 0
        # User data should be preserved
        new_state = json.loads(state_path.read_text())
        assert new_state["status"] == "active"

    def test_init_dry_run_with_conflicts(self, runner, temp_dir):
        """Test dry run shows conflicts."""
        # First init
        runner.invoke(cli, ["init", str(temp_dir)])
        # Dry run should show conflicts
        result = runner.invoke(cli, ["init", "--dry-run", str(temp_dir)])
        assert result.exit_code == 0
        assert "Conflicts detected" in result.output or "!" in result.output

    def test_init_dry_run_with_adapter(self, runner, temp_dir):
        """Test dry run shows adapter files."""
        result = runner.invoke(
            cli, ["init", "--dry-run", "--adapter", "cursor", str(temp_dir)])
        assert result.exit_code == 0
        assert ".cursorrules" in result.output or "cursor" in result.output


class TestInstallAdapter:
    """Tests for install_adapter function."""

    def test_install_adapter_unknown(self, temp_dir):
        """Test error on unknown adapter."""
        with pytest.raises(ClickException) as exc:
            install_adapter("nonexistent", temp_dir)
        assert "Unknown adapter" in str(exc.value)

    def test_install_adapter_dry_run(self, temp_dir, capsys):
        """Test dry run mode."""
        install_adapter("cursor", temp_dir, dry_run=True)
        # Should not create file
        assert not (temp_dir / ".cursorrules").exists()

    def test_install_adapter_success(self, temp_dir):
        """Test successful adapter installation."""
        install_adapter("cursor", temp_dir)
        assert (temp_dir / ".cursorrules").exists()

    def test_install_adapter_missing_directory(self, temp_dir, monkeypatch):
        """Test error when adapter directory doesn't exist."""
        from anrs import init_cmd
        # Point to non-existent adapters directory
        fake_dir = temp_dir / "fake_adapters"
        monkeypatch.setattr(init_cmd, "ADAPTERS_DIR", fake_dir)

        with pytest.raises(ClickException) as exc:
            install_adapter("cursor", temp_dir)
        assert "not found" in str(exc.value)

    def test_install_adapter_missing_source_file(self, temp_dir, monkeypatch):
        """Test warning when adapter source file is missing."""
        from anrs import init_cmd
        # Create adapter dir but no files
        fake_dir = temp_dir / "adapters" / "cursor"
        fake_dir.mkdir(parents=True)
        monkeypatch.setattr(init_cmd, "ADAPTERS_DIR", temp_dir / "adapters")

        # Should not raise, just warn
        install_adapter("cursor", temp_dir, dry_run=True)

    def test_install_adapter_io_error(self, temp_dir, monkeypatch):
        """Test IOError handling in install_adapter."""
        import shutil
        from anrs import init_cmd

        def mock_copy2(*args, **kwargs):
            raise IOError("Permission denied")

        monkeypatch.setattr(shutil, "copy2", mock_copy2)

        with pytest.raises(ClickException) as exc:
            install_adapter("cursor", temp_dir)
        assert "Cannot install" in str(exc.value)


class TestCopyTemplateFile:
    """Tests for copy_template_file function."""

    def test_copy_nonexistent_template(self, temp_dir, capsys):
        """Test handling of non-existent template."""
        target = temp_dir / "test.txt"
        copy_template_file("nonexistent.txt", target, "test-project")
        # Should not create file
        assert not target.exists()

    def test_copy_with_state_transform(self, temp_dir):
        """Test copy with init_state transform."""
        target = temp_dir / "state.json"
        copy_template_file(
            "state.template.json", target, "test-project", "init_state")
        assert target.exists()
        data = json.loads(target.read_text())
        assert "created_at" in data.get("metadata", {})

    def test_copy_with_config_transform(self, temp_dir):
        """Test copy with init_config transform."""
        target = temp_dir / "config.json"
        copy_template_file("config.json", target, "my-project", "init_config")
        assert target.exists()
        data = json.loads(target.read_text())
        assert data["project"]["name"] == "my-project"

    def test_copy_template_json_error(self, temp_dir, monkeypatch):
        """Test copy_template_file with corrupted JSON template."""
        from anrs import init_cmd
        # Create corrupted template
        fake_templates = temp_dir / "files"
        fake_templates.mkdir(parents=True)
        (fake_templates / "corrupted.json").write_text("{invalid}")
        monkeypatch.setattr(init_cmd, "TEMPLATES_DIR", temp_dir)

        target = temp_dir / "output.json"
        with pytest.raises(ClickException) as exc:
            copy_template_file("corrupted.json", target, "test", "init_state")
        assert "Corrupted" in str(exc.value)

    def test_copy_template_io_error(self, temp_dir, monkeypatch):
        """Test copy_template_file with IO error."""
        from anrs import init_cmd
        from anrs.constants import TEMPLATES_DIR

        def mock_write_text(self, content):
            raise IOError("Permission denied")

        target = temp_dir / "output.md"
        # Mock the write to fail
        monkeypatch.setattr(Path, "write_text", mock_write_text)

        with pytest.raises((ClickException, IOError)):
            copy_template_file("ENTRY.md", target, "test")


class TestDetectConflicts:
    """Tests for detect_conflicts function."""

    def test_detect_no_conflicts(self, temp_dir):
        """Test no conflicts on fresh directory."""
        manifest = resolve_manifest("minimal")
        conflicts = detect_conflicts(manifest, temp_dir)
        assert conflicts == []

    def test_detect_conflicts_existing(self, runner, temp_dir):
        """Test detecting conflicts with existing files."""
        # Create some files
        runner.invoke(cli, ["init", str(temp_dir)])
        manifest = resolve_manifest("minimal")
        conflicts = detect_conflicts(manifest, temp_dir)
        assert len(conflicts) > 0

    def test_detect_conflicts_with_adapter(self, runner, temp_dir):
        """Test detecting conflicts with adapter files."""
        # Init with adapter
        runner.invoke(cli, ["init", "--adapter", "cursor", str(temp_dir)])
        manifest = resolve_manifest("minimal")
        # Pass adapter to detect adapter file conflicts
        conflicts = detect_conflicts(manifest, temp_dir, adapter="cursor")
        # Should detect adapter file conflict
        adapter_conflicts = [
            c for c in conflicts if ".cursorrules" in c["file"]]
        assert len(adapter_conflicts) >= 1


class TestInstallFileWithStrategy:
    """Tests for install_file_with_strategy function."""

    def test_skip_strategy(self, temp_dir):
        """Test SKIP strategy skips existing files."""
        from anrs.constants import TEMPLATES_DIR
        source = TEMPLATES_DIR / "files" / "config.json"
        target = temp_dir / "config.json"
        target.write_text('{"existing": true}')

        backup_dir = temp_dir / ".backups"
        install_file_with_strategy(
            source, target, "test", None,
            ConflictStrategy.SKIP, backup_dir, "test_id"
        )
        # Should not overwrite
        assert '{"existing": true}' == target.read_text()

    def test_merge_strategy_json(self, temp_dir):
        """Test MERGE strategy merges JSON files."""
        from anrs.constants import TEMPLATES_DIR
        source = TEMPLATES_DIR / "files" / "state.template.json"
        target = temp_dir / "state.json"
        # Create existing with custom status
        target.write_text(json.dumps({
            "status": "active",
            "current_task": "task-123",
            "metadata": {"created_at": "2024-01-01"}
        }))

        backup_dir = temp_dir / ".backups"
        install_file_with_strategy(
            source, target, "test", None,
            ConflictStrategy.MERGE, backup_dir, "test_id"
        )
        data = json.loads(target.read_text())
        # User values should be preserved
        assert data["status"] == "active"
        assert data["current_task"] == "task-123"

    def test_backup_and_overwrite_strategy(self, temp_dir):
        """Test BACKUP_AND_OVERWRITE creates backup."""
        from anrs.constants import TEMPLATES_DIR
        source = TEMPLATES_DIR / "files" / "ENTRY.md"
        target = temp_dir / "ENTRY.md"
        target.write_text("old content")

        backup_dir = temp_dir / ".backups"
        install_file_with_strategy(
            source, target, "test", None,
            ConflictStrategy.BACKUP_AND_OVERWRITE, backup_dir, "test_id"
        )
        # Backup should exist
        assert backup_dir.exists()
        backup_files = list(backup_dir.glob("ENTRY.md.*"))
        assert len(backup_files) == 1

    def test_install_file_missing_template(self, temp_dir, capsys):
        """Test install_file_with_strategy with missing template."""
        source = temp_dir / "nonexistent.txt"
        target = temp_dir / "target.txt"
        backup_dir = temp_dir / ".backups"

        # Should not raise, just warn
        install_file_with_strategy(
            source, target, "test", None,
            ConflictStrategy.BACKUP_AND_OVERWRITE, backup_dir, "test_id"
        )
        assert not target.exists()

    def test_install_file_json_error(self, temp_dir, monkeypatch):
        """Test install_file_with_strategy with JSON error."""
        # Create corrupted JSON template
        source = temp_dir / "corrupted.json"
        source.write_text("{invalid}")
        target = temp_dir / "target.json"
        backup_dir = temp_dir / ".backups"

        with pytest.raises(ClickException) as exc:
            install_file_with_strategy(
                source, target, "test", "init_state",
                ConflictStrategy.BACKUP_AND_OVERWRITE, backup_dir, "test_id"
            )
        assert "Corrupted" in str(exc.value)


class TestInstallAdapterWithStrategy:
    """Tests for install_adapter_with_strategy function."""

    def test_install_adapter_with_strategy_unknown(self, temp_dir):
        """Test error with unknown adapter."""
        from anrs.init_cmd import install_adapter_with_strategy
        backup_dir = temp_dir / ".backups"

        with pytest.raises(ClickException) as exc:
            install_adapter_with_strategy(
                "nonexistent", temp_dir,
                ConflictStrategy.BACKUP_AND_OVERWRITE, backup_dir, "test_id"
            )
        assert "Unknown adapter" in str(exc.value)

    def test_install_adapter_with_strategy_missing_dir(self, temp_dir, monkeypatch):
        """Test error with missing adapter directory."""
        from anrs import init_cmd
        from anrs.init_cmd import install_adapter_with_strategy

        fake_dir = temp_dir / "fake_adapters"
        monkeypatch.setattr(init_cmd, "ADAPTERS_DIR", fake_dir)
        backup_dir = temp_dir / ".backups"

        with pytest.raises(ClickException) as exc:
            install_adapter_with_strategy(
                "cursor", temp_dir,
                ConflictStrategy.BACKUP_AND_OVERWRITE, backup_dir, "test_id"
            )
        assert "not found" in str(exc.value)

    def test_install_adapter_with_strategy_skip(self, temp_dir):
        """Test SKIP strategy for adapter installation."""
        from anrs.init_cmd import install_adapter_with_strategy
        # Create existing adapter file
        (temp_dir / ".cursorrules").write_text("user config")
        backup_dir = temp_dir / ".backups"

        install_adapter_with_strategy(
            "cursor", temp_dir,
            ConflictStrategy.SKIP, backup_dir, "test_id"
        )
        # Should not overwrite
        assert (temp_dir / ".cursorrules").read_text() == "user config"

    def test_install_adapter_with_strategy_backup(self, temp_dir):
        """Test BACKUP_AND_OVERWRITE strategy for adapter."""
        from anrs.init_cmd import install_adapter_with_strategy
        # Create existing adapter file
        (temp_dir / ".cursorrules").write_text("user config")
        backup_dir = temp_dir / ".backups"

        install_adapter_with_strategy(
            "cursor", temp_dir,
            ConflictStrategy.BACKUP_AND_OVERWRITE, backup_dir, "test_id"
        )
        # Should create backup
        assert backup_dir.exists()
        backup_files = list(backup_dir.glob(".cursorrules.*"))
        assert len(backup_files) == 1

    def test_install_adapter_with_strategy_io_error(self, temp_dir, monkeypatch):
        """Test IOError handling in install_adapter_with_strategy."""
        import shutil
        from anrs.init_cmd import install_adapter_with_strategy

        def mock_copy2(*args, **kwargs):
            raise IOError("Permission denied")

        monkeypatch.setattr(shutil, "copy2", mock_copy2)
        backup_dir = temp_dir / ".backups"

        with pytest.raises(ClickException) as exc:
            install_adapter_with_strategy(
                "cursor", temp_dir,
                ConflictStrategy.BACKUP_AND_OVERWRITE, backup_dir, "test_id"
            )
        assert "Cannot install" in str(exc.value)

    def test_install_adapter_with_strategy_missing_source(self, temp_dir, monkeypatch):
        """Test warning when adapter source file is missing."""
        from anrs import init_cmd
        from anrs.init_cmd import install_adapter_with_strategy
        # Create adapter dir but no files
        fake_dir = temp_dir / "adapters" / "cursor"
        fake_dir.mkdir(parents=True)
        monkeypatch.setattr(init_cmd, "ADAPTERS_DIR", temp_dir / "adapters")
        backup_dir = temp_dir / ".backups"

        # Should not raise, just warn and skip
        install_adapter_with_strategy(
            "cursor", temp_dir,
            ConflictStrategy.BACKUP_AND_OVERWRITE, backup_dir, "test_id"
        )


class TestGetManifestIOError:
    """Tests for get_manifest IO error handling."""

    def test_get_manifest_io_error(self, temp_dir, monkeypatch):
        """Test get_manifest handles IO errors."""
        from anrs import init_cmd

        # Create manifest directory but make read fail
        manifests_dir = temp_dir / "manifests"
        manifests_dir.mkdir()
        manifest_file = manifests_dir / "broken.json"
        manifest_file.write_text('{"name": "test"}')
        monkeypatch.setattr(init_cmd, "TEMPLATES_DIR", temp_dir)

        # Mock open to raise IOError
        original_open = open

        def mock_open(path, *args, **kwargs):
            if "broken.json" in str(path):
                raise IOError("Cannot read")
            return original_open(path, *args, **kwargs)

        monkeypatch.setattr("builtins.open", mock_open)

        with pytest.raises(ClickException) as exc:
            get_manifest("broken")
        assert "Cannot read" in str(exc.value)
