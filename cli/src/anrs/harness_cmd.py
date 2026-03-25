"""ANRS harness command - Run quality checks."""

import logging
import subprocess
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel

from anrs.constants import HARNESS_LEVELS, HARNESS_SCRIPTS

logger = logging.getLogger(__name__)
console = Console()


@click.command()
@click.option(
    "--level", "-l",
    type=click.Choice(HARNESS_LEVELS),
    default="all",
    help="Harness level to run (default: all)"
)
@click.option(
    "--strict",
    is_flag=True,
    help="Fail on any check failure"
)
@click.argument("path", default=".", type=click.Path(exists=True))
def harness(level: str, strict: bool, path: str):
    """Run ANRS harness quality checks.

    Executes the quality gate evaluators:

    \b
    - L1: Static checks (syntax, lint, complexity)
    - L2: Dynamic tests (unit tests, coverage)
    - L3: Stability analysis (risk assessment)
    - security: Security scans
    - all: Run all levels (default)
    """
    target_dir = Path(path).resolve()
    anrs_dir = target_dir / ".anrs"
    harness_dir = anrs_dir / "harness"

    if not harness_dir.exists():
        console.print(Panel(
            f"[yellow]No harness directory found[/yellow]\n\n"
            f"Initialize with [cyan]anrs init --level full[/cyan] to create harness.",
            title="ANRS Harness"
        ))
        return

    # Validate harness directory is safe (no symlinks to outside)
    if harness_dir.is_symlink():
        logger.error("Harness directory is a symlink - security risk")
        raise click.ClickException(
            "Security: .anrs/harness/ cannot be a symlink")

    # Check for quality_gate.py
    quality_gate = harness_dir / "quality_gate.py"
    if quality_gate.exists():
        # Verify quality_gate.py is within harness directory
        try:
            quality_gate.resolve().relative_to(harness_dir.resolve())
        except ValueError:
            logger.error("quality_gate.py points outside harness directory")
            raise click.ClickException(
                "Security: quality_gate.py location invalid")

        console.print(f"[bold]Running quality gate ({level})...[/bold]\n")

        cmd = [sys.executable, str(quality_gate)]
        if level != "all":
            cmd.extend(["--level", level])
        if strict:
            cmd.append("--strict")

        try:
            result = subprocess.run(cmd, cwd=target_dir, timeout=300)
            sys.exit(result.returncode)
        except subprocess.TimeoutExpired:
            logger.error("Harness timed out after 5 minutes")
            raise click.ClickException("Harness timed out (5 min limit)")
        except Exception as e:
            logger.error(f"Harness execution failed: {e}")
            raise click.ClickException(f"Harness failed: {e}")
    else:
        # Fallback to shell scripts
        console.print(
            "[yellow]quality_gate.py not found, looking for shell scripts...[/yellow]")

        if level == "all":
            levels_to_run = ["L1", "L2", "L3", "security"]
        else:
            levels_to_run = [level]

        for lvl in levels_to_run:
            script_name = HARNESS_SCRIPTS.get(lvl, "")
            script = harness_dir / script_name
            if script.exists() and script.is_file():
                console.print(f"[bold]Running {lvl}...[/bold]")
                try:
                    result = subprocess.run(
                        ["bash", str(script)],
                        cwd=target_dir,
                        timeout=120
                    )
                    if result.returncode != 0 and strict:
                        console.print(f"[red]{lvl} failed![/red]")
                        sys.exit(1)
                except subprocess.TimeoutExpired:
                    console.print(f"[red]{lvl} timed out![/red]")
                    if strict:
                        sys.exit(1)
            else:
                console.print(f"[dim]Skipping {lvl} (no script)[/dim]")

        console.print("\n[green]Harness complete[/green]")
