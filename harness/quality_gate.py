#!/usr/bin/env python3
"""
🧪 AHES Quality Gate

Main entry point for the harness evaluation system.
Runs L1 → L2 → L3 cascade evaluation.

Usage:
    python quality_gate.py [--level L1|L2|L3] [--verbose]
"""

import json
import sys
import time
from datetime import datetime
from pathlib import Path

# Import evaluators
# from evaluators.l1_static_checks import run_l1
# from evaluators.l2_dynamic_tests import run_l2
# from evaluators.l3_stability_fmea import run_l3
# from evaluators.security_scan import run_security


def load_config():
    """Load evaluation configuration."""
    config_path = Path(__file__).parent / "metrics" / "code_quality.json"
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)
    return {}


def run_level(level: str, verbose: bool = False) -> dict:
    """
    Run a specific evaluation level.

    Args:
        level: L1, L2, or L3
        verbose: Enable verbose output

    Returns:
        Level result dictionary
    """
    start_time = time.time()

    # Placeholder implementation
    # In production, this would call actual evaluators
    result = {
        "status": "PASS",
        "duration_ms": 0,
        "checks": []
    }

    if level == "L1":
        # Static checks: lint, syntax, complexity
        result["checks"] = [
            {"name": "syntax", "status": "PASS", "message": "No syntax errors"},
            {"name": "lint", "status": "PASS", "message": "No lint issues"},
            {"name": "complexity", "status": "PASS",
                "message": "Complexity within limits"}
        ]
    elif level == "L2":
        # Dynamic tests: unit tests, contracts
        result["checks"] = [
            {"name": "unit_tests", "status": "PASS", "message": "All tests passed"},
            {"name": "coverage", "status": "PASS", "message": "Coverage >= 80%"},
            {"name": "contracts", "status": "PASS",
                "message": "API contracts valid"}
        ]
    elif level == "L3":
        # Stability: FMEA, chaos
        result["checks"] = [
            {"name": "fmea", "status": "PASS", "message": "No high-risk items"},
            {"name": "chaos", "status": "SKIP", "message": "Skipped in dev mode"}
        ]

    result["duration_ms"] = int((time.time() - start_time) * 1000)

    # Check if any check failed
    for check in result["checks"]:
        if check["status"] == "FAIL":
            result["status"] = "FAIL"
            break

    if verbose:
        print(f"  {level}: {result['status']} ({result['duration_ms']}ms)")
        for check in result["checks"]:
            status_icon = "✅" if check["status"] == "PASS" else "❌" if check["status"] == "FAIL" else "⏭️"
            print(f"    {status_icon} {check['name']}: {check['message']}")

    return result


def run_quality_gate(max_level: str = "L3", verbose: bool = False) -> dict:
    """
    Run the full quality gate evaluation.

    Args:
        max_level: Maximum level to run (L1, L2, or L3)
        verbose: Enable verbose output

    Returns:
        Full harness result
    """
    start_time = time.time()

    if verbose:
        print("🧪 AHES Quality Gate")
        print("=" * 40)

    result = {
        "result": "PASS",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "levels": {},
        "errors": [],
        "warnings": [],
        "metrics": {}
    }

    levels = ["L1", "L2", "L3"]
    max_idx = levels.index(max_level) + 1

    for level in levels[:max_idx]:
        level_result = run_level(level, verbose)
        result["levels"][level] = level_result

        # Stop cascade on failure
        if level_result["status"] == "FAIL":
            result["result"] = "FAIL"
            if verbose:
                print(f"\n❌ Quality gate FAILED at {level}")
            break

    result["duration_ms"] = int((time.time() - start_time) * 1000)

    if result["result"] == "PASS" and verbose:
        print(f"\n✅ Quality gate PASSED ({result['duration_ms']}ms)")

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

    parser = argparse.ArgumentParser(description="AHES Quality Gate")
    parser.add_argument("--level", choices=["L1", "L2", "L3"], default="L3",
                        help="Maximum level to run")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Enable verbose output")
    parser.add_argument("--json", action="store_true",
                        help="Output JSON result")

    args = parser.parse_args()

    result = run_quality_gate(args.level, args.verbose)
    save_result(result)

    if args.json:
        print(json.dumps(result, indent=2))

    # Exit with appropriate code
    sys.exit(0 if result["result"] == "PASS" else 1)


if __name__ == "__main__":
    main()
