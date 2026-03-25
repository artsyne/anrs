"""Tests for ANRS CLI doctor command."""

import json
import pytest
from pathlib import Path
from click.testing import CliRunner

from anrs.main import cli
from anrs.doctor_cmd import (
    check_python_version,
    check_anrs_directory,
    check_entry_md,
    check_state_json,
    check_config_json,
    check_adapter_files,
    check_plans_directory,
    run_health_checks,
)


@pytest.fixture
def runner():
    """Create CLI runner."""
    return CliRunner()


@pytest.fixture
def temp_dir(tmp_path):
    """Create a temporary directory for testing."""
    return tmp_path


class TestDoctorCommand:
    """Tests for doctor CLI command."""

    def test_doctor_help(self, runner):
        """Test doctor --help."""
        result = runner.invoke(cli, ["doctor", "--help"])
        assert result.exit_code == 0
        assert "Diagnose and repair" in result.output
        assert "--fix" in result.output

    def test_doctor_no_anrs(self, runner, temp_dir):
        """Test doctor on non-ANRS directory."""
        result = runner.invoke(cli, ["doctor", str(temp_dir)])
        assert result.exit_code == 1
        assert "Not an ANRS repository" in result.output

    def test_doctor_valid_anrs(self, runner, temp_dir):
        """Test doctor on valid ANRS directory."""
        # Initialize ANRS
        runner.invoke(cli, ["init", str(temp_dir)])

        # Run doctor
        result = runner.invoke(cli, ["doctor", str(temp_dir)])
        assert result.exit_code == 0
        assert "passed" in result.output

    def test_doctor_verbose(self, runner, temp_dir):
        """Test doctor with verbose flag."""
        runner.invoke(cli, ["init", str(temp_dir)])
        result = runner.invoke(cli, ["doctor", "--verbose", str(temp_dir)])
        assert result.exit_code == 0
        assert "Checking:" in result.output


class TestHealthChecks:
    """Tests for individual health check functions."""

    def test_check_python_version(self):
        """Test Python version check."""
        result = check_python_version()
        assert result.status == "pass"
        assert "Python" in result.message

    def test_check_anrs_directory_missing(self, temp_dir):
        """Test check when .anrs doesn't exist."""
        result = check_anrs_directory(temp_dir)
        assert result.status == "fail"
        assert result.fix_hint is not None

    def test_check_anrs_directory_exists(self, temp_dir):
        """Test check when .anrs exists."""
        (temp_dir / ".anrs").mkdir()
        result = check_anrs_directory(temp_dir)
        assert result.status == "pass"

    def test_check_entry_md_missing(self, temp_dir):
        """Test check when ENTRY.md is missing."""
        (temp_dir / ".anrs").mkdir()
        result = check_entry_md(temp_dir)
        assert result.status == "fail"

    def test_check_entry_md_exists(self, temp_dir):
        """Test check when ENTRY.md exists."""
        anrs_dir = temp_dir / ".anrs"
        anrs_dir.mkdir()
        (anrs_dir / "ENTRY.md").write_text("# Entry Point\n" + "x" * 100)
        result = check_entry_md(temp_dir)
        assert result.status == "pass"

    def test_check_state_json_missing(self, temp_dir):
        """Test check when state.json is missing."""
        (temp_dir / ".anrs").mkdir()
        result = check_state_json(temp_dir)
        assert result.status == "fail"

    def test_check_state_json_invalid(self, temp_dir):
        """Test check when state.json has invalid JSON."""
        anrs_dir = temp_dir / ".anrs"
        anrs_dir.mkdir()
        (anrs_dir / "state.json").write_text("{invalid json}")
        result = check_state_json(temp_dir)
        assert result.status == "fail"
        assert "Invalid JSON" in result.message

    def test_check_state_json_missing_fields(self, temp_dir):
        """Test check when state.json missing required fields."""
        anrs_dir = temp_dir / ".anrs"
        anrs_dir.mkdir()
        (anrs_dir / "state.json").write_text("{}")
        result = check_state_json(temp_dir)
        assert result.status == "fail"
        assert "Missing required fields" in result.message

    def test_check_state_json_valid(self, temp_dir):
        """Test check when state.json is valid."""
        anrs_dir = temp_dir / ".anrs"
        anrs_dir.mkdir()
        state = {
            "status": "idle",
            "metadata": {"created_at": "2024-01-01"}
        }
        (anrs_dir / "state.json").write_text(json.dumps(state))
        result = check_state_json(temp_dir)
        assert result.status == "pass"

    def test_check_config_json_missing(self, temp_dir):
        """Test check when config.json is missing."""
        (temp_dir / ".anrs").mkdir()
        result = check_config_json(temp_dir)
        assert result.status == "fail"

    def test_check_config_json_valid(self, temp_dir):
        """Test check when config.json is valid."""
        anrs_dir = temp_dir / ".anrs"
        anrs_dir.mkdir()
        config = {"project": {"name": "test-project"}}
        (anrs_dir / "config.json").write_text(json.dumps(config))
        result = check_config_json(temp_dir)
        assert result.status == "pass"

    def test_check_adapter_files_none(self, temp_dir):
        """Test check when no adapters installed."""
        result = check_adapter_files(temp_dir)
        assert result.status == "warn"

    def test_check_adapter_files_cursor(self, temp_dir):
        """Test check when Cursor adapter installed."""
        (temp_dir / ".cursorrules").write_text("# Cursor rules")
        result = check_adapter_files(temp_dir)
        assert result.status == "pass"
        assert "Cursor" in result.message

    def test_check_plans_directory_missing(self, temp_dir):
        """Test check when plans directory missing."""
        (temp_dir / ".anrs").mkdir()
        result = check_plans_directory(temp_dir)
        assert result.status == "warn"

    def test_check_plans_directory_complete(self, temp_dir):
        """Test check when plans directory complete."""
        plans_dir = temp_dir / ".anrs" / "plans"
        for subdir in ["active", "backlog", "completed"]:
            (plans_dir / subdir).mkdir(parents=True)
        result = check_plans_directory(temp_dir)
        assert result.status == "pass"


class TestHealthReport:
    """Tests for health report generation."""

    def test_run_health_checks_no_anrs(self, temp_dir):
        """Test report when .anrs doesn't exist."""
        report = run_health_checks(temp_dir)
        assert report.failures >= 1
        assert any(c.name == ".anrs Directory" for c in report.checks)

    def test_run_health_checks_valid(self, temp_dir, runner):
        """Test report on valid ANRS installation."""
        runner.invoke(cli, ["init", str(temp_dir)])
        report = run_health_checks(temp_dir)
        assert report.passed >= 4
        assert report.failures == 0


class TestDoctorFix:
    """Tests for doctor --fix functionality."""

    def test_fix_invalid_state_json(self, runner, temp_dir):
        """Test fixing invalid state.json."""
        # Create invalid state.json
        anrs_dir = temp_dir / ".anrs"
        anrs_dir.mkdir()
        (anrs_dir / "ENTRY.md").write_text("# Entry\n" + "x" * 100)
        (anrs_dir / "config.json").write_text('{"project":{"name":"test"}}')
        (anrs_dir / "state.json").write_text("{invalid}")

        # Run doctor --fix
        result = runner.invoke(cli, ["doctor", "--fix", str(temp_dir)])

        # Verify fix
        assert "Fixed" in result.output or "Could not fix" in result.output
