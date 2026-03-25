"""ANRS backup and restore utilities.

Provides a unified backup mechanism for all CLI write operations.
Ensures user data is never lost during init, upgrade, or adapter operations.

Design principles:
1. Never lose user data - always backup before destructive operations
2. Make conflicts visible - show what will be changed
3. Offer choices - merge, overwrite, skip, or abort
4. Enable rollback - restore from any backup
"""

import json
import logging
import shutil
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

logger = logging.getLogger(__name__)
console = Console()


class ConflictStrategy(Enum):
    """Strategy for handling file conflicts."""
    BACKUP_AND_OVERWRITE = "backup"  # Backup existing, then overwrite
    MERGE = "merge"                   # Smart merge (for JSON files)
    SKIP = "skip"                     # Skip if exists
    ABORT = "abort"                   # Abort operation


# Backup directory location
BACKUP_DIR_NAME = ".backups"


def get_backup_dir(anrs_dir: Path) -> Path:
    """Get the backup directory path."""
    return anrs_dir / BACKUP_DIR_NAME


def create_backup_id() -> str:
    """Create a unique backup ID based on timestamp."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def backup_file(
    file_path: Path,
    backup_dir: Path,
    backup_id: Optional[str] = None
) -> Optional[Path]:
    """Backup a single file.

    Args:
        file_path: Path to the file to backup
        backup_dir: Directory to store backups
        backup_id: Optional backup ID (auto-generated if not provided)

    Returns:
        Path to the backup file, or None if file doesn't exist
    """
    if not file_path.exists():
        return None

    backup_id = backup_id or create_backup_id()
    backup_dir.mkdir(parents=True, exist_ok=True)

    # Create backup filename with timestamp
    backup_name = f"{file_path.name}.{backup_id}"
    backup_path = backup_dir / backup_name

    try:
        shutil.copy2(file_path, backup_path)
        logger.info(f"Backed up {file_path} to {backup_path}")
        return backup_path
    except IOError as e:
        logger.error(f"Failed to backup {file_path}: {e}")
        return None


def backup_directory(
    dir_path: Path,
    backup_dir: Path,
    backup_id: Optional[str] = None
) -> Optional[Path]:
    """Backup an entire directory.

    Args:
        dir_path: Path to the directory to backup
        backup_dir: Directory to store backups
        backup_id: Optional backup ID (auto-generated if not provided)

    Returns:
        Path to the backup directory, or None if directory doesn't exist
    """
    if not dir_path.exists():
        return None

    backup_id = backup_id or create_backup_id()
    backup_dir.mkdir(parents=True, exist_ok=True)

    # Create backup directory name with timestamp
    backup_name = f"{dir_path.name}.{backup_id}"
    backup_path = backup_dir / backup_name

    try:
        shutil.copytree(dir_path, backup_path)
        logger.info(f"Backed up {dir_path} to {backup_path}")
        return backup_path
    except IOError as e:
        logger.error(f"Failed to backup {dir_path}: {e}")
        return None


def list_backups(backup_dir: Path) -> List[Dict]:
    """List all available backups.

    Returns:
        List of backup info dicts with 'name', 'path', 'timestamp', 'size'
    """
    if not backup_dir.exists():
        return []

    backups = []
    for item in backup_dir.iterdir():
        # Parse backup ID from filename (name.YYYYMMDD_HHMMSS)
        parts = item.name.rsplit(".", 1)
        if len(parts) == 2:
            name, timestamp = parts
            try:
                dt = datetime.strptime(timestamp, "%Y%m%d_%H%M%S")
                size = sum(f.stat().st_size for f in item.rglob(
                    "*") if f.is_file()) if item.is_dir() else item.stat().st_size
                backups.append({
                    "name": name,
                    "path": item,
                    "timestamp": dt,
                    "size": size,
                    "is_dir": item.is_dir()
                })
            except ValueError:
                continue

    # Sort by timestamp descending (newest first)
    backups.sort(key=lambda x: x["timestamp"], reverse=True)
    return backups


def restore_backup(backup_path: Path, target_path: Path) -> bool:
    """Restore a file or directory from backup.

    Args:
        backup_path: Path to the backup file/directory
        target_path: Path to restore to

    Returns:
        True if successful, False otherwise
    """
    if not backup_path.exists():
        logger.error(f"Backup not found: {backup_path}")
        return False

    try:
        if backup_path.is_dir():
            if target_path.exists():
                shutil.rmtree(target_path)
            shutil.copytree(backup_path, target_path)
        else:
            shutil.copy2(backup_path, target_path)

        logger.info(f"Restored {backup_path} to {target_path}")
        return True
    except IOError as e:
        logger.error(f"Failed to restore {backup_path}: {e}")
        return False


def merge_json_files(
    source: Path,
    target: Path,
    preserve_keys: Optional[List[str]] = None
) -> Dict:
    """Merge two JSON files, preserving user data.

    Strategy:
    - Template values are used as base
    - User values in preserve_keys are kept
    - New keys from template are added

    Args:
        source: Path to template/new JSON file
        target: Path to existing user JSON file
        preserve_keys: List of top-level keys to preserve from target

    Returns:
        Merged dictionary
    """
    preserve_keys = preserve_keys or []

    try:
        with open(source) as f:
            source_data = json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        logger.error(f"Failed to read source JSON: {e}")
        return {}

    if not target.exists():
        return source_data

    try:
        with open(target) as f:
            target_data = json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        logger.warning(f"Failed to read target JSON, using source: {e}")
        return source_data

    # Start with source (template) as base
    merged = source_data.copy()

    # Preserve specified keys from target (user data)
    for key in preserve_keys:
        if key in target_data:
            merged[key] = target_data[key]

    # Deep merge: keep user's nested values where they exist
    def deep_merge(base: Dict, override: Dict) -> Dict:
        """Recursively merge override into base."""
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = deep_merge(result[key], value)
            elif key in result and result[key] != value:
                # User has customized this value, preserve it
                result[key] = value
        return result

    # For non-preserved keys, do deep merge to keep user customizations
    for key in target_data:
        if key not in preserve_keys:
            if key in merged and isinstance(merged[key], dict) and isinstance(target_data[key], dict):
                merged[key] = deep_merge(merged[key], target_data[key])

    return merged


def detect_user_modifications(
    template_path: Path,
    user_path: Path
) -> Tuple[bool, Optional[str]]:
    """Detect if user has modified a file from the template.

    Args:
        template_path: Path to original template file
        user_path: Path to user's file

    Returns:
        Tuple of (has_modifications, diff_summary)
    """
    if not user_path.exists():
        return False, None

    if not template_path.exists():
        return True, "No template to compare"

    try:
        template_content = template_path.read_text()
        user_content = user_path.read_text()

        if template_content == user_content:
            return False, None

        # Count differences
        template_lines = set(template_content.splitlines())
        user_lines = set(user_content.splitlines())

        added = len(user_lines - template_lines)
        removed = len(template_lines - user_lines)

        return True, f"+{added}/-{removed} lines"
    except IOError:
        return False, None


def show_conflict_summary(
    conflicts: List[Dict],
    title: str = "File Conflicts Detected"
) -> None:
    """Display a summary of file conflicts.

    Args:
        conflicts: List of conflict dicts with 'file', 'status', 'diff'
    """
    table = Table(title=title)
    table.add_column("File", style="cyan")
    table.add_column("Status", style="yellow")
    table.add_column("Changes")

    for conflict in conflicts:
        table.add_row(
            str(conflict["file"]),
            conflict["status"],
            conflict.get("diff", "")
        )

    console.print(table)


def prompt_conflict_resolution() -> ConflictStrategy:
    """Prompt user to choose how to handle conflicts.

    Returns:
        Selected ConflictStrategy
    """
    console.print(
        "\n[bold]How would you like to handle these conflicts?[/bold]")
    console.print(
        "  [cyan]b[/cyan] - Backup existing files and overwrite (recommended)")
    console.print(
        "  [cyan]m[/cyan] - Merge (keep user customizations where possible)")
    console.print("  [cyan]s[/cyan] - Skip existing files")
    console.print("  [cyan]a[/cyan] - Abort operation")

    while True:
        choice = console.input(
            "\n[bold]Your choice [b/m/s/a]:[/bold] ").strip().lower()
        if choice == "b":
            return ConflictStrategy.BACKUP_AND_OVERWRITE
        elif choice == "m":
            return ConflictStrategy.MERGE
        elif choice == "s":
            return ConflictStrategy.SKIP
        elif choice == "a":
            return ConflictStrategy.ABORT
        else:
            console.print(
                "[red]Invalid choice. Please enter b, m, s, or a.[/red]")


def format_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def show_backup_list(backup_dir: Path) -> None:
    """Display list of available backups."""
    backups = list_backups(backup_dir)

    if not backups:
        console.print("[dim]No backups found[/dim]")
        return

    table = Table(title="Available Backups")
    table.add_column("Name", style="cyan")
    table.add_column("Timestamp")
    table.add_column("Size")
    table.add_column("Type")

    for backup in backups:
        table.add_row(
            backup["name"],
            backup["timestamp"].strftime("%Y-%m-%d %H:%M:%S"),
            format_size(backup["size"]),
            "dir" if backup["is_dir"] else "file"
        )

    console.print(table)
