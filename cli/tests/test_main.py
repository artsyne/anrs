"""Tests for ANRS CLI main entry point."""

import pytest
from click.testing import CliRunner

from anrs.main import cli
from anrs import __version__


@pytest.fixture
def runner():
    """Create CLI runner."""
    return CliRunner()


class TestMainCLI:
    """Tests for main CLI entry point."""

    def test_cli_help(self, runner):
        """Test CLI --help option."""
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "ANRS" in result.output
        assert "init" in result.output
        assert "status" in result.output
        assert "harness" in result.output
        assert "adapter" in result.output

    def test_cli_version(self, runner):
        """Test CLI --version option."""
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert __version__ in result.output

    def test_cli_init_help(self, runner):
        """Test anrs init --help."""
        result = runner.invoke(cli, ["init", "--help"])
        assert result.exit_code == 0
        assert "minimal" in result.output
        assert "standard" in result.output
        assert "full" in result.output

    def test_cli_status_help(self, runner):
        """Test anrs status --help."""
        result = runner.invoke(cli, ["status", "--help"])
        assert result.exit_code == 0

    def test_cli_harness_help(self, runner):
        """Test anrs harness --help."""
        result = runner.invoke(cli, ["harness", "--help"])
        assert result.exit_code == 0
        assert "L1" in result.output
        assert "L2" in result.output

    def test_cli_adapter_help(self, runner):
        """Test anrs adapter --help."""
        result = runner.invoke(cli, ["adapter", "--help"])
        assert result.exit_code == 0
