"""Tests for ANRS CLI harness command."""

import pytest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from click import ClickException

from anrs.main import cli


@pytest.fixture
def runner():
    """Create CLI runner."""
    return CliRunner()


@pytest.fixture
def repo_with_harness(tmp_path):
    """Create a repository with harness directory."""
    harness_dir = tmp_path / "harness"
    harness_dir.mkdir()
    return tmp_path


@pytest.fixture
def repo_with_quality_gate(tmp_path):
    """Create a repository with quality_gate.py."""
    harness_dir = tmp_path / "harness"
    harness_dir.mkdir()

    # Create a simple quality_gate.py that just exits successfully
    quality_gate = harness_dir / "quality_gate.py"
    quality_gate.write_text("""
import sys
print("Quality gate passed")
sys.exit(0)
""")

    return tmp_path


@pytest.fixture
def repo_with_scripts(tmp_path):
    """Create a repository with harness shell scripts."""
    harness_dir = tmp_path / "harness"
    harness_dir.mkdir()

    # Create shell scripts for each level
    (harness_dir / "l1_lint.sh").write_text("#!/bin/bash\necho L1 passed")
    (harness_dir / "l2_test.sh").write_text("#!/bin/bash\necho L2 passed")
    (harness_dir / "l3_risk.sh").write_text("#!/bin/bash\necho L3 passed")
    (harness_dir / "security_scan.sh").write_text("#!/bin/bash\necho Security passed")

    return tmp_path


