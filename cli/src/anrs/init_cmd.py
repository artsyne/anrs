"""ANRS init command - Initialize ANRS in a repository."""

import json
import logging
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from anrs.constants import (
    TEMPLATES_DIR,
    ADAPTERS_DIR,
    ADAPTERS,
    LEVELS,
    DEFAULT_LEVEL,
    get_adapter_files,
)
from anrs.backup import (
    ConflictStrategy,
    backup_directory,
    backup_file,
    get_backup_dir,
    detect_user_modifications,
    show_conflict_summary,
    prompt_conflict_resolution,
    merge_json_files,
    create_backup_id,
)

logger = logging.getLogger(__name__)
console = Console()


def get_manifest(level: str) -> Dict[str, Any]:
    """Load manifest for given level."""
    manifest_path = TEMPLATES_DIR / "manifests" / f"{level}.json"
    if not manifest_path.exists():
        raise click.ClickException(f"Unknown level: {level}")
    try:
        with open(manifest_path) as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid manifest JSON: {e}")
        raise click.ClickException(f"Corrupted manifest file: {manifest_path}")
    except IOError as e:
        logger.error(f"Failed to read manifest: {e}")
        raise click.ClickException(f"Cannot read manifest: {e}")


def resolve_manifest(level: str) -> Dict[str, Any]:
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
    if adapter not in ADAPTERS:
        raise click.ClickException(
            f"Unknown adapter: {adapter}. "
            f"Available: {', '.join(ADAPTERS.keys())}"
        )

    adapter_dir = ADAPTERS_DIR / adapter
    if not adapter_dir.exists():
        raise click.ClickException(f"Adapter directory not found: {adapter}")

    for source_name, target_name in get_adapter_files(adapter):
        source_path = adapter_dir / source_name
        if not source_path.exists():
            console.print(f"[yellow]Warning: {source_name} not found[/yellow]")
            continue

        target_path = target_dir / target_name
        if dry_run:
            console.print(
                f"  [green]+ {target_name}[/green] (adapter: {adapter})")
        else:
            try:
                shutil.copy2(source_path, target_path)
                console.print(f"[green]Installed:[/green] {target_name}")
            except IOError as e:
                logger.error(f"Failed to install adapter file: {e}")
                raise click.ClickException(
                    f"Cannot install {target_name}: {e}")


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

    try:
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
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in template {source}: {e}")
        raise click.ClickException(f"Corrupted template: {source}")
    except IOError as e:
        logger.error(f"Failed to copy template: {e}")
        raise click.ClickException(f"Cannot create {target}: {e}")


