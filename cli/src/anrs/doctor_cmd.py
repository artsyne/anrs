"""ANRS doctor command - Diagnose and repair ANRS installation."""

import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, NamedTuple, Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

logger = logging.getLogger(__name__)
console = Console()


class CheckResult(NamedTuple):
    """Result of a single health check."""

    name: str
    status: str  # "pass", "warn", "fail"
    message: str
    fix_hint: Optional[str] = None


class HealthReport(NamedTuple):
    """Overall health report."""

    checks: List[CheckResult]
    passed: int
    warnings: int
    failures: int


def check_python_version() -> CheckResult:
    """Check Python version compatibility."""
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"

    if version >= (3, 9):
        return CheckResult(
            name="Python Version",
            status="pass",
            message=f"Python {version_str} (>= 3.9 required)",
        )
    else:
        return CheckResult(
            name="Python Version",
            status="fail",
            message=f"Python {version_str} is too old",
            fix_hint="Upgrade to Python 3.9 or higher",
        )


def check_anrs_directory(target_dir: Path) -> CheckResult:
    """Check if .anrs directory exists."""
    anrs_dir = target_dir / ".anrs"

    if anrs_dir.is_dir():
        return CheckResult(
            name=".anrs Directory",
            status="pass",
            message="Directory exists",
        )
    elif anrs_dir.exists():
        return CheckResult(
            name=".anrs Directory",
            status="fail",
            message=".anrs exists but is not a directory",
            fix_hint="Remove .anrs file and run 'anrs init'",
        )
    else:
        return CheckResult(
            name=".anrs Directory",
            status="fail",
            message="Not an ANRS repository",
            fix_hint="Run 'anrs init' to initialize",
        )


def check_entry_md(target_dir: Path) -> CheckResult:
    """Check ENTRY.md file."""
    entry_path = target_dir / ".anrs" / "ENTRY.md"

    if not entry_path.exists():
        return CheckResult(
            name="ENTRY.md",
            status="fail",
            message="Missing required file",
            fix_hint="Run 'anrs upgrade' to restore",
        )

    content = entry_path.read_text()
    if len(content) < 100:
        return CheckResult(
            name="ENTRY.md",
            status="warn",
            message="File seems incomplete",
            fix_hint="Check file contents or run 'anrs upgrade --force'",
        )

    return CheckResult(
        name="ENTRY.md",
        status="pass",
        message="Present and valid",
    )


def check_state_json(target_dir: Path) -> CheckResult:
    """Check state.json file."""
    state_path = target_dir / ".anrs" / "state.json"

    if not state_path.exists():
        return CheckResult(
            name="state.json",
            status="fail",
            message="Missing required file",
            fix_hint="Run 'anrs upgrade' to restore",
        )

    try:
        with open(state_path) as f:
            state = json.load(f)
    except json.JSONDecodeError as e:
        return CheckResult(
            name="state.json",
            status="fail",
            message=f"Invalid JSON: {e.msg} at line {e.lineno}",
            fix_hint="Fix JSON syntax or run 'anrs doctor --fix'",
        )

    # Check required fields
    required_fields = ["status", "metadata"]
    missing = [f for f in required_fields if f not in state]

    if missing:
        return CheckResult(
            name="state.json",
            status="fail",
            message=f"Missing required fields: {', '.join(missing)}",
            fix_hint="Run 'anrs doctor --fix' to reset state",
        )

    # Check status value
    valid_statuses = ["idle", "active", "blocked", "completed"]
    if state.get("status") not in valid_statuses:
        return CheckResult(
            name="state.json",
            status="warn",
            message=f"Invalid status value: {state.get('status')}",
            fix_hint=f"Set status to one of: {', '.join(valid_statuses)}",
        )

    return CheckResult(
        name="state.json",
        status="pass",
        message=f"Valid (status: {state.get('status', 'unknown')})",
    )


