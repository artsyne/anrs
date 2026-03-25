"""ANRS adapter command - Manage AI tool adapters."""

import logging
import shutil
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from anrs.constants import ADAPTERS_DIR, ADAPTERS, get_adapter_config_file
from anrs.backup import (
    ConflictStrategy,
    backup_file,
    get_backup_dir,
    detect_user_modifications,
    prompt_conflict_resolution,
    show_conflict_summary,
    create_backup_id,
)

logger = logging.getLogger(__name__)
console = Console()


@click.group()
def adapter():
    """Manage AI tool adapters.

    Install and configure adapters for different AI tools (Cursor, Claude Code, etc.)
    """
    pass


@adapter.command("list")
def list_adapters():
    """List available adapters."""
    table = Table(title="Available Adapters")
    table.add_column("Adapter", style="cyan")
    table.add_column("Description")
    table.add_column("Config File")

    for name, info in ADAPTERS.items():
        table.add_row(name, info["description"], info["config_file"])

    console.print(table)


@adapter.command("install")
@click.argument("adapter_name", type=click.Choice(list(ADAPTERS.keys())))
@click.option(
    "--force", "-f",
    is_flag=True,
    help="Overwrite existing adapter config (with automatic backup)"
)
@click.option(
    "--skip",
    is_flag=True,
    help="Skip if adapter config already exists"
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Show what would be done without making changes"
)
@click.argument("path", default=".", type=click.Path(exists=True))
def install_adapter(adapter_name: str, force: bool, skip: bool, dry_run: bool, path: str):
    """Install an adapter for an AI tool.

    Creates a trampoline config file that points to .anrs/ENTRY.md.

    \b
    Conflict handling:
    - Default: Asks how to handle existing files
    - --force: Backup existing file, then overwrite
    - --skip: Skip installation if file exists
    """
    target_dir = Path(path).resolve()
    adapter_source = ADAPTERS_DIR / adapter_name

    if not adapter_source.exists():
        raise click.ClickException(f"Adapter not found: {adapter_name}")

    config_file = get_adapter_config_file(adapter_name)
    source_path = adapter_source / config_file
    target_path = target_dir / config_file

    # Detect conflict
    conflict = None
    if target_path.exists():
        has_mods, diff = detect_user_modifications(source_path, target_path)
        conflict = {
            "file": config_file,
            "status": "modified" if has_mods else "unchanged",
            "diff": diff or "",
        }

    if dry_run:
        console.print(
            "[bold yellow]Dry run mode - no changes made[/bold yellow]")
        console.print(f"Would copy: [cyan]{source_path}[/cyan]")
        console.print(f"       to: [cyan]{target_path}[/cyan]")
        if conflict:
            console.print(
                f"\n[yellow]Conflict:[/yellow] {config_file} already exists ({conflict['status']})")
            console.print(
                "[dim]Use --force to backup and overwrite, or --skip to skip[/dim]")
        return

    # Handle conflict
    strategy = ConflictStrategy.BACKUP_AND_OVERWRITE
    if conflict:
        if skip:
            console.print(f"[dim]Skipped: {config_file} already exists[/dim]")
            return
        elif force:
            strategy = ConflictStrategy.BACKUP_AND_OVERWRITE
        else:
            show_conflict_summary(
                [conflict], f"Adapter Config Conflict: {config_file}")
            strategy = prompt_conflict_resolution()

        if strategy == ConflictStrategy.ABORT:
            raise click.Abort()
        elif strategy == ConflictStrategy.SKIP:
            console.print(f"[dim]Skipped: {config_file}[/dim]")
            return

    # Backup if overwriting
    backup_id = create_backup_id()
    if conflict and strategy == ConflictStrategy.BACKUP_AND_OVERWRITE:
        anrs_dir = target_dir / ".anrs"
        backup_dir = get_backup_dir(anrs_dir)
        backup_path = backup_file(target_path, backup_dir, backup_id)
        if backup_path:
            console.print(f"[green]Backed up:[/green] {backup_path}")

    try:
        shutil.copy(source_path, target_path)
    except IOError as e:
        logger.error(f"Failed to install adapter: {e}")
        raise click.ClickException(f"Cannot install adapter: {e}")

    console.print(f"[green]Installed {adapter_name} adapter[/green]")
    console.print(f"Config: [cyan]{target_path}[/cyan]")
    console.print(
        f"\nThe adapter will redirect AI to [cyan].anrs/ENTRY.md[/cyan]")
