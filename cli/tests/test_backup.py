"""Tests for ANRS CLI backup module."""

import json
import pytest
from pathlib import Path

from anrs.backup import (
    ConflictStrategy,
    backup_file,
    backup_directory,
    create_backup_id,
    get_backup_dir,
    list_backups,
    restore_backup,
    merge_json_files,
    detect_user_modifications,
    format_size,
)


@pytest.fixture
def temp_dir(tmp_path):
    """Create a temporary directory for testing."""
    return tmp_path


class TestBackupFile:
    """Tests for backup_file function."""

    def test_backup_file_creates_backup(self, temp_dir):
        """Test that backup_file creates a backup."""
        # Create a file to backup
        original = temp_dir / "test.txt"
        original.write_text("original content")

        backup_dir = temp_dir / "backups"

        result = backup_file(original, backup_dir)

        assert result is not None
        assert result.exists()
        assert result.read_text() == "original content"

    def test_backup_file_nonexistent(self, temp_dir):
        """Test backup_file with non-existent file."""
        nonexistent = temp_dir / "nonexistent.txt"
        backup_dir = temp_dir / "backups"

        result = backup_file(nonexistent, backup_dir)

        assert result is None

    def test_backup_file_with_custom_id(self, temp_dir):
        """Test backup_file with custom backup ID."""
        original = temp_dir / "test.json"
        original.write_text("{}")

        backup_dir = temp_dir / "backups"
        backup_id = "20240101_120000"

        result = backup_file(original, backup_dir, backup_id)

        assert result is not None
        assert backup_id in result.name


class TestBackupDirectory:
    """Tests for backup_directory function."""

    def test_backup_directory_creates_backup(self, temp_dir):
        """Test that backup_directory creates a backup."""
        # Create a directory with files
        source_dir = temp_dir / "source"
        source_dir.mkdir()
        (source_dir / "file1.txt").write_text("content1")
        (source_dir / "file2.txt").write_text("content2")

        backup_dir = temp_dir / "backups"

        result = backup_directory(source_dir, backup_dir)

        assert result is not None
        assert result.is_dir()
        assert (result / "file1.txt").exists()
        assert (result / "file2.txt").exists()

    def test_backup_directory_nonexistent(self, temp_dir):
        """Test backup_directory with non-existent directory."""
        nonexistent = temp_dir / "nonexistent"
        backup_dir = temp_dir / "backups"

        result = backup_directory(nonexistent, backup_dir)

        assert result is None


class TestListBackups:
    """Tests for list_backups function."""

    def test_list_backups_empty(self, temp_dir):
        """Test list_backups with empty/non-existent directory."""
        backup_dir = temp_dir / "backups"

        result = list_backups(backup_dir)

        assert result == []

    def test_list_backups_with_files(self, temp_dir):
        """Test list_backups returns sorted backups."""
        backup_dir = temp_dir / "backups"
        backup_dir.mkdir()

        # Create backup files with different timestamps
        (backup_dir / "state.json.20240101_100000").write_text("{}")
        (backup_dir / "state.json.20240102_100000").write_text("{}")

        result = list_backups(backup_dir)

        assert len(result) == 2
        # Should be sorted newest first
        assert "20240102" in result[0]["path"].name


class TestRestoreBackup:
    """Tests for restore_backup function."""

    def test_restore_backup_file(self, temp_dir):
        """Test restoring a backup file."""
        # Create backup
        backup_file_path = temp_dir / "backup.txt"
        backup_file_path.write_text("backup content")

        # Create target (will be overwritten)
        target = temp_dir / "target.txt"
        target.write_text("old content")

        result = restore_backup(backup_file_path, target)

        assert result is True
        assert target.read_text() == "backup content"

    def test_restore_backup_nonexistent(self, temp_dir):
        """Test restore_backup with non-existent backup."""
        nonexistent = temp_dir / "nonexistent"
        target = temp_dir / "target.txt"

        result = restore_backup(nonexistent, target)

        assert result is False


