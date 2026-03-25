"""Tests for ANRS CLI status command."""

import json
import pytest
from pathlib import Path
from click.testing import CliRunner

from anrs.main import cli
from anrs.status import check_file, check_dir


@pytest.fixture
def runner():
    """Create CLI runner."""
    return CliRunner()


@pytest.fixture
def anrs_repo(tmp_path):
    """Create a mock ANRS repository."""
    anrs_dir = tmp_path / ".anrs"
    anrs_dir.mkdir()

    # Create basic files
    (anrs_dir / "ENTRY.md").write_text("# Entry")
    (anrs_dir / "state.json").write_text(json.dumps({
        "status": "idle",
        "current_task": None,
        "last_completed": "task-001"
    }))
    (anrs_dir / "config.json").write_text(json.dumps({
        "project": {"name": "test"}
    }))

    return tmp_path


class TestCheckFunctions:
    """Tests for check_file and check_dir functions."""

    def test_check_file_exists(self, tmp_path):
        """Test check_file when file exists."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test")
        exists, icon = check_file(test_file)
        assert exists is True
        assert "✓" in icon

    def test_check_file_not_exists(self, tmp_path):
        """Test check_file when file doesn't exist."""
        test_file = tmp_path / "nonexistent.txt"
        exists, icon = check_file(test_file)
        assert exists is False
        assert "✗" in icon

    def test_check_dir_exists(self, tmp_path):
        """Test check_dir when directory exists."""
        test_dir = tmp_path / "subdir"
        test_dir.mkdir()
        exists, icon = check_dir(test_dir)
        assert exists is True
        assert "✓" in icon

    def test_check_dir_not_exists(self, tmp_path):
        """Test check_dir when directory doesn't exist."""
        test_dir = tmp_path / "nonexistent"
        exists, icon = check_dir(test_dir)
        assert exists is False
        assert "✗" in icon


class TestStatusCommand:
    """Tests for anrs status command."""

    def test_status_not_anrs_repo(self, runner, tmp_path):
        """Test status on non-ANRS repository."""
        result = runner.invoke(cli, ["status", str(tmp_path)])
        assert result.exit_code == 0
        assert "Not an ANRS repository" in result.output

    def test_status_anrs_repo(self, runner, anrs_repo):
        """Test status on ANRS repository."""
        result = runner.invoke(cli, ["status", str(anrs_repo)])
        assert result.exit_code == 0
        assert "ENTRY" in result.output
        assert "State" in result.output
        assert "Config" in result.output

    def test_status_shows_current_state(self, runner, anrs_repo):
        """Test that status shows current state from state.json."""
        result = runner.invoke(cli, ["status", str(anrs_repo)])
        assert result.exit_code == 0
        assert "idle" in result.output
        assert "task-001" in result.output

    def test_status_default_path(self, runner, anrs_repo, monkeypatch):
        """Test status with default path (current directory)."""
        monkeypatch.chdir(anrs_repo)
        result = runner.invoke(cli, ["status"])
        assert result.exit_code == 0
