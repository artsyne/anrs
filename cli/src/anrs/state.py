"""ANRS state management with optimistic concurrency control.

Provides safe read/write operations for state.json with version-based
conflict detection to prevent concurrent modification issues.

Usage:
    from anrs.state import StateManager

    with StateManager(anrs_dir) as state:
        state.data["status"] = "active"
        state.data["current_task"] = "task-001"
    # Automatically saves with version check
"""

import json
import logging
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Generator, Optional

logger = logging.getLogger(__name__)


class StateConflictError(Exception):
    """Raised when state has been modified by another process."""

    def __init__(self, expected_version: int, actual_version: int):
        self.expected_version = expected_version
        self.actual_version = actual_version
        super().__init__(
            f"State conflict: expected version {expected_version}, "
            f"but found version {actual_version}. "
            f"Another process may have modified the state."
        )


class StateManager:
    """Manages state.json with optimistic concurrency control.

    Uses a version number to detect concurrent modifications.
    If the state was modified by another process between read and write,
    a StateConflictError is raised.

    Attributes:
        path: Path to state.json
        data: Current state data (available after read)
        version: Current version number
    """

    def __init__(self, anrs_dir: Path):
        """Initialize state manager.

        Args:
            anrs_dir: Path to .anrs directory
        """
        self.path = anrs_dir / "state.json"
        self.data: Dict[str, Any] = {}
        self._original_version: Optional[int] = None

    @property
    def version(self) -> int:
        """Get current version number."""
        return self.data.get("_version", 0)

    def read(self) -> Dict[str, Any]:
        """Read state from file.

        Returns:
            Current state data

        Raises:
            FileNotFoundError: If state.json doesn't exist
            json.JSONDecodeError: If state.json is invalid
        """
        with open(self.path) as f:
            self.data = json.load(f)

        # Ensure version field exists
        if "_version" not in self.data:
            self.data["_version"] = 0

        self._original_version = self.data["_version"]
        return self.data

    def write(self, force: bool = False) -> None:
        """Write state to file with version check.

        Args:
            force: If True, skip version check (use with caution)

        Raises:
            StateConflictError: If state was modified by another process
        """
        if not force and self._original_version is not None:
            # Re-read to check version
            try:
                with open(self.path) as f:
                    current = json.load(f)
                current_version = current.get("_version", 0)

                if current_version != self._original_version:
                    raise StateConflictError(
                        self._original_version, current_version
                    )
            except FileNotFoundError:
                pass  # File was deleted, proceed with write

        # Increment version
        self.data["_version"] = self.version + 1

        # Update timestamp
        if "metadata" in self.data:
            self.data["metadata"]["updated_at"] = datetime.now().isoformat()

        # Write atomically (write to temp, then rename)
        temp_path = self.path.with_suffix(".json.tmp")
        try:
            with open(temp_path, "w") as f:
                json.dump(self.data, f, indent=2)
            temp_path.replace(self.path)
        except Exception:
            if temp_path.exists():
                temp_path.unlink()
            raise

        self._original_version = self.data["_version"]

    def update(self, updates: Dict[str, Any]) -> None:
        """Update state fields.

        Args:
            updates: Dictionary of fields to update
        """
        self.data.update(updates)

    def __enter__(self) -> "StateManager":
        """Context manager entry - read state."""
        self.read()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit - write state if no exception."""
        if exc_type is None:
            self.write()


@contextmanager
def atomic_state_update(
    anrs_dir: Path,
    max_retries: int = 3
) -> Generator[Dict[str, Any], None, None]:
    """Context manager for atomic state updates with retry.

    Automatically retries on conflict up to max_retries times.

    Args:
        anrs_dir: Path to .anrs directory
        max_retries: Maximum retry attempts on conflict

    Yields:
        State data dictionary

    Raises:
        StateConflictError: If all retries exhausted

    Example:
        with atomic_state_update(anrs_dir) as state:
            state["status"] = "active"
    """
    manager = StateManager(anrs_dir)

    for attempt in range(max_retries):
        try:
            manager.read()
            yield manager.data
            manager.write()
            return
        except StateConflictError:
            if attempt == max_retries - 1:
                raise
            logger.warning(
                f"State conflict, retrying (attempt {attempt + 2}/{max_retries})"
            )
            continue


def get_state_version(anrs_dir: Path) -> int:
    """Get current state version without full read.

    Args:
        anrs_dir: Path to .anrs directory

    Returns:
        Current version number, or 0 if not found
    """
    state_path = anrs_dir / "state.json"
    try:
        with open(state_path) as f:
            data = json.load(f)
        return data.get("_version", 0)
    except (FileNotFoundError, json.JSONDecodeError):
        return 0