def check_config_json(target_dir: Path) -> CheckResult:
    """Check config.json file."""
    config_path = target_dir / ".anrs" / "config.json"

    if not config_path.exists():
        return CheckResult(
            name="config.json",
            status="fail",
            message="Missing required file",
            fix_hint="Run 'anrs upgrade' to restore",
        )

    try:
        with open(config_path) as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        return CheckResult(
            name="config.json",
            status="fail",
            message=f"Invalid JSON: {e.msg} at line {e.lineno}",
            fix_hint="Fix JSON syntax or run 'anrs doctor --fix'",
        )

    # Check project name
    if not config.get("project", {}).get("name"):
        return CheckResult(
            name="config.json",
            status="warn",
            message="Project name not configured",
            fix_hint="Set project.name in config.json",
        )

    return CheckResult(
        name="config.json",
        status="pass",
        message=f"Valid (project: {config.get('project', {}).get('name', 'unnamed')})",
    )


def check_adapter_files(target_dir: Path) -> CheckResult:
    """Check for adapter configuration files."""
    adapters_found = []

    adapter_files = {
        ".cursorrules": "Cursor",
        "CLAUDE.md": "Claude Code",
        "AGENTS.md": "Codex",
        "opencode.json": "OpenCode",
    }

    for filename, name in adapter_files.items():
        if (target_dir / filename).exists():
            adapters_found.append(name)

    if adapters_found:
        return CheckResult(
            name="Adapters",
            status="pass",
            message=f"Found: {', '.join(adapters_found)}",
        )
    else:
        return CheckResult(
            name="Adapters",
            status="warn",
            message="No adapter installed",
            fix_hint="Run 'anrs adapter install <name>' to add one",
        )


def check_plans_directory(target_dir: Path) -> CheckResult:
    """Check plans directory structure."""
    plans_dir = target_dir / ".anrs" / "plans"

    if not plans_dir.exists():
        return CheckResult(
            name="Plans Directory",
            status="warn",
            message="Not present (standard level required)",
            fix_hint="Run 'anrs init --level standard' to add",
        )

    subdirs = ["active", "backlog", "completed"]
    missing = [d for d in subdirs if not (plans_dir / d).is_dir()]

    if missing:
        return CheckResult(
            name="Plans Directory",
            status="warn",
            message=f"Missing subdirectories: {', '.join(missing)}",
            fix_hint="Run 'anrs upgrade' to restore structure",
        )

    return CheckResult(
        name="Plans Directory",
        status="pass",
        message="Structure complete",
    )


def check_harness_directory(target_dir: Path) -> CheckResult:
    """Check harness directory."""
    harness_dir = target_dir / "harness"

    if not harness_dir.exists():
        return CheckResult(
            name="Harness",
            status="warn",
            message="Not present (full level required)",
            fix_hint="Run 'anrs init --level full' to add",
        )

    # Check for quality_gate.py
    if (harness_dir / "quality_gate.py").exists():
        return CheckResult(
            name="Harness",
            status="pass",
            message="Quality gate present",
        )

    return CheckResult(
        name="Harness",
        status="warn",
        message="Directory exists but quality_gate.py missing",
        fix_hint="Add quality_gate.py for full harness support",
    )


def run_health_checks(target_dir: Path) -> HealthReport:
    """Run all health checks and return report."""
    checks = [
        check_python_version(),
        check_anrs_directory(target_dir),
    ]

    # Only run detailed checks if .anrs exists
    anrs_dir = target_dir / ".anrs"
    if anrs_dir.is_dir():
        checks.extend([
            check_entry_md(target_dir),
            check_state_json(target_dir),
            check_config_json(target_dir),
            check_adapter_files(target_dir),
            check_plans_directory(target_dir),
            check_harness_directory(target_dir),
        ])

    passed = sum(1 for c in checks if c.status == "pass")
    warnings = sum(1 for c in checks if c.status == "warn")
    failures = sum(1 for c in checks if c.status == "fail")

    return HealthReport(
        checks=checks,
        passed=passed,
        warnings=warnings,
        failures=failures,
    )


