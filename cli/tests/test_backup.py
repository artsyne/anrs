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
