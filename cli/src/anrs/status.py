"""ANRS status command - Show repository status."""

import json
import logging
from pathlib import Path
from typing import Tuple

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

logger = logging.getLogger(__name__)
console = Console()


def check_file(path: Path) -> Tuple[bool, str]:
    """Check if file exists and return status."""
    if path.exists():
        return True, "[green]\u2713[/green]"
    return False, "[red]\u2717[/red]"


def check_dir(path: Path) -> Tuple[bool, str]:
    """Check if directory exists and return status."""
    if path.is_dir():
        return True, "[green]\u2713[/green]"
    return False, "[red]\u2717[/red]"


@click.command()
@click.argument("path", default=".", type=click.Path(exists=True))
def status(path: str):
    """Show ANRS status for a repository.

    Checks if the repository is ANRS-compliant and shows current state.
    """
    target_dir = Path(path).resolve()
    anrs_dir = target_dir / ".anrs"

    if not anrs_dir.exists():
        console.print(Panel(
            f"[yellow]Not an ANRS repository[/yellow]\n\n"
            f"Run [cyan]anrs init[/cyan] to initialize.",
            title="ANRS Status"
        ))
        return

    # Check structure
    table = Table(title="ANRS Structure")
    table.add_column("Component", style="cyan")
    table.add_column("Status")
    table.add_column("Path")

    checks = [
        ("ENTRY", check_file(anrs_dir / "ENTRY.md"), ".anrs/ENTRY.md"),
        ("State", check_file(anrs_dir / "state.json"), ".anrs/state.json"),
        ("Config", check_file(anrs_dir / "config.json"), ".anrs/config.json"),
        ("Scratchpad", check_file(anrs_dir / "scratchpad.md"), ".anrs/scratchpad.md"),
        ("Plans", check_dir(anrs_dir / "plans"), ".anrs/plans/"),
        ("Skills", check_dir(anrs_dir / "skills"), ".anrs/skills/"),
        ("Harness", check_dir(anrs_dir / "harness"), ".anrs/harness/ (Level 2)"),
    ]

    for name, (exists, status_icon), filepath in checks:
        table.add_row(name, status_icon, filepath)

    console.print(table)

    # Show state if exists
    state_path = anrs_dir / "state.json"
    if state_path.exists():
        try:
            with open(state_path) as f:
                state = json.load(f)

            console.print("\n")
            state_table = Table(title="Current State")
            state_table.add_column("Field", style="cyan")
            state_table.add_column("Value")

            state_table.add_row("Status", state.get("status", "unknown"))
            state_table.add_row("Current Task", state.get(
                "current_task") or "[dim]none[/dim]")
            state_table.add_row("Last Completed", state.get(
                "last_completed") or "[dim]none[/dim]")

            console.print(state_table)
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse state.json: {e}")
            console.print("[yellow]Warning: state.json is corrupted[/yellow]")
        except Exception as e:
            logger.error(f"Error reading state: {e}")
            console.print(f"[red]Error reading state: {e}[/red]")
