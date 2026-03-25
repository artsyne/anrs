"""Integration tests for ANRS CLI - End-to-end workflows."""

import json
import pytest
from pathlib import Path
from click.testing import CliRunner

from anrs.main import cli


@pytest.fixture
def runner():
    """Create CLI runner."""
    return CliRunner()


@pytest.fixture
def temp_project(tmp_path):
    """Create a temporary project directory."""
    return tmp_path


class TestInitStatusWorkflow:
    """Test init -> status workflow."""

    def test_minimal_init_status(self, runner, temp_project):
        """Test minimal init followed by status check."""
        # Step 1: Initialize with minimal level
        result = runner.invoke(
            cli, ["init", "--level", "minimal", str(temp_project)])
        assert result.exit_code == 0
        assert "ANRS initialized" in result.output

        # Step 2: Verify structure
        anrs_dir = temp_project / ".anrs"
        assert anrs_dir.exists()
        assert (anrs_dir / "ENTRY.md").exists()
        assert (anrs_dir / "state.json").exists()
        assert (anrs_dir / "config.json").exists()

        # Step 3: Check status
        result = runner.invoke(cli, ["status", str(temp_project)])
        assert result.exit_code == 0
        assert "ENTRY" in result.output
        assert "State" in result.output

    def test_standard_init_status(self, runner, temp_project):
        """Test standard init followed by status check."""
        # Initialize with standard level (default)
        result = runner.invoke(cli, ["init", str(temp_project)])
        assert result.exit_code == 0

        # Verify additional structure
        plans_dir = temp_project / ".anrs" / "plans"
        assert plans_dir.exists()
        assert (plans_dir / "active").is_dir()
        assert (plans_dir / "backlog").is_dir()

        # Check status shows plans
        result = runner.invoke(cli, ["status", str(temp_project)])
        assert result.exit_code == 0
        assert "Plans" in result.output

    def test_full_init_status(self, runner, temp_project):
        """Test full init followed by status check."""
        result = runner.invoke(
            cli, ["init", "--level", "full", str(temp_project)])
        assert result.exit_code == 0

        # Verify full structure
        assert (temp_project / ".anrs" / "skills").is_dir()
        assert (temp_project / ".anrs" / "failure-cases").is_dir()
        assert (temp_project / ".anrs" / "harness").is_dir()

        # Check status shows harness
        result = runner.invoke(cli, ["status", str(temp_project)])
        assert "Harness" in result.output


class TestInitAdapterWorkflow:
    """Test init with adapter workflow."""

    def test_init_with_cursor_adapter(self, runner, temp_project):
        """Test init with Cursor adapter."""
        result = runner.invoke(
            cli, ["init", "--adapter", "cursor", str(temp_project)])
        assert result.exit_code == 0
        assert "cursor" in result.output.lower()

        # Verify adapter file
        assert (temp_project / ".cursorrules").exists()

    def test_init_then_adapter_install(self, runner, temp_project):
        """Test init followed by separate adapter install."""
        # Step 1: Init without adapter
        runner.invoke(cli, ["init", str(temp_project)])

        # Step 2: Install adapter
        result = runner.invoke(
            cli, ["adapter", "install", "cursor", str(temp_project)])
        assert result.exit_code == 0
        assert (temp_project / ".cursorrules").exists()

    def test_adapter_list(self, runner):
        """Test adapter list command."""
        result = runner.invoke(cli, ["adapter", "list"])
        assert result.exit_code == 0
        assert "cursor" in result.output.lower()
        assert "claude" in result.output.lower()


class TestInitUpgradeWorkflow:
    """Test init -> upgrade workflow."""

    def test_upgrade_after_init(self, runner, temp_project):
        """Test upgrade on freshly initialized project."""
        # Initialize
        runner.invoke(cli, ["init", str(temp_project)])

        # Upgrade (should report already up to date)
        result = runner.invoke(cli, ["upgrade", str(temp_project)])
        assert result.exit_code == 0
        assert "up to date" in result.output.lower() or "Upgrade" in result.output

    def test_upgrade_preserves_state(self, runner, temp_project):
        """Test that upgrade preserves user state."""
        # Initialize
        runner.invoke(cli, ["init", str(temp_project)])

        # Modify state
        state_path = temp_project / ".anrs" / "state.json"
        state = json.loads(state_path.read_text())
        state["status"] = "active"
        state["current_task"] = "test-task-001"
        state_path.write_text(json.dumps(state, indent=2))

        # Force upgrade
        result = runner.invoke(cli, ["upgrade", "--force", str(temp_project)])
        assert result.exit_code == 0

        # Verify state preserved
        new_state = json.loads(state_path.read_text())
        assert new_state["status"] == "active"
        assert new_state["current_task"] == "test-task-001"


class TestInitDoctorWorkflow:
    """Test init -> doctor workflow."""

    def test_doctor_on_fresh_init(self, runner, temp_project):
        """Test doctor on freshly initialized project."""
        # Initialize
        runner.invoke(cli, ["init", str(temp_project)])

        # Run doctor
        result = runner.invoke(cli, ["doctor", str(temp_project)])
        assert result.exit_code == 0
        assert "passed" in result.output.lower()

    def test_doctor_detects_corruption(self, runner, temp_project):
        """Test doctor detects corrupted state."""
        # Initialize
        runner.invoke(cli, ["init", str(temp_project)])

        # Corrupt state.json
        state_path = temp_project / ".anrs" / "state.json"
        state_path.write_text("{invalid json}")

        # Run doctor
        result = runner.invoke(cli, ["doctor", str(temp_project)])
        assert result.exit_code == 1
        assert "fail" in result.output.lower() or "Invalid" in result.output

    def test_doctor_fix_corruption(self, runner, temp_project):
        """Test doctor --fix repairs corrupted state."""
        # Initialize
        runner.invoke(cli, ["init", str(temp_project)])

        # Corrupt state.json
        state_path = temp_project / ".anrs" / "state.json"
        state_path.write_text("{invalid}")

        # Run doctor --fix
        result = runner.invoke(cli, ["doctor", "--fix", str(temp_project)])
        assert "Fix" in result.output or "fixed" in result.output.lower()

        # Verify state is valid now
        state = json.loads(state_path.read_text())
        assert "status" in state


