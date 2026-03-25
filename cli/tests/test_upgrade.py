"""Tests for ANRS CLI upgrade command."""

import json
import pytest
from pathlib import Path
from click.testing import CliRunner

from anrs.main import cli
from anrs.upgrade import get_current_version, backup_state, upgrade_file


@pytest.fixture
def runner():
    """Create CLI runner."""
    return CliRunner()


@pytest.fixture
def anrs_repo(tmp_path):
    """Create a mock ANRS repository with .anrs directory."""
    anrs_dir = tmp_path / ".anrs"
    anrs_dir.mkdir()

    # Create config.json
    config = {
        "version": "0.0.1",
        "project": {"name": "test-project"}
    }
    (anrs_dir / "config.json").write_text(json.dumps(config, indent=2))

    # Create state.json
    state = {
        "status": "in_progress",
        "current_task": "task-123",
        "last_completed": "task-122"
    }
    (anrs_dir / "state.json").write_text(json.dumps(state, indent=2))

    # Create ENTRY.md
    (anrs_dir / "ENTRY.md").write_text("# Old Entry\n")

    return tmp_path


class TestGetCurrentVersion:
    """Tests for get_current_version function."""

    def test_get_version_exists(self, anrs_repo):
        """Test getting version when config exists."""
        anrs_dir = anrs_repo / ".anrs"
        version = get_current_version(anrs_dir)
        assert version == "0.0.1"

    def test_get_version_no_config(self, tmp_path):
        """Test getting version when no config."""
        anrs_dir = tmp_path / ".anrs"
        anrs_dir.mkdir()
        version = get_current_version(anrs_dir)
        assert version is None


class TestBackupState:
    """Tests for backup_state function."""

    def test_backup_creates_file(self, anrs_repo):
        """Test that backup creates a backup file."""
        anrs_dir = anrs_repo / ".anrs"
        backup_dir = anrs_dir / ".backups"

        backup_state(anrs_dir, backup_dir)

        assert backup_dir.exists()
        backup_files = list(backup_dir.glob("state_*.json"))
        assert len(backup_files) == 1

    def test_backup_no_state(self, tmp_path):
        """Test backup when no state file exists."""
        anrs_dir = tmp_path / ".anrs"
        anrs_dir.mkdir()
        backup_dir = anrs_dir / ".backups"

        # Should not raise
        backup_state(anrs_dir, backup_dir)
        assert not backup_dir.exists()


class TestUpgradeFile:
    """Tests for upgrade_file function."""

    def test_upgrade_overwrites(self, tmp_path):
        """Test that upgrade overwrites file."""
        source = tmp_path / "source.md"
        target = tmp_path / "target.md"

        source.write_text("new content")
        target.write_text("old content")

        result = upgrade_file(source, target, preserve_data=False)

        assert result is True
        assert target.read_text() == "new content"

    def test_upgrade_preserves_json_data(self, tmp_path):
        """Test that upgrade preserves user data in JSON."""
        source = tmp_path / "source.json"
        target = tmp_path / "target.json"

        source.write_text(json.dumps({
            "version": "0.2",
            "status": "idle",
            "current_task": None
        }))
        target.write_text(json.dumps({
            "version": "0.1",
            "status": "in_progress",
            "current_task": "task-123"
        }))

        result = upgrade_file(source, target, preserve_data=True)

        assert result is True
        data = json.loads(target.read_text())
        # User data preserved
        assert data["status"] == "in_progress"
        assert data["current_task"] == "task-123"


class TestUpgradeCommand:
    """Tests for anrs upgrade command."""

    def test_upgrade_not_anrs_repo(self, runner, tmp_path):
        """Test upgrade on non-ANRS repository."""
        result = runner.invoke(cli, ["upgrade", str(tmp_path)])
        assert result.exit_code != 0
        assert "Not an ANRS repository" in result.output

    def test_upgrade_dry_run(self, runner, anrs_repo):
        """Test upgrade --dry-run."""
        result = runner.invoke(cli, ["upgrade", "--dry-run", str(anrs_repo)])
        assert result.exit_code == 0
        assert "Dry run" in result.output

        # Should not modify files
        config = json.loads((anrs_repo / ".anrs" / "config.json").read_text())
        assert config["version"] == "0.0.1"

    def test_upgrade_creates_backup(self, runner, anrs_repo):
        """Test that upgrade creates backup."""
        result = runner.invoke(cli, ["upgrade", "--force", str(anrs_repo)])

        backup_dir = anrs_repo / ".anrs" / ".backups"
        backup_files = list(backup_dir.glob("state_*.json"))
        assert len(backup_files) >= 1

    def test_upgrade_no_backup(self, runner, anrs_repo):
        """Test upgrade --no-backup."""
        result = runner.invoke(
            cli, ["upgrade", "--force", "--no-backup", str(anrs_repo)])

        backup_dir = anrs_repo / ".anrs" / ".backups"
        assert not backup_dir.exists()

    def test_upgrade_preserves_state(self, runner, anrs_repo):
        """Test that upgrade preserves state data."""
        result = runner.invoke(cli, ["upgrade", "--force", str(anrs_repo)])

        state = json.loads((anrs_repo / ".anrs" / "state.json").read_text())
        # User state preserved
        assert state["current_task"] == "task-123"
        assert state["status"] == "in_progress"