def fix_state_json(target_dir: Path) -> bool:
    """Attempt to fix state.json."""
    state_path = target_dir / ".anrs" / "state.json"

    try:
        # Create minimal valid state
        from datetime import datetime
        state = {
            "status": "idle",
            "current_task": None,
            "last_completed": None,
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
            },
        }

        # Backup existing if present
        if state_path.exists():
            backup_path = state_path.with_suffix(".json.bak")
            state_path.rename(backup_path)
            console.print(f"[dim]Backed up to: {backup_path}[/dim]")

        state_path.write_text(json.dumps(state, indent=2))
        return True
    except IOError as e:
        logger.error(f"Failed to fix state.json: {e}")
        return False


def display_report(report: HealthReport) -> None:
    """Display health report in a formatted panel."""
    # Status icons
    icons = {
        "pass": "[green]✓[/green]",
        "warn": "[yellow]⚠[/yellow]",
        "fail": "[red]✗[/red]",
    }

    # Build table
    table = Table(show_header=False, box=None, padding=(0, 1))
    table.add_column("Icon", width=3)
    table.add_column("Check", width=20)
    table.add_column("Status")

    for check in report.checks:
        icon = icons.get(check.status, "?")
        table.add_row(icon, check.name, check.message)

    console.print(Panel(
        table,
        title="ANRS Health Check",
        subtitle=f"[green]{report.passed} passed[/green] | "
        f"[yellow]{report.warnings} warnings[/yellow] | "
        f"[red]{report.failures} failures[/red]",
    ))

    # Show fix hints for failures
    failures = [c for c in report.checks if c.status == "fail" and c.fix_hint]
    if failures:
        console.print("\n[bold red]Issues requiring attention:[/bold red]")
        for check in failures:
            console.print(Panel(
                f"[bold]{check.name}[/bold]: {check.message}\n\n"
                f"[cyan]Fix:[/cyan] {check.fix_hint}",
                border_style="red",
            ))


@click.command()
@click.option(
    "--fix",
    is_flag=True,
    help="Attempt to auto-fix detected issues",
)
@click.option(
    "--verbose", "-v",
    is_flag=True,
    help="Show detailed diagnostic information",
)
@click.argument("path", default=".", type=click.Path(exists=True))
def doctor(fix: bool, verbose: bool, path: str) -> None:
    """Diagnose and repair ANRS installation.

    Checks the health of your ANRS setup and reports any issues.
    Use --fix to attempt automatic repairs.

    \b
    Checks performed:
    - Python version compatibility
    - .anrs/ directory structure
    - Configuration file validity
    - Adapter installation status
    - Plans directory structure
    - Harness configuration
    """
    target_dir = Path(path).resolve()

    if verbose:
        console.print(f"[dim]Checking: {target_dir}[/dim]\n")

    # Run health checks
    report = run_health_checks(target_dir)

    # Display report
    display_report(report)

    # Attempt fixes if requested
    if fix and report.failures > 0:
        console.print("\n[bold]Attempting auto-fix...[/bold]\n")

        fixed = 0
        for check in report.checks:
            if check.status == "fail":
                if check.name == "state.json" and "Invalid JSON" in check.message:
                    if fix_state_json(target_dir):
                        console.print(f"[green]✓[/green] Fixed: {check.name}")
                        fixed += 1
                    else:
                        console.print(
                            f"[red]✗[/red] Could not fix: {check.name}")

        if fixed > 0:
            console.print(f"\n[green]Fixed {fixed} issue(s).[/green]")
            console.print("[dim]Run 'anrs doctor' again to verify.[/dim]")
        else:
            console.print(
                "\n[yellow]No automatic fixes available for detected issues.[/yellow]")
            console.print(
                "[dim]See hints above for manual resolution steps.[/dim]")

    # Exit with appropriate code
    if report.failures > 0:
        raise SystemExit(1)