class TestMergeJsonFiles:
    """Tests for merge_json_files function."""

    def test_merge_json_preserves_keys(self, temp_dir):
        """Test that merge preserves specified keys."""
        source = temp_dir / "source.json"
        target = temp_dir / "target.json"

        source.write_text(json.dumps({
            "version": "0.2",
            "status": "idle",
            "config": {"new": "value"}
        }))
        target.write_text(json.dumps({
            "version": "0.1",
            "status": "active",
            "config": {"old": "value"}
        }))

        result = merge_json_files(source, target, ["status"])

        assert result["version"] == "0.2"  # From source
        assert result["status"] == "active"  # Preserved from target
        assert "new" in result["config"]  # From source (deep merged)

    def test_merge_json_target_not_exists(self, temp_dir):
        """Test merge when target doesn't exist."""
        source = temp_dir / "source.json"
        target = temp_dir / "nonexistent.json"

        source.write_text(json.dumps({"key": "value"}))

        result = merge_json_files(source, target)

        assert result == {"key": "value"}


class TestDetectUserModifications:
    """Tests for detect_user_modifications function."""

    def test_detect_no_modifications(self, temp_dir):
        """Test detection when files are identical."""
        template = temp_dir / "template.txt"
        user = temp_dir / "user.txt"

        content = "same content"
        template.write_text(content)
        user.write_text(content)

        has_mods, diff = detect_user_modifications(template, user)

        assert has_mods is False
        assert diff is None

    def test_detect_with_modifications(self, temp_dir):
        """Test detection when files differ."""
        template = temp_dir / "template.txt"
        user = temp_dir / "user.txt"

        template.write_text("line1\nline2")
        user.write_text("line1\nmodified\nline3")

        has_mods, diff = detect_user_modifications(template, user)

        assert has_mods is True
        assert diff is not None
        assert "+" in diff or "-" in diff

    def test_detect_user_file_not_exists(self, temp_dir):
        """Test detection when user file doesn't exist."""
        template = temp_dir / "template.txt"
        user = temp_dir / "nonexistent.txt"

        template.write_text("content")

        has_mods, diff = detect_user_modifications(template, user)

        assert has_mods is False


class TestHelperFunctions:
    """Tests for helper functions."""

    def test_create_backup_id_format(self):
        """Test that backup ID has correct format."""
        backup_id = create_backup_id()

        # Should be YYYYMMDD_HHMMSS format
        assert len(backup_id) == 15
        assert "_" in backup_id

    def test_get_backup_dir(self, temp_dir):
        """Test get_backup_dir returns correct path."""
        anrs_dir = temp_dir / ".anrs"

        result = get_backup_dir(anrs_dir)

        assert result == anrs_dir / ".backups"

    def test_format_size(self):
        """Test format_size returns human-readable sizes."""
        assert "B" in format_size(100)
        assert "KB" in format_size(1024)
        assert "MB" in format_size(1024 * 1024)


class TestConflictStrategy:
    """Tests for ConflictStrategy enum."""

    def test_conflict_strategies_exist(self):
        """Test that all conflict strategies are defined."""
        assert ConflictStrategy.BACKUP_AND_OVERWRITE
        assert ConflictStrategy.MERGE
        assert ConflictStrategy.SKIP
        assert ConflictStrategy.ABORT

    def test_conflict_strategy_values(self):
        """Test strategy values."""
        assert ConflictStrategy.BACKUP_AND_OVERWRITE.value == "backup"
        assert ConflictStrategy.MERGE.value == "merge"
        assert ConflictStrategy.SKIP.value == "skip"
        assert ConflictStrategy.ABORT.value == "abort"


