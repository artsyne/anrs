"""ANRS init command - Initialize ANRS in a repository."""

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel

console = Console()

# Template directory relative to this file
# cli/src/anrs/init_cmd.py -> cli/src/anrs -> cli/src -> cli -> anrs (root)
ROOT_DIR = Path(__file__).parent.parent.parent.parent
TEMPLATES_DIR = ROOT_DIR / "templates"
ADAPTERS_DIR = ROOT_DIR / "adapters"

# Available adapters and their files
ADAPTER_FILES = {
    "cursor": [
        (".cursorrules", ".cursorrules"),
    ],
    "claude-code": [
        ("CLAUDE.md", "CLAUDE.md"),
    ],
    "codex": [
        ("AGENTS.md", "AGENTS.md"),
    ],
    "opencode": [
        ("opencode.json", "opencode.json"),
    ],
}


def get_manifest(level: str) -> dict:
    """Load manifest for given level."""
    manifest_path = TEMPLATES_DIR / "manifests" / f"{level}.json"
    if not manifest_path.exists():
        raise click.ClickException(f"Unknown level: {level}")
    with open(manifest_path) as f:
        return json.load(f)


def resolve_manifest(level: str) -> dict:
    """Resolve manifest with inheritance."""
    manifest = get_manifest(level)

    # Handle inheritance
    if "extends" in manifest:
        parent = resolve_manifest(manifest["extends"])
        # Merge files and directories
        files = parent.get("files", []) + manifest.get("files", [])
        dirs = parent.get("directories", []) + manifest.get("directories", [])
        manifest["files"] = files
        manifest["directories"] = dirs

    return manifest


def init_state_transform(content: str, project_name: str) -> str:
    """Transform state template with project info."""
    data = json.loads(content)
    now = datetime.now().isoformat()
    data["metadata"]["created_at"] = now
    data["metadata"]["updated_at"] = now
    return json.dumps(data, indent=2)


def init_config_transform(content: str, project_name: str) -> str:
    """Transform config template with project info."""
    data = json.loads(content)
    data["project"]["name"] = project_name
    return json.dumps(data, indent=2)


def install_adapter(adapter: str, target_dir: Path, dry_run: bool = False) -> None:
    """Install adapter files to target directory."""
    if adapter not in ADAPTER_FILES:
        raise click.ClickException(
            f"Unknown adapter: {adapter}. "
            f"Available: {', '.join(ADAPTER_FILES.keys())}"
        )

    adapter_dir = ADAPTERS_DIR / adapter
    if not adapter_dir.exists():
        raise click.ClickException(f"Adapter directory not found: {adapter}")

    for source_name, target_name in ADAPTER_FILES[adapter]:
        source_path = adapter_dir / source_name
        if not source_path.exists():
            console.print(f"[yellow]Warning: {source_name} not found[/yellow]")
            continue

        target_path = target_dir / target_name
        if dry_run:
            console.print(
                f"  [green]+ {target_name}[/green] (adapter: {adapter})")
        else:
            shutil.copy2(source_path, target_path)
            console.print(f"[green]Installed:[/green] {target_name}")


def copy_template_file(
    source: str,
    target: Path,
    project_name: str,
    transform: Optional[str] = None
) -> None:
    """Copy template file to target, optionally transforming content."""
    source_path = TEMPLATES_DIR / "files" / source

    if not source_path.exists():
        console.print(
            f"[yellow]Warning: Template not found: {source}[/yellow]")
        return

    # Read source content
    content = source_path.read_text()

    # Apply transform if specified
    if transform == "init_state":
        content = init_state_transform(content, project_name)
    elif transform == "init_config":
        content = init_config_transform(content, project_name)

    # Write to target
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content)


@click.command()
@click.option(
    "--level", "-l",
    type=click.Choice(["minimal", "standard", "full"]),
    default="standard",
    help="Installation level (default: standard)"
)
@click.option(
    "--adapter", "-a",
    type=click.Choice(["cursor", "claude-code", "codex", "opencode"]),
    help="Install adapter for specific AI tool"
)
@click.option(
    "--force", "-f",
    is_flag=True,
    help="Overwrite existing .anrs directory"
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Show what would be created without making changes"
)
@click.argument("path", default=".", type=click.Path())
def init(level: str, adapter: Optional[str], force: bool, dry_run: bool, path: str):
    """Initialize ANRS in a repository.

    Creates the .anrs directory and required files based on the selected level:

    \b
    - minimal:  .anrs/ with ENTRY + state + config
    - standard: + plans/ + scratchpad (default)
    - full:     + skills/ + harness/ + failure-cases/

    Use --adapter to install AI tool integration files (e.g., .cursorrules).
    """
    target_dir = Path(path).resolve()
    anrs_dir = target_dir / ".anrs"

    # Check if already initialized
    if anrs_dir.exists() and not force:
        raise click.ClickException(
            f".anrs already exists at {target_dir}. Use --force to overwrite."
        )

    # Resolve manifest with inheritance
    manifest = resolve_manifest(level)

    # Get project name from directory
    project_name = target_dir.name

    if dry_run:
        console.print(Panel(
            f"[bold]Dry run[/bold] - would initialize ANRS ({level}) in:\n"
            f"[cyan]{target_dir}[/cyan]",
            title="ANRS Init"
        ))
        console.print("\n[bold]Directories to create:[/bold]")
        for d in manifest.get("directories", []):
            console.print(f"  [green]+ {d}/[/green]")
        console.print("\n[bold]Files to create:[/bold]")
        for f in manifest.get("files", []):
            console.print(f"  [green]+ {f['target']}[/green]")
        if adapter:
            console.print(f"\n[bold]Adapter files ({adapter}):[/bold]")
            install_adapter(adapter, target_dir, dry_run=True)
        return

    # Remove existing .anrs if force
    if force and anrs_dir.exists():
        shutil.rmtree(anrs_dir)
        console.print("[yellow]Removed existing .anrs directory[/yellow]")

    # Create directories
    for d in manifest.get("directories", []):
        dir_path = target_dir / d
        dir_path.mkdir(parents=True, exist_ok=True)

    # Copy files
    for file_spec in manifest.get("files", []):
        source = file_spec["source"]
        target = target_dir / file_spec["target"]
        transform = file_spec.get("transform")
        copy_template_file(source, target, project_name, transform)

    # Run post_init commands
    for cmd in manifest.get("post_init", []):
        console.print(f"[dim]{cmd}[/dim]")

    # Install adapter if specified
    if adapter:
        install_adapter(adapter, target_dir)

    # Success message
    adapter_msg = f"\nAdapter: [cyan]{adapter}[/cyan]" if adapter else ""
    console.print(Panel(
        f"[bold green]ANRS initialized![/bold green]\n\n"
        f"Level: [cyan]{level}[/cyan]{adapter_msg}\n"
        f"Location: [cyan]{target_dir}[/cyan]\n\n"
        f"Next steps:\n"
        f"  1. Configure [cyan].anrs/config.json[/cyan]\n"
        f"  2. Point your AI tool to [cyan].anrs/ENTRY.md[/cyan]\n"
        f"  3. Run [cyan]anrs status[/cyan] to verify",
        title="ANRS Init"
    ))