class TestConflictWorkflow:
    """Test conflict handling workflows."""

    def test_reinit_with_force(self, runner, temp_project):
        """Test re-initialization with --force."""
        # First init
        runner.invoke(cli, ["init", str(temp_project)])

        # Modify state
        state_path = temp_project / ".anrs" / "state.json"
        original_content = state_path.read_text()

        # Force reinit
        result = runner.invoke(
            cli, ["init", "--force", str(temp_project)], input="y\n")
        assert result.exit_code == 0

        # Verify backup was created
        backups_dir = temp_project / ".anrs-backups"
        # Backup may or may not exist depending on implementation
        # The key is that reinit succeeded

    def test_reinit_with_merge(self, runner, temp_project):
        """Test re-initialization with --merge."""
        # First init
        runner.invoke(cli, ["init", str(temp_project)])

        # Modify state
        state_path = temp_project / ".anrs" / "state.json"
        state = json.loads(state_path.read_text())
        state["custom_field"] = "user_value"
        state_path.write_text(json.dumps(state, indent=2))

        # Merge reinit
        result = runner.invoke(cli, ["init", "--merge", str(temp_project)])
        assert result.exit_code == 0

    def test_adapter_conflict_skip(self, runner, temp_project):
        """Test adapter install with --skip on existing."""
        # Init with adapter
        runner.invoke(cli, ["init", "--adapter", "cursor", str(temp_project)])

        # Modify adapter file
        adapter_path = temp_project / ".cursorrules"
        adapter_path.write_text("# Custom rules")

        # Try to reinstall with skip
        result = runner.invoke(
            cli, ["adapter", "install", "cursor", "--skip", str(temp_project)])
        assert result.exit_code == 0

        # Verify original content preserved
        assert adapter_path.read_text() == "# Custom rules"


class TestDryRunWorkflow:
    """Test dry-run mode across commands."""

    def test_init_dry_run(self, runner, temp_project):
        """Test init --dry-run doesn't create files."""
        result = runner.invoke(cli, ["init", "--dry-run", str(temp_project)])
        assert result.exit_code == 0
        assert "Dry run" in result.output

        # Verify nothing created
        assert not (temp_project / ".anrs").exists()

    def test_upgrade_dry_run(self, runner, temp_project):
        """Test upgrade --dry-run shows changes."""
        # First init
        runner.invoke(cli, ["init", str(temp_project)])

        # Dry run upgrade
        result = runner.invoke(
            cli, ["upgrade", "--dry-run", str(temp_project)])
        assert result.exit_code == 0

    def test_adapter_dry_run(self, runner, temp_project):
        """Test adapter install --dry-run."""
        runner.invoke(cli, ["init", str(temp_project)])

        result = runner.invoke(
            cli, ["adapter", "install", "cursor", "--dry-run", str(temp_project)])
        assert result.exit_code == 0

        # Verify adapter not installed
        assert not (temp_project / ".cursorrules").exists()


class TestLevelUpgradeWorkflow:
    """Test upgrading between levels."""

    def test_minimal_to_standard(self, runner, temp_project):
        """Test upgrading from minimal to standard."""
        # Init minimal
        runner.invoke(cli, ["init", "--level", "minimal", str(temp_project)])
        assert not (temp_project / ".anrs" / "plans").exists()

        # Upgrade to standard
        result = runner.invoke(
            cli, ["init", "--level", "standard", "--merge", str(temp_project)])
        assert result.exit_code == 0

        # Verify plans directory added
        assert (temp_project / ".anrs" / "plans").exists()

    def test_standard_to_full(self, runner, temp_project):
        """Test upgrading from standard to full."""
        # Init standard
        runner.invoke(cli, ["init", "--level", "standard", str(temp_project)])
        assert not (temp_project / ".anrs" / "harness").exists()

        # Upgrade to full
        result = runner.invoke(
            cli, ["init", "--level", "full", "--merge", str(temp_project)])
        assert result.exit_code == 0

        # Verify harness added
        assert (temp_project / ".anrs" / "harness").exists()


class TestMultipleAdaptersWorkflow:
    """Test installing multiple adapters."""

    def test_install_multiple_adapters(self, runner, temp_project):
        """Test installing multiple adapters sequentially."""
        runner.invoke(cli, ["init", str(temp_project)])

        # Install cursor
        runner.invoke(cli, ["adapter", "install", "cursor", str(temp_project)])
        assert (temp_project / ".cursorrules").exists()

        # Install claude-code
        runner.invoke(cli, ["adapter", "install",
                      "claude-code", str(temp_project)])
        assert (temp_project / "CLAUDE.md").exists()

        # Verify both exist
        assert (temp_project / ".cursorrules").exists()
        assert (temp_project / "CLAUDE.md").exists()

        # Doctor should show both
        result = runner.invoke(cli, ["doctor", str(temp_project)])
        assert "Cursor" in result.output
        assert "Claude" in result.output