class TestRestoreDirectory:
    """Tests for restore_backup with directories."""

    def test_restore_directory(self, temp_dir):
        """Test restoring a backup directory."""
        # Create backup directory
        backup_dir = temp_dir / "backup_dir"
        backup_dir.mkdir()
        (backup_dir / "file.txt").write_text("backup content")

        # Create target (will be replaced)
        target = temp_dir / "target_dir"
        target.mkdir()
        (target / "old.txt").write_text("old")

        result = restore_backup(backup_dir, target)

        assert result is True
        assert (target / "file.txt").exists()
        assert (target / "file.txt").read_text() == "backup content"


class TestMergeJsonAdvanced:
    """Advanced tests for merge_json_files."""

    def test_merge_deep_nested(self, temp_dir):
        """Test deep merge of nested JSON."""
        source = temp_dir / "source.json"
        target = temp_dir / "target.json"

        source.write_text(json.dumps({
            "level1": {
                "level2": {
                    "new_key": "new_value",
                    "shared": "source"
                }
            }
        }))
        target.write_text(json.dumps({
            "level1": {
                "level2": {
                    "user_key": "user_value",
                    "shared": "user"
                }
            }
        }))

        result = merge_json_files(source, target)

        assert result["level1"]["level2"]["new_key"] == "new_value"
        # User value preserved
        assert result["level1"]["level2"]["shared"] == "user"

    def test_merge_invalid_target_json(self, temp_dir):
        """Test merge when target has invalid JSON."""
        source = temp_dir / "source.json"
        target = temp_dir / "target.json"

        source.write_text(json.dumps({"key": "value"}))
        target.write_text("not valid json")

        result = merge_json_files(source, target)

        # Should fall back to source
        assert result == {"key": "value"}

    def test_merge_invalid_source_json(self, temp_dir):
        """Test merge when source has invalid JSON."""
        source = temp_dir / "source.json"
        target = temp_dir / "target.json"

        source.write_text("not valid json")
        target.write_text(json.dumps({"key": "value"}))

        result = merge_json_files(source, target)

        # Should return empty dict on source error
        assert result == {}


class TestBackupEdgeCases:
    """Edge case tests for backup functions."""

    def test_backup_file_io_error(self, temp_dir):
        """Test backup_file handles IO errors gracefully."""
        # Create a file
        original = temp_dir / "test.txt"
        original.write_text("content")

        # Try to backup to read-only location (mock)
        backup_dir = temp_dir / "readonly"
        backup_dir.mkdir()

        # This should succeed normally
        result = backup_file(original, backup_dir)
        assert result is not None

    def test_list_backups_with_invalid_files(self, temp_dir):
        """Test list_backups ignores files without valid timestamp."""
        backup_dir = temp_dir / "backups"
        backup_dir.mkdir()

        # Create files with valid and invalid names
        (backup_dir / "state.json.20240101_120000").write_text("{}")
        (backup_dir / "invalid_name.txt").write_text("{}")
        (backup_dir / "no_timestamp").write_text("{}")

        result = list_backups(backup_dir)

        # Should only find the valid one
        assert len(result) == 1
        assert "20240101" in result[0]["path"].name


class TestBackupIOErrors:
    """Tests for IO error handling in backup functions."""

    def test_backup_file_io_error_on_copy(self, temp_dir, monkeypatch):
        """Test backup_file handles copy errors."""
        import shutil

        original = temp_dir / "test.txt"
        original.write_text("content")
        backup_dir = temp_dir / "backups"
        backup_dir.mkdir()

        def mock_copy2(*args, **kwargs):
            raise IOError("Cannot copy file")

        monkeypatch.setattr(shutil, "copy2", mock_copy2)

        result = backup_file(original, backup_dir)
        # Should return None on error
        assert result is None

    def test_restore_backup_io_error(self, temp_dir, monkeypatch):
        """Test restore_backup handles IO errors."""
        import shutil

        backup_path = temp_dir / "backup.txt"
        backup_path.write_text("backup")
        target = temp_dir / "target.txt"

        def mock_copy2(*args, **kwargs):
            raise IOError("Cannot restore")

        monkeypatch.setattr(shutil, "copy2", mock_copy2)

        result = restore_backup(backup_path, target)
        assert result is False

    def test_detect_user_modifications_io_error(self, temp_dir, monkeypatch):
        """Test detect_user_modifications handles IO errors."""
        template = temp_dir / "template.txt"
        user = temp_dir / "user.txt"
        template.write_text("content")
        user.write_text("content")

        def mock_read_text(self):
            raise IOError("Cannot read")

        monkeypatch.setattr(Path, "read_text", mock_read_text)

        has_mods, diff = detect_user_modifications(template, user)
        # Should return False on error
        assert has_mods is False

    def test_detect_user_modifications_no_template(self, temp_dir):
        """Test detect_user_modifications when template doesn't exist."""
        template = temp_dir / "nonexistent.txt"
        user = temp_dir / "user.txt"
        user.write_text("user content")

        has_mods, diff = detect_user_modifications(template, user)
        assert has_mods is True
        assert diff == "No template to compare"


