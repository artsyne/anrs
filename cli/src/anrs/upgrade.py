"""ANRS upgrade command - Upgrade .anrs/ to latest version."""

import json
import logging
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from anrs.constants import TEMPLATES_DIR, PRESERVE_FIELDS

logger = logging.getLogger(__name__)
console = Console()


def get_current_version(anrs_dir: Path) -> Optional[str]:
    """Get current ANRS version from config."""
    config_path = anrs_dir / "config.json"
    if config_path.exists():
        try:
            with open(config_path) as f:
                config = json.load(f)
            return config.get("version", "unknown")
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Failed to read config: {e}")
            return "unknown"
    return None


def backup_state(anrs_dir: Path, backup_dir: Path) -> None:
    """Backup state files before upgrade."""
    state_file = anrs_dir / "state.json"
    if state_file.exists():
        try:
            backup_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = backup_dir / f"state_{timestamp}.json"
            shutil.copy(state_file, backup_path)
            console.print(f"[dim]Backed up state to {backup_path}[/dim]")
        except IOError as e:
            logger.warning(f"Failed to backup state: {e}")
            console.print(f"[yellow]Warning: Could not backup state: {e}[/yellow]")


def upgrade_file(source: Path, target: Path, preserve_data: bool = False) -> bool:
    """Upgrade a single file, optionally preserving user data."""
    if not source.exists():
        return False

    if preserve_data and target.exists():
        # For JSON files, merge preserving user data
        if target.suffix == ".json":
            try:
                with open(target) as f:
                    user_data = json.load(f)
                with open(source) as f:
                    template_data = json.load(f)

                # Preserve user-specific fields
                for field in PRESERVE_FIELDS:
                    if field in user_data:
                        template_data[field] = user_data[field]

                # Update metadata
                if "metadata" in template_data:
                    template_data["metadata"]["updated_at"] = datetime.now().isoformat()

                with open(target, "w") as f:
                    json.dump(template_data, f, indent=2)
                return True
            except (json.JSONDecodeError, KeyError) as e:
                logger.warning(f"Failed to merge JSON, overwriting: {e}")
            except IOError as e:
                logger.error(f"Failed to upgrade file: {e}")
                return False

    # Default: overwrite
    try:
        shutil.copy(source, target)
        return True
    except IOError as e:
        logger.error(f"Failed to copy file: {e}")
        return False


@click.command()
@click.option(
    "--dry-run",
    is_flag=True,
    help="Show what would be upgraded without making changes"
)
@click.option(
    "--force", "-f",
    is_flag=True,
    help="Force upgrade even if versions match"
)
@click.option(
    "--no-backup",
    is_flag=True,
    help="Skip backing up state files"
)
@click.argument("path", default=".", type=click.Path(exists=True))
def upgrade(dry_run: bool, force: bool, no_backup: bool, path: str):
    """Upgrade .anrs/ directory to latest ANRS version.

    This command updates the ANRS protocol files while preserving:
    - Current state (task, status)
    - Project configuration
    - Custom skills (if any)

    State files are backed up before upgrade.
    """
    target_dir = Path(path).resolve()
    anrs_dir = target_dir / ".anrs"

    if not anrs_dir.exists():
        raise click.ClickException(
            f"Not an ANRS repository: {target_dir}\n"
            f"Run 'anrs init' first."
        )

    # Get current version
    current_version = get_current_version(anrs_dir)

    # Get template version
    template_config = TEMPLATES_DIR / "files" / "config.json"
    if template_config.exists():
        with open(template_config) as f:
            new_version = json.load(f).get("version", "0.1")
    else:
        new_version = "0.1"

    if current_version == new_version and not force:
        console.print(Panel(
            f"[green]Already up to date[/green]\n\n"
            f"Current version: [cyan]{current_version}[/cyan]",
            title="ANRS Upgrade"
        ))
        return

    # Files to upgrade
    upgrade_files = [
        ("ENTRY.md", False),           # Protocol file, always update
        ("config.json", True),         # Preserve project settings
        ("state.json", True),          # Preserve state data (with backup)
    ]

    if dry_run:
        console.print(Panel(
            f"[bold]Dry run[/bold] - would upgrade:\n"
            f"[cyan]{anrs_dir}[/cyan]\n\n"
            f"From: [yellow]{current_version}[/yellow]\n"
            f"To:   [green]{new_version}[/green]",
            title="ANRS Upgrade"
        ))

        table = Table(title="Files to Upgrade")
        table.add_column("File", style="cyan")
        table.add_column("Action")

        for filename, preserve in upgrade_files:
            source = TEMPLATES_DIR / "files" / filename
            target = anrs_dir / filename
            if source.exists():
                action = "[yellow]Update (preserve data)[/yellow]" if preserve else "[green]Replace[/green]"
                if not target.exists():
                    action = "[green]Create[/green]"
                table.add_row(filename, action)

        console.print(table)
        return

    # Backup state
    if not no_backup:
        backup_dir = anrs_dir / ".backups"
        backup_state(anrs_dir, backup_dir)

    # Perform upgrade
    upgraded = []
    for filename, preserve in upgrade_files:
        source = TEMPLATES_DIR / "files" / filename
        target = anrs_dir / filename

        if upgrade_file(source, target, preserve):
            upgraded.append(filename)

    # Update version in config
    config_path = anrs_dir / "config.json"
    if config_path.exists():
        with open(config_path) as f:
            config = json.load(f)
        config["version"] = new_version
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)

    console.print(Panel(
        f"[bold green]Upgrade complete![/bold green]\n\n"
        f"From: [yellow]{current_version}[/yellow]\n"
        f"To:   [green]{new_version}[/green]\n\n"
        f"Updated files:\n" + "\n".join(f"  - {f}" for f in upgraded),
        title="ANRS Upgrade"
    ))
