"""Tests for ANRS state management with concurrency control."""

import json
import pytest
from pathlib import Path

from anrs.state import (
    StateManager,
    StateConflictError,
    atomic_state_update,
    get_state_version,
)


@pytest.fixture
def temp_anrs(tmp_path):
    """Create a temporary .anrs directory with state.json."""
    anrs_dir = tmp_path / ".anrs"
    anrs_dir.mkdir()

    state = {
        "status": "idle",
        "current_task": None,
        "_version": 1,
        "metadata": {
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00",
        }
    }
    (anrs_dir / "state.json").write_text(json.dumps(state, indent=2))

    return anrs_dir


class TestStateManager:
    """Tests for StateManager class."""

    def test_read_state(self, temp_anrs):
        """Test reading state from file."""
        manager = StateManager(temp_anrs)
        data = manager.read()

        assert data["status"] == "idle"
        assert data["_version"] == 1
        assert manager.version == 1

    def test_write_state(self, temp_anrs):
        """Test writing state to file."""
        manager = StateManager(temp_anrs)
        manager.read()
        manager.data["status"] = "active"
        manager.write()

        # Verify written
        with open(temp_anrs / "state.json") as f:
            saved = json.load(f)
        assert saved["status"] == "active"
        assert saved["_version"] == 2  # Version incremented

    def test_context_manager(self, temp_anrs):
        """Test using StateManager as context manager."""
        with StateManager(temp_anrs) as state:
            state.data["status"] = "active"
            state.data["current_task"] = "task-001"

        # Verify saved
        with open(temp_anrs / "state.json") as f:
            saved = json.load(f)
        assert saved["status"] == "active"
        assert saved["current_task"] == "task-001"

    def test_conflict_detection(self, temp_anrs):
        """Test that concurrent modifications are detected."""
        manager = StateManager(temp_anrs)
        manager.read()

        # Simulate another process modifying state
        with open(temp_anrs / "state.json") as f:
            other = json.load(f)
        other["_version"] = 5
        with open(temp_anrs / "state.json", "w") as f:
            json.dump(other, f)

        # Try to write - should fail
        with pytest.raises(StateConflictError) as exc:
            manager.write()

        assert exc.value.expected_version == 1
        assert exc.value.actual_version == 5

    def test_force_write(self, temp_anrs):
        """Test force write bypasses version check."""
        manager = StateManager(temp_anrs)
        manager.read()

        # Simulate another process modifying state
        with open(temp_anrs / "state.json") as f:
            other = json.load(f)
        other["_version"] = 5
        with open(temp_anrs / "state.json", "w") as f:
            json.dump(other, f)

        # Force write should succeed
        manager.data["status"] = "forced"
        manager.write(force=True)

        with open(temp_anrs / "state.json") as f:
            saved = json.load(f)
        assert saved["status"] == "forced"

    def test_update_method(self, temp_anrs):
        """Test update method."""
        manager = StateManager(temp_anrs)
        manager.read()
        manager.update({"status": "active", "current_task": "test"})

        assert manager.data["status"] == "active"
        assert manager.data["current_task"] == "test"

    def test_version_auto_init(self, temp_anrs):
        """Test version is auto-initialized if missing."""
        # Remove version from state
        with open(temp_anrs / "state.json") as f:
            data = json.load(f)
        del data["_version"]
        with open(temp_anrs / "state.json", "w") as f:
            json.dump(data, f)

        manager = StateManager(temp_anrs)
        manager.read()
        assert manager.version == 0


class TestAtomicStateUpdate:
    """Tests for atomic_state_update context manager."""

    def test_atomic_update(self, temp_anrs):
        """Test atomic state update."""
        with atomic_state_update(temp_anrs) as state:
            state["status"] = "active"

        with open(temp_anrs / "state.json") as f:
            saved = json.load(f)
        assert saved["status"] == "active"

    def test_atomic_update_exception(self, temp_anrs):
        """Test that exception prevents save."""
        try:
            with atomic_state_update(temp_anrs) as state:
                state["status"] = "should_not_save"
                raise ValueError("Test exception")
        except ValueError:
            pass

        with open(temp_anrs / "state.json") as f:
            saved = json.load(f)
        assert saved["status"] == "idle"  # Unchanged


class TestGetStateVersion:
    """Tests for get_state_version function."""

    def test_get_version(self, temp_anrs):
        """Test getting state version."""
        version = get_state_version(temp_anrs)
        assert version == 1

    def test_get_version_no_file(self, tmp_path):
        """Test getting version when file doesn't exist."""
        version = get_state_version(tmp_path / ".anrs")
        assert version == 0

    def test_get_version_invalid_json(self, temp_anrs):
        """Test getting version from invalid JSON."""
        (temp_anrs / "state.json").write_text("{invalid}")
        version = get_state_version(temp_anrs)
        assert version == 0