@click.command()
@click.option(
    "--level", "-l",
    type=click.Choice(LEVELS),
    default=DEFAULT_LEVEL,
    help=f"Installation level (default: {DEFAULT_LEVEL})"
)
@click.option(
    "--adapter", "-a",
    type=click.Choice(list(ADAPTERS.keys())),
    help="Install adapter for specific AI tool"
)
@click.option(
    "--force", "-f",
    is_flag=True,
    help="Overwrite existing files (with automatic backup)"
)
@click.option(
    "--merge", "-m",
    is_flag=True,
    help="Merge with existing configuration (preserve user customizations)"
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Show what would be created without making changes"
)
@click.argument("path", default=".", type=click.Path())
def init(
    level: str,
    adapter: Optional[str],
    force: bool,
    merge: bool,
    dry_run: bool,
    path: str
):
    """Initialize ANRS in a repository.

    Creates the .anrs directory and required files based on the selected level:

    \b
    - minimal:  .anrs/ with ENTRY + state + config
    - standard: + plans/ + scratchpad (default)
    - full:     + skills/ + harness/ + failure-cases/

    \b
    Conflict handling:
    - Default: Asks how to handle existing files
    - --force: Backup existing files, then overwrite
    - --merge: Preserve user customizations where possible

    Use --adapter to install AI tool integration files (e.g., .cursorrules).
    """
    target_dir = Path(path).resolve()
    anrs_dir = target_dir / ".anrs"
    backup_dir = get_backup_dir(anrs_dir)

    # Resolve manifest with inheritance
    manifest = resolve_manifest(level)

    # Get project name from directory
    project_name = target_dir.name

    # Check for existing installation and detect conflicts
    conflicts = []
    if anrs_dir.exists():
        conflicts = detect_conflicts(manifest, target_dir, adapter)

    if dry_run:
        show_dry_run(manifest, target_dir, adapter, conflicts)
        return

    # Handle conflicts if any
    strategy = ConflictStrategy.BACKUP_AND_OVERWRITE
    if conflicts:
        if merge:
            strategy = ConflictStrategy.MERGE
        elif force:
            strategy = ConflictStrategy.BACKUP_AND_OVERWRITE
        else:
            show_conflict_summary(conflicts, "Existing Files Detected")
            strategy = prompt_conflict_resolution()

        if strategy == ConflictStrategy.ABORT:
            raise click.Abort()

    # Create backup if needed
    backup_id = create_backup_id()
    if conflicts and strategy == ConflictStrategy.BACKUP_AND_OVERWRITE:
        console.print("\n[bold]Creating backup...[/bold]")
        backup_path = backup_directory(
            anrs_dir, backup_dir.parent / ".anrs-backups", backup_id)
        if backup_path:
            console.print(f"[green]Backed up to:[/green] {backup_path}")

    # Execute installation
    execute_init(
        manifest=manifest,
        target_dir=target_dir,
        project_name=project_name,
        strategy=strategy,
        backup_id=backup_id,
        adapter=adapter,
    )

    # Success message
    adapter_msg = f"\nAdapter: [cyan]{adapter}[/cyan]" if adapter else ""
    backup_msg = ""
    if conflicts and strategy == ConflictStrategy.BACKUP_AND_OVERWRITE:
        backup_msg = f"\n[dim]Backup ID: {backup_id}[/dim]"
    elif conflicts and strategy == ConflictStrategy.MERGE:
        backup_msg = "\n[dim]Merged with existing configuration[/dim]"

    console.print(Panel(
        f"[bold green]ANRS initialized![/bold green]\n\n"
        f"Level: [cyan]{level}[/cyan]{adapter_msg}\n"
        f"Location: [cyan]{target_dir}[/cyan]{backup_msg}\n\n"
        f"Next steps:\n"
        f"  1. Configure [cyan].anrs/config.json[/cyan]\n"
        f"  2. Point your AI tool to [cyan].anrs/ENTRY.md[/cyan]\n"
        f"  3. Run [cyan]anrs status[/cyan] to verify",
        title="ANRS Init"
    ))


