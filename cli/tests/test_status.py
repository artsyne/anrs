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

    def test_status_with_invalid_state_json(self, runner, tmp_path):
        """Test status when state.json has invalid JSON."""
        anrs_dir = tmp_path / ".anrs"
        anrs_dir.mkdir()
        (anrs_dir / "ENTRY.md").write_text("# Entry")
        (anrs_dir / "state.json").write_text("invalid json")
        (anrs_dir / "config.json").write_text("{}")

        result = runner.invoke(cli, ["status", str(tmp_path)])
        # Should still complete, showing partial status
        assert result.exit_code == 0

    def test_status_with_plans_directory(self, runner, tmp_path):
        """Test status with plans directory."""
        anrs_dir = tmp_path / ".anrs"
        anrs_dir.mkdir()
        (anrs_dir / "ENTRY.md").write_text("# Entry")
        (anrs_dir / "state.json").write_text('{}')
        (anrs_dir / "config.json").write_text('{}')
        (anrs_dir / "plans").mkdir()

        result = runner.invoke(cli, ["status", str(tmp_path)])
        assert result.exit_code == 0
        assert "Plans" in result.output

    def test_status_with_harness_directory(self, runner, tmp_path):
        """Test status with harness directory."""
        anrs_dir = tmp_path / ".anrs"
        anrs_dir.mkdir()
        (anrs_dir / "ENTRY.md").write_text("# Entry")
        (anrs_dir / "state.json").write_text('{}')
        (anrs_dir / "config.json").write_text('{}')
        (tmp_path / "harness").mkdir()  # harness is at root level

        result = runner.invoke(cli, ["status", str(tmp_path)])
        assert result.exit_code == 0
        assert "Harness" in result.output

    def test_status_corrupted_state_json(self, runner, tmp_path):
        """Test status shows warning when state.json is corrupted."""
        anrs_dir = tmp_path / ".anrs"
        anrs_dir.mkdir()
        (anrs_dir / "ENTRY.md").write_text("# Entry")
        (anrs_dir / "state.json").write_text("{not valid json}")
        (anrs_dir / "config.json").write_text('{}')

        result = runner.invoke(cli, ["status", str(tmp_path)])
        assert result.exit_code == 0
        # Should show warning about corrupted state
        assert "corrupted" in result.output.lower() or "warning" in result.output.lower()

    def test_status_with_skills_directory(self, runner, tmp_path):
        """Test status with skills directory."""
        anrs_dir = tmp_path / ".anrs"
        anrs_dir.mkdir()
        (anrs_dir / "ENTRY.md").write_text("# Entry")
        (anrs_dir / "state.json").write_text('{}')
        (anrs_dir / "config.json").write_text('{}')
        (anrs_dir / "skills").mkdir()

        result = runner.invoke(cli, ["status", str(tmp_path)])
        assert result.exit_code == 0
        assert "Skills" in result.output

    def test_status_state_read_error(self, runner, tmp_path, monkeypatch):
        """Test status handles generic exceptions when reading state."""
        anrs_dir = tmp_path / ".anrs"
        anrs_dir.mkdir()
        (anrs_dir / "ENTRY.md").write_text("# Entry")
        (anrs_dir / "state.json").write_text('{"status": "idle"}')
        (anrs_dir / "config.json").write_text('{}')

        # Mock json.load to raise a generic exception
        import json as json_module
        original_load = json_module.load

        def mock_load(f):
            if "state.json" in str(f.name):
                raise RuntimeError("Unexpected read error")
            return original_load(f)

        monkeypatch.setattr(json_module, "load", mock_load)

        result = runner.invoke(cli, ["status", str(tmp_path)])
        # Should still complete, showing error
        assert result.exit_code == 0
        assert "Error" in result.output or "error" in result.output.lower()
