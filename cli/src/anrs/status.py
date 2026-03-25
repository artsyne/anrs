"""ANRS status command - Show repository status."""

import json
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


def check_file(path: Path) -> tuple[bool, str]:
    """Check if file exists and return status."""
    if path.exists():
        return True, "[green]✓[/green]"
    return False, "[red]✗[/red]"


def check_dir(path: Path) -> tuple[bool, str]:
    """Check if directory exists and return status."""
    if path.is_dir():
        return True, "[green]✓[/green]"
    return False, "[red]✗[/red]"


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
        ("Plans", check_dir(target_dir / "plans"), "plans/"),
        ("Harness", check_dir(target_dir / "harness"), "harness/"),
    ]
    
    for name, (exists, status_icon), filepath in checks:
        table.add_row(name, status_icon, filepath)
    
    console.print(table)
    
    # Show state if exists
    state_path = anrs_dir / "state.json"
    if state_path.exists():
        with open(state_path) as f:
            state = json.load(f)
        
        console.print("\n")
        state_table = Table(title="Current State")
        state_table.add_column("Field", style="cyan")
        state_table.add_column("Value")
        
        state_table.add_row("Status", state.get("status", "unknown"))
        state_table.add_row("Current Task", state.get("current_task") or "[dim]none[/dim]")
        state_table.add_row("Last Completed", state.get("last_completed") or "[dim]none[/dim]")
        
        console.print(state_table)