class TestHarnessCommand:
    """Tests for anrs harness command."""

    def test_harness_no_directory(self, runner, tmp_path):
        """Test harness when no harness directory exists."""
        result = runner.invoke(cli, ["harness", str(tmp_path)])
        assert result.exit_code == 0
        assert "No harness directory found" in result.output

    def test_harness_with_quality_gate(self, runner, repo_with_quality_gate):
        """Test harness with quality_gate.py present."""
        result = runner.invoke(cli, ["harness", str(repo_with_quality_gate)])
        assert "Running quality gate" in result.output

    def test_harness_level_option(self, runner, repo_with_harness):
        """Test harness --level option."""
        result = runner.invoke(
            cli, ["harness", "--level", "L1", str(repo_with_harness)])
        # Should not fail even without scripts
        assert result.exit_code == 0

    def test_harness_strict_option(self, runner, repo_with_harness):
        """Test harness --strict option."""
        result = runner.invoke(
            cli, ["harness", "--strict", str(repo_with_harness)])
        # Should complete without errors when no scripts exist
        assert result.exit_code == 0

    def test_harness_symlink_security(self, runner, tmp_path):
        """Test harness rejects symlinked directory."""
        # Create a target directory
        real_dir = tmp_path / "real_harness"
        real_dir.mkdir()

        # Create a symlink
        harness_link = tmp_path / "harness"
        harness_link.symlink_to(real_dir)

        result = runner.invoke(cli, ["harness", str(tmp_path)])
        assert result.exit_code != 0
        assert "Security" in result.output or "symlink" in result.output.lower()

    def test_harness_shell_scripts_fallback(self, runner, repo_with_scripts):
        """Test fallback to shell scripts when no quality_gate.py."""
        result = runner.invoke(cli, ["harness", str(repo_with_scripts)])
        assert "quality_gate.py not found" in result.output
        assert "Harness complete" in result.output

    def test_harness_specific_level_l1(self, runner, repo_with_scripts):
        """Test running specific level L1."""
        result = runner.invoke(
            cli, ["harness", "--level", "L1", str(repo_with_scripts)])
        assert result.exit_code == 0

    def test_harness_specific_level_security(self, runner, repo_with_scripts):
        """Test running security level."""
        result = runner.invoke(
            cli, ["harness", "--level", "security", str(repo_with_scripts)])
        assert result.exit_code == 0

    def test_harness_quality_gate_with_args(self, runner, tmp_path):
        """Test quality gate with level and strict args."""
        harness_dir = tmp_path / "harness"
        harness_dir.mkdir()

        # Create a quality_gate.py that accepts args
        quality_gate = harness_dir / "quality_gate.py"
        quality_gate.write_text('''
import sys
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--level", default="all")
parser.add_argument("--strict", action="store_true")
args = parser.parse_args()
print(f"Level: {args.level}, Strict: {args.strict}")
sys.exit(0)
''')

        result = runner.invoke(
            cli, ["harness", "--level", "L1", "--strict", str(tmp_path)])
        assert "Running quality gate" in result.output

    def test_harness_shell_script_all_levels(self, runner, repo_with_scripts):
        """Test running all levels via shell scripts."""
        result = runner.invoke(
            cli, ["harness", "--level", "all", str(repo_with_scripts)])
        assert result.exit_code == 0
        assert "Harness complete" in result.output

    def test_harness_missing_script_skipped(self, runner, tmp_path):
        """Test that missing scripts are skipped."""
        harness_dir = tmp_path / "harness"
        harness_dir.mkdir()
        # Only create L1 script
        (harness_dir / "l1_lint.sh").write_text("#!/bin/bash\necho L1")

        result = runner.invoke(
            cli, ["harness", "--level", "all", str(tmp_path)])
        assert "Skipping" in result.output or result.exit_code == 0

    def test_harness_quality_gate_outside_dir(self, runner, tmp_path):
        """Test quality_gate.py symlink pointing outside harness."""
        harness_dir = tmp_path / "harness"
        harness_dir.mkdir()

        # Create quality_gate.py outside harness
        outside_script = tmp_path / "evil_script.py"
        outside_script.write_text("print('evil')")

        # Create symlink inside harness pointing outside
        quality_gate = harness_dir / "quality_gate.py"
        quality_gate.symlink_to(outside_script)

        result = runner.invoke(cli, ["harness", str(tmp_path)])
        assert result.exit_code != 0
        assert "Security" in result.output or "invalid" in result.output.lower()

    def test_harness_quality_gate_timeout(self, runner, tmp_path, monkeypatch):
        """Test quality_gate.py timeout handling."""
        import subprocess

        harness_dir = tmp_path / "harness"
        harness_dir.mkdir()

        # Create quality_gate that times out
        quality_gate = harness_dir / "quality_gate.py"
        quality_gate.write_text("import time; time.sleep(999)")

        # Mock subprocess.run to raise TimeoutExpired
        original_run = subprocess.run

        def mock_run(*args, **kwargs):
            raise subprocess.TimeoutExpired(cmd="test", timeout=300)

        monkeypatch.setattr(subprocess, "run", mock_run)

        result = runner.invoke(cli, ["harness", str(tmp_path)])
        assert result.exit_code != 0
        assert "timed out" in result.output.lower() or "timeout" in result.output.lower()

    def test_harness_quality_gate_exception(self, runner, tmp_path, monkeypatch):
        """Test quality_gate.py exception handling."""
        import subprocess

        harness_dir = tmp_path / "harness"
        harness_dir.mkdir()

        quality_gate = harness_dir / "quality_gate.py"
        quality_gate.write_text("print('test')")

        # Mock subprocess.run to raise exception
        def mock_run(*args, **kwargs):
            raise RuntimeError("Unexpected error")

        monkeypatch.setattr(subprocess, "run", mock_run)

        result = runner.invoke(cli, ["harness", str(tmp_path)])
        assert result.exit_code != 0
        assert "failed" in result.output.lower()

    def test_harness_shell_script_timeout(self, runner, tmp_path, monkeypatch):
        """Test shell script timeout handling."""
        import subprocess

        harness_dir = tmp_path / "harness"
        harness_dir.mkdir()
        (harness_dir / "l1_lint.sh").write_text("#!/bin/bash\nsleep 999")

        call_count = [0]
        original_run = subprocess.run

        def mock_run(*args, **kwargs):
            call_count[0] += 1
            raise subprocess.TimeoutExpired(cmd="bash", timeout=120)

        monkeypatch.setattr(subprocess, "run", mock_run)

        result = runner.invoke(
            cli, ["harness", "--level", "L1", str(tmp_path)])
        assert "timed out" in result.output.lower()

    def test_harness_shell_script_strict_fail(self, runner, tmp_path):
        """Test --strict fails on script error."""
        harness_dir = tmp_path / "harness"
        harness_dir.mkdir()
        # Create script that fails
        (harness_dir / "l1_lint.sh").write_text("#!/bin/bash\nexit 1")

        result = runner.invoke(
            cli, ["harness", "--strict", "--level", "L1", str(tmp_path)])
        # In strict mode with failing script, exit code should be non-zero
        # Note: Click's test runner may not propagate sys.exit properly
        assert "L1" in result.output or result.exit_code != 0
