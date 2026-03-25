#!/usr/bin/env python3
"""
ANRS Quality Gate - Reference Implementation

This is the main entry point for AI to execute quality checks.
It integrates real evaluators (ruff, pytest, bandit, gitleaks, etc.)
with graceful degradation when tools are not installed.

Execution Order:
1. Security checks (cross-level, runs first)
2. L1 -> L2 -> L3 cascade (stops on failure)

Usage:
    python quality_gate.py [--level L1|L2|L3] [--verbose] [--skip-security] [--strict]

Strict Mode:
    In strict mode (default), checks must pass or the gate fails.
    In non-strict mode, some checks (like coverage) report WARNING instead of FAIL.
"""

import json
import sys
import time
from datetime import datetime
from pathlib import Path

# Import evaluators with graceful fallback
try:
    from evaluators.l1_static_checks import run_l1
    L1_AVAILABLE = True
except ImportError:
    L1_AVAILABLE = False

try:
    from evaluators.l2_dynamic_tests import run_l2
    L2_AVAILABLE = True
except ImportError:
    L2_AVAILABLE = False

try:
    from evaluators.l3_stability import run_l3
    L3_AVAILABLE = True
except ImportError:
    L3_AVAILABLE = False

try:
    from evaluators.security_scan import run_security_scan
    SECURITY_AVAILABLE = True
except ImportError:
    SECURITY_AVAILABLE = False


def load_config():
    """Load evaluation configuration."""
    config_path = Path(__file__).parent / "metrics" / "code_quality.json"
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)
    return {}


def run_level(level: str, verbose: bool = False, strict: bool = True, src_dir: str = "src", test_dir: str = "tests") -> dict:
    """
    Run a specific evaluation level using real evaluators.

    Args:
        level: L1, L2, or L3
        verbose: Enable verbose output
        strict: Strict mode (FAIL on issues) vs non-strict (WARNING on some issues)
        src_dir: Source directory path
        test_dir: Test directory path

    Returns:
        Level result dictionary
    """
    start_time = time.time()

    result = {
        "status": "PASS",
        "duration_ms": 0,
        "checks": []
    }

    if level == "L1":
        if L1_AVAILABLE:
            # Call real L1 evaluator
            l1_result = run_l1(src_dir)
            result["checks"] = l1_result.get("checks", [])
            result["status"] = l1_result.get("status", "PASS")
        else:
            result["checks"] = [
                {"name": "l1_checks", "status": "SKIP",
                 "message": "L1 evaluator not available (run from harness/ directory)"}
            ]

    elif level == "L2":
        if L2_AVAILABLE:
            # Call real L2 evaluator with configurable coverage threshold
            min_coverage = 60.0  # Default threshold
            l2_result = run_l2(
                src_dir=src_dir, test_dir=test_dir, min_coverage=min_coverage)
            result["checks"] = l2_result.get("checks", [])
            result["status"] = l2_result.get("status", "PASS")

            # Non-strict mode: downgrade coverage FAIL to WARNING
            if not strict:
                for check in result["checks"]:
                    if check["name"] == "coverage" and check["status"] == "FAIL":
                        check["status"] = "WARNING"
                        check["message"] = f"[non-strict] {check['message']}"
                # Recalculate overall status
                result["status"] = "PASS"
                for check in result["checks"]:
                    if check["status"] == "FAIL":
                        result["status"] = "FAIL"
                        break
        else:
            result["checks"] = [
                {"name": "l2_checks", "status": "SKIP",
                 "message": "L2 evaluator not available (run from harness/ directory)"}
            ]

    elif level == "L3":
        if L3_AVAILABLE:
            # Call real L3 evaluator
            l3_result = run_l3(chaos_enabled=False)
            result["checks"] = l3_result.get("checks", [])
            result["status"] = l3_result.get("status", "PASS")
        else:
            result["checks"] = [
                {"name": "l3_checks", "status": "SKIP",
                 "message": "L3 evaluator not available (run from harness/ directory)"}
            ]

    result["duration_ms"] = int((time.time() - start_time) * 1000)

    # Recalculate status based on checks (SKIP doesn't cause failure)
    for check in result["checks"]:
        if check["status"] == "FAIL":
            result["status"] = "FAIL"
            break

    if verbose:
        print(f"  {level}: {result['status']} ({result['duration_ms']}ms)")
        for check in result["checks"]:
            icon = {"PASS": "[PASS]", "FAIL": "[FAIL]", "SKIP": "[SKIP]",
                    "WARNING": "[WARN]"}.get(check["status"], "[????]")
            print(f"    {icon} {check['name']}: {check.get('message', '')}")

    return result


