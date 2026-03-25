"""Tests for ANRS CLI init command."""

import json
import pytest
from pathlib import Path
from click.testing import CliRunner

from anrs.main import cli
from anrs.init_cmd import (
    get_manifest,
    resolve_manifest,
    init_state_transform,
    init_config_transform,
)


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
        # Should have harness directory (at root level for CI/CD)
        assert "harness" in manifest["directories"]


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
        assert (temp_dir / "harness").exists()  # harness at root for CI/CD

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
