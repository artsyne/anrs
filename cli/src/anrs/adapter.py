"""ANRS adapter command - Manage AI tool adapters."""

import shutil
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

console = Console()

# Adapter templates directory
# cli/src/anrs/adapter.py -> cli/src/anrs -> cli/src -> cli -> anrs (root)
ADAPTERS_DIR = Path(__file__).parent.parent.parent.parent / "adapters"


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
    
    adapters = [
        ("cursor", "Cursor AI editor", ".cursorrules"),
        ("claude-code", "Claude Code (Anthropic)", "CLAUDE.md"),
        ("codex", "OpenAI Codex CLI", "AGENTS.md"),
        ("opencode", "OpenCode AI", "opencode.json"),
    ]
    
    for name, desc, config in adapters:
        table.add_row(name, desc, config)
    
    console.print(table)


@adapter.command("install")
@click.argument("adapter_name")
@click.option(
    "--force", "-f",
    is_flag=True,
    help="Overwrite existing adapter config"
)
@click.argument("path", default=".", type=click.Path(exists=True))
def install_adapter(adapter_name: str, force: bool, path: str):
    """Install an adapter for an AI tool.
    
    Creates a trampoline config file that points to .anrs/ENTRY.md
    """
    target_dir = Path(path).resolve()
    adapter_source = ADAPTERS_DIR / adapter_name
    
    if not adapter_source.exists():
        raise click.ClickException(f"Unknown adapter: {adapter_name}")
    
    # Adapter config file mappings
    config_files = {
        "cursor": ".cursorrules",
        "claude-code": "CLAUDE.md",
        "codex": "AGENTS.md",
        "opencode": "opencode.json",
    }
    
    config_file = config_files.get(adapter_name)
    if not config_file:
        raise click.ClickException(f"No config file mapping for: {adapter_name}")
    
    source_path = adapter_source / config_file
    target_path = target_dir / config_file
    
    if target_path.exists() and not force:
        raise click.ClickException(
            f"{config_file} already exists. Use --force to overwrite."
        )
    
    # Copy the trampoline config
    shutil.copy(source_path, target_path)
    
    console.print(f"[green]Installed {adapter_name} adapter[/green]")
    console.print(f"Config: [cyan]{target_path}[/cyan]")
    console.print(f"\nThe adapter will redirect AI to [cyan].anrs/ENTRY.md[/cyan]")