def detect_conflicts(
    manifest: Dict[str, Any],
    target_dir: Path,
    adapter: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Detect file conflicts with existing installation."""
    conflicts = []

    for file_spec in manifest.get("files", []):
        target = target_dir / file_spec["target"]
        source = TEMPLATES_DIR / "files" / file_spec["source"]

        if target.exists():
            has_mods, diff = detect_user_modifications(source, target)
            conflicts.append({
                "file": file_spec["target"],
                "status": "modified" if has_mods else "unchanged",
                "diff": diff or "",
                "source": source,
                "target": target,
            })

    # Check adapter files
    if adapter:
        for source_name, target_name in get_adapter_files(adapter):
            target = target_dir / target_name
            source = ADAPTERS_DIR / adapter / source_name

            if target.exists():
                has_mods, diff = detect_user_modifications(source, target)
                conflicts.append({
                    "file": target_name,
                    "status": "modified" if has_mods else "unchanged",
                    "diff": diff or "",
                    "source": source,
                    "target": target,
                })

    return conflicts


def show_dry_run(
    manifest: Dict[str, Any],
    target_dir: Path,
    adapter: Optional[str],
    conflicts: List[Dict[str, Any]]
) -> None:
    """Display dry-run summary."""
    console.print(Panel(
        f"[bold]Dry run[/bold] - would initialize ANRS ({manifest.get('name', 'unknown')}) in:\n"
        f"[cyan]{target_dir}[/cyan]",
        title="ANRS Init"
    ))

    if conflicts:
        console.print("\n[bold yellow]Conflicts detected:[/bold yellow]")
        for c in conflicts:
            status_color = "yellow" if c["status"] == "modified" else "dim"
            console.print(
                f"  [{status_color}]! {c['file']}[/{status_color}] ({c['status']})")
        console.print(
            "\n[dim]Use --force to backup and overwrite, or --merge to preserve customizations[/dim]")

    console.print("\n[bold]Directories to create:[/bold]")
    for d in manifest.get("directories", []):
        console.print(f"  [green]+ {d}/[/green]")

    console.print("\n[bold]Files to create:[/bold]")
    for f in manifest.get("files", []):
        console.print(f"  [green]+ {f['target']}[/green]")

    if adapter:
        console.print(f"\n[bold]Adapter files ({adapter}):[/bold]")
        install_adapter(adapter, target_dir, dry_run=True)


def execute_init(
    manifest: Dict[str, Any],
    target_dir: Path,
    project_name: str,
    strategy: ConflictStrategy,
    backup_id: str,
    adapter: Optional[str] = None,
) -> None:
    """Execute the initialization with given strategy."""
    anrs_dir = target_dir / ".anrs"
    backup_dir = get_backup_dir(anrs_dir)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Creating directories...", total=None)

        # Create directories
        for d in manifest.get("directories", []):
            dir_path = target_dir / d
            dir_path.mkdir(parents=True, exist_ok=True)

        progress.update(task, description="Installing files...")

        # Copy files with strategy
        for file_spec in manifest.get("files", []):
            source = file_spec["source"]
            target = target_dir / file_spec["target"]
            transform = file_spec.get("transform")

            install_file_with_strategy(
                source=TEMPLATES_DIR / "files" / source,
                target=target,
                project_name=project_name,
                transform=transform,
                strategy=strategy,
                backup_dir=backup_dir,
                backup_id=backup_id,
            )

    # Run post_init commands
    for cmd in manifest.get("post_init", []):
        console.print(f"[dim]{cmd}[/dim]")

    # Install adapter if specified
    if adapter:
        install_adapter_with_strategy(
            adapter=adapter,
            target_dir=target_dir,
            strategy=strategy,
            backup_dir=backup_dir,
            backup_id=backup_id,
        )


def install_file_with_strategy(
    source: Path,
    target: Path,
    project_name: str,
    transform: Optional[str],
    strategy: ConflictStrategy,
    backup_dir: Path,
    backup_id: str,
) -> None:
    """Install a single file with conflict handling strategy."""
    if not source.exists():
        console.print(
            f"[yellow]Warning: Template not found: {source.name}[/yellow]")
        return

    # Handle existing file
    if target.exists():
        if strategy == ConflictStrategy.SKIP:
            logger.info(f"Skipped existing: {target}")
            return
        elif strategy == ConflictStrategy.MERGE and target.suffix == ".json":
            # Merge JSON files
            preserve_keys = ["current_task", "status",
                             "last_completed", "history", "context"]
            merged = merge_json_files(source, target, preserve_keys)
            if merged:
                target.write_text(json.dumps(merged, indent=2))
                logger.info(f"Merged: {target}")
                return
        elif strategy == ConflictStrategy.BACKUP_AND_OVERWRITE:
            # Backup existing file
            backup_file(target, backup_dir, backup_id)

    # Read source content
    try:
        content = source.read_text()

        # Apply transform if specified
        if transform == "init_state":
            content = init_state_transform(content, project_name)
        elif transform == "init_config":
            content = init_config_transform(content, project_name)

        # Write to target
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in template {source}: {e}")
        raise click.ClickException(f"Corrupted template: {source}")
    except IOError as e:
        logger.error(f"Failed to copy template: {e}")
        raise click.ClickException(f"Cannot create {target}: {e}")


def install_adapter_with_strategy(
    adapter: str,
    target_dir: Path,
    strategy: ConflictStrategy,
    backup_dir: Path,
    backup_id: str,
) -> None:
    """Install adapter files with conflict handling strategy."""
    if adapter not in ADAPTERS:
        raise click.ClickException(
            f"Unknown adapter: {adapter}. "
            f"Available: {', '.join(ADAPTERS.keys())}"
        )

    adapter_dir = ADAPTERS_DIR / adapter
    if not adapter_dir.exists():
        raise click.ClickException(f"Adapter directory not found: {adapter}")

    for source_name, target_name in get_adapter_files(adapter):
        source_path = adapter_dir / source_name
        if not source_path.exists():
            console.print(f"[yellow]Warning: {source_name} not found[/yellow]")
            continue

        target_path = target_dir / target_name

        # Handle existing file
        if target_path.exists():
            if strategy == ConflictStrategy.SKIP:
                logger.info(f"Skipped existing adapter: {target_path}")
                continue
            elif strategy == ConflictStrategy.BACKUP_AND_OVERWRITE:
                backup_file(target_path, backup_dir, backup_id)

        try:
            shutil.copy2(source_path, target_path)
            console.print(f"[green]Installed:[/green] {target_name}")
        except IOError as e:
            logger.error(f"Failed to install adapter file: {e}")
            raise click.ClickException(f"Cannot install {target_name}: {e}")