def run_security(verbose: bool = False, scan_path: str = ".") -> dict:
    """
    Run security checks (cross-level) using real evaluators.

    Security runs independently of L1/L2/L3 cascade.

    Args:
        verbose: Enable verbose output
        scan_path: Path to scan for secrets

    Returns:
        Security check result
    """
    if SECURITY_AVAILABLE:
        # Call real security evaluator
        result = run_security_scan(src_dir="src", scan_path=scan_path)
    else:
        result = {
            "status": "SKIP",
            "checks": [
                {"name": "security_scan", "status": "SKIP",
                 "message": "Security evaluator not available (run from harness/ directory)"}
            ]
        }

    if verbose:
        print("  Security:")
        for check in result.get("checks", []):
            icon = {"PASS": "[PASS]", "FAIL": "[FAIL]", "SKIP": "[SKIP]",
                    "WARNING": "[WARN]"}.get(check["status"], "[????]")
            print(f"    {icon} {check['name']}: {check.get('message', '')}")

    return result


def run_quality_gate(max_level: str = "L3", verbose: bool = False, skip_security: bool = False,
                     strict: bool = True, src_dir: str = "src", test_dir: str = "tests") -> dict:
    """
    Run the full quality gate evaluation.

    Execution order:
    1. Security checks (cross-level, runs first)
    2. L1 -> L2 -> L3 cascade (stops on failure)

    Args:
        max_level: Maximum level to run (L1, L2, or L3)
        verbose: Enable verbose output
        skip_security: Skip security checks
        strict: Strict mode (default True). Non-strict allows some checks to warn instead of fail.
        src_dir: Source directory path
        test_dir: Test directory path

    Returns:
        Full harness result
    """
    start_time = time.time()

    if verbose:
        mode_str = "strict" if strict else "non-strict"
        print(f"ANRS Quality Gate ({mode_str} mode)")
        print("=" * 40)

    result = {
        "result": "PASS",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "security": None,
        "levels": {},
        "errors": [],
        "warnings": [],
        "metrics": {}
    }

    # Run security checks first (cross-level)
    if not skip_security:
        security_result = run_security(verbose)
        result["security"] = security_result
        if security_result["status"] == "FAIL":
            result["result"] = "FAIL"
            if verbose:
                print("\n[FAIL] Quality gate FAILED at Security")
            result["duration_ms"] = int((time.time() - start_time) * 1000)
            return result

    # Run L1 -> L2 -> L3 cascade
    levels = ["L1", "L2", "L3"]
    max_idx = levels.index(max_level) + 1

    for level in levels[:max_idx]:
        level_result = run_level(level, verbose, strict, src_dir, test_dir)
        result["levels"][level] = level_result

        # Stop cascade on failure
        if level_result["status"] == "FAIL":
            result["result"] = "FAIL"
            if verbose:
                print(f"\n[FAIL] Quality gate FAILED at {level}")
            break

    result["duration_ms"] = int((time.time() - start_time) * 1000)

    if result["result"] == "PASS" and verbose:
        print(f"\n[PASS] Quality gate PASSED ({result['duration_ms']}ms)")

    return result


def save_result(result: dict):
    """Save result to reports directory."""
    reports_dir = Path(__file__).parent / "reports"
    reports_dir.mkdir(exist_ok=True)

    # Save as latest
    latest_path = reports_dir / "latest.json"
    with open(latest_path, "w") as f:
        json.dump(result, f, indent=2)

    # Archive to history
    history_dir = reports_dir / "history"
    history_dir.mkdir(exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    history_path = history_dir / f"report_{timestamp}.json"
    with open(history_path, "w") as f:
        json.dump(result, f, indent=2)


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="ANRS Quality Gate")
    parser.add_argument("--level", choices=["L1", "L2", "L3"], default="L3",
                        help="Maximum level to run")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Enable verbose output")
    parser.add_argument("--json", action="store_true",
                        help="Output JSON result")
    parser.add_argument("--skip-security", action="store_true",
                        help="Skip security checks")
    parser.add_argument("--strict", action="store_true", default=True,
                        help="Strict mode (default). Fail on any issue.")
    parser.add_argument("--no-strict", dest="strict", action="store_false",
                        help="Non-strict mode. Some checks warn instead of fail.")
    parser.add_argument("--src-dir", default="src",
                        help="Source directory (default: src)")
    parser.add_argument("--test-dir", default="tests",
                        help="Test directory (default: tests)")

    args = parser.parse_args()

    result = run_quality_gate(
        max_level=args.level,
        verbose=args.verbose,
        skip_security=args.skip_security,
        strict=args.strict,
        src_dir=args.src_dir,
        test_dir=args.test_dir
    )
    save_result(result)

    if args.json:
        print(json.dumps(result, indent=2))

    # Exit with appropriate code
    sys.exit(0 if result["result"] == "PASS" else 1)


if __name__ == "__main__":
    main()
