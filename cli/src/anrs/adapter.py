"""ANRS adapter command - Manage AI tool adapters."""

import logging
import shutil
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from anrs.constants import ADAPTERS_DIR, ADAPTERS, get_adapter_config_file

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
    help="Overwrite existing adapter config"
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Show what would be done without making changes"
)
@click.argument("path", default=".", type=click.Path(exists=True))
def install_adapter(adapter_name: str, force: bool, dry_run: bool, path: str):
    """Install an adapter for an AI tool.

    Creates a trampoline config file that points to .anrs/ENTRY.md
    """
    target_dir = Path(path).resolve()
    adapter_source = ADAPTERS_DIR / adapter_name

    if not adapter_source.exists():
        raise click.ClickException(f"Adapter not found: {adapter_name}")

    config_file = get_adapter_config_file(adapter_name)
    source_path = adapter_source / config_file
    target_path = target_dir / config_file

    if target_path.exists() and not force:
        raise click.ClickException(
            f"{config_file} already exists. Use --force to overwrite."
        )

    if dry_run:
        console.print(
            "[bold yellow]Dry run mode - no changes made[/bold yellow]")
        console.print(f"Would copy: [cyan]{source_path}[/cyan]")
        console.print(f"       to: [cyan]{target_path}[/cyan]")
        return

    try:
        shutil.copy(source_path, target_path)
    except IOError as e:
        logger.error(f"Failed to install adapter: {e}")
        raise click.ClickException(f"Cannot install adapter: {e}")

    console.print(f"[green]Installed {adapter_name} adapter[/green]")
    console.print(f"Config: [cyan]{target_path}[/cyan]")
    console.print(
        f"\nThe adapter will redirect AI to [cyan].anrs/ENTRY.md[/cyan]")