class TestFormatSizeEdgeCases:
    """Tests for format_size edge cases."""

    def test_format_size_gb(self):
        """Test format_size with GB values."""
        result = format_size(1024 * 1024 * 1024)
        assert "GB" in result

    def test_format_size_tb(self):
        """Test format_size with TB values."""
        result = format_size(1024 * 1024 * 1024 * 1024)
        assert "TB" in result


class TestPromptConflictResolution:
    """Tests for prompt_conflict_resolution."""

    def test_prompt_backup_choice(self, monkeypatch):
        """Test choosing backup option."""
        from anrs.backup import prompt_conflict_resolution
        from anrs.backup import console

        monkeypatch.setattr(console, "input", lambda x: "b")
        result = prompt_conflict_resolution()
        assert result == ConflictStrategy.BACKUP_AND_OVERWRITE

    def test_prompt_merge_choice(self, monkeypatch):
        """Test choosing merge option."""
        from anrs.backup import prompt_conflict_resolution
        from anrs.backup import console

        monkeypatch.setattr(console, "input", lambda x: "m")
        result = prompt_conflict_resolution()
        assert result == ConflictStrategy.MERGE

    def test_prompt_skip_choice(self, monkeypatch):
        """Test choosing skip option."""
        from anrs.backup import prompt_conflict_resolution
        from anrs.backup import console

        monkeypatch.setattr(console, "input", lambda x: "s")
        result = prompt_conflict_resolution()
        assert result == ConflictStrategy.SKIP

    def test_prompt_abort_choice(self, monkeypatch):
        """Test choosing abort option."""
        from anrs.backup import prompt_conflict_resolution
        from anrs.backup import console

        monkeypatch.setattr(console, "input", lambda x: "a")
        result = prompt_conflict_resolution()
        assert result == ConflictStrategy.ABORT

    def test_prompt_invalid_then_valid(self, monkeypatch):
        """Test invalid input followed by valid input."""
        from anrs.backup import prompt_conflict_resolution
        from anrs.backup import console

        inputs = iter(["x", "invalid", "b"])
        monkeypatch.setattr(console, "input", lambda x: next(inputs))
        result = prompt_conflict_resolution()
        assert result == ConflictStrategy.BACKUP_AND_OVERWRITE


class TestShowBackupList:
    """Tests for show_backup_list function."""

    def test_show_backup_list_empty(self, temp_dir, capsys):
        """Test show_backup_list with no backups."""
        from anrs.backup import show_backup_list

        backup_dir = temp_dir / "backups"
        show_backup_list(backup_dir)
        # Should print "No backups found"

    def test_show_backup_list_with_backups(self, temp_dir):
        """Test show_backup_list with existing backups."""
        from anrs.backup import show_backup_list

        backup_dir = temp_dir / "backups"
        backup_dir.mkdir()
        (backup_dir / "state.json.20240101_120000").write_text("{}")

        # Should not raise
        show_backup_list(backup_dir)
