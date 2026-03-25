"""ANRS harness command - Run quality checks."""

import subprocess
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel

console = Console()


@click.command()
@click.option(
    "--level", "-l",
    type=click.Choice(["L1", "L2", "L3", "security", "all"]),
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
    harness_dir = target_dir / "harness"
    
    if not harness_dir.exists():
        console.print(Panel(
            f"[yellow]No harness directory found[/yellow]\n\n"
            f"Create [cyan]harness/[/cyan] with evaluator scripts.",
            title="ANRS Harness"
        ))
        return
    
    # Check for quality_gate.py
    quality_gate = harness_dir / "quality_gate.py"
    if quality_gate.exists():
        console.print(f"[bold]Running quality gate ({level})...[/bold]\n")
        
        cmd = [sys.executable, str(quality_gate)]
        if level != "all":
            cmd.extend(["--level", level])
        if strict:
            cmd.append("--strict")
        
        result = subprocess.run(cmd, cwd=target_dir)
        sys.exit(result.returncode)
    else:
        # Fallback to shell scripts
        console.print("[yellow]quality_gate.py not found, looking for shell scripts...[/yellow]")
        
        scripts = {
            "L1": "l1_lint.sh",
            "L2": "l2_test.sh",
            "L3": "l3_risk.sh",
            "security": "security_scan.sh",
        }
        
        if level == "all":
            levels_to_run = ["L1", "L2", "L3", "security"]
        else:
            levels_to_run = [level]
        
        for lvl in levels_to_run:
            script = harness_dir / scripts.get(lvl, "")
            if script.exists():
                console.print(f"[bold]Running {lvl}...[/bold]")
                result = subprocess.run(["bash", str(script)], cwd=target_dir)
                if result.returncode != 0 and strict:
                    console.print(f"[red]{lvl} failed![/red]")
                    sys.exit(1)
            else:
                console.print(f"[dim]Skipping {lvl} (no script)[/dim]")
        
        console.print("\n[green]Harness complete[/green]")
