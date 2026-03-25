"""Tests for ANRS CLI harness command."""

import pytest
from pathlib import Path
from click.testing import CliRunner

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
