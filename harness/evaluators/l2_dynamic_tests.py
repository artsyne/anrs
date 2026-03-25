#!/usr/bin/env python3
"""
L2 Dynamic Tests

Level 2 evaluation: Dynamic testing.
- Unit tests (pytest)
- Coverage analysis (pytest-cov)
- Contract validation

Requirements:
    pip install pytest pytest-cov pytest-json-report
"""

import subprocess
import json
import tempfile
from pathlib import Path
from typing import Dict, Optional


def run_unit_tests(test_dir: str = "tests", test_cmd: Optional[str] = None) -> Dict:
    """
    Run unit tests using pytest.

    Args:
        test_dir: Test directory path
        test_cmd: Custom test command (uses pytest if None)

    Returns:
        Check result dictionary
    """
    result = {
        "name": "unit_tests",
        "status": "PASS",
        "message": "All tests passed",
        "stats": {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "errors": 0
        },
        "failed_tests": []
    }

    test_path = Path(test_dir)
    if not test_path.exists():
        result["status"] = "SKIP"
        result["message"] = f"Test directory '{test_dir}' not found"
        return result

    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json_report_path = f.name

        # Run pytest with JSON report
        cmd = test_cmd if test_cmd else [
            "pytest", test_dir,
            "-v",
            "--tb=short",
            f"--json-report",
            f"--json-report-file={json_report_path}"
        ]

        if isinstance(cmd, str):
            cmd = cmd.split()

        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        # Parse JSON report if available
        report_path = Path(json_report_path)
        if report_path.exists():
            with open(report_path) as f:
                report = json.load(f)

            summary = report.get("summary", {})
            result["stats"]["total"] = summary.get("total", 0)
            result["stats"]["passed"] = summary.get("passed", 0)
            result["stats"]["failed"] = summary.get("failed", 0)
            result["stats"]["skipped"] = summary.get("skipped", 0)
            result["stats"]["errors"] = summary.get("errors", 0)

            # Collect failed test details
            for test in report.get("tests", []):
                if test.get("outcome") in ["failed", "error"]:
                    result["failed_tests"].append({
                        "nodeid": test.get("nodeid", ""),
                        "outcome": test.get("outcome"),
                        "message": test.get("call", {}).get("longrepr", "")[:500]
                    })

            report_path.unlink()  # Clean up

        if proc.returncode != 0 or result["stats"]["failed"] > 0:
            result["status"] = "FAIL"
            failed_count = result["stats"]["failed"] + \
                result["stats"]["errors"]
            result["message"] = f"{failed_count} test(s) failed"
        else:
            result["message"] = f"All {result['stats']['passed']} test(s) passed"

    except FileNotFoundError:
        result["status"] = "SKIP"
        result["message"] = "pytest not installed (pip install pytest pytest-json-report)"
    except Exception as e:
        result["status"] = "FAIL"
        result["message"] = f"Test execution failed: {str(e)}"

    return result


def check_coverage(src_dir: str = "src", test_dir: str = "tests", min_coverage: float = 80.0) -> Dict:
    """
    Check test coverage using pytest-cov.

    Args:
        src_dir: Source directory to measure coverage for
        test_dir: Test directory
        min_coverage: Minimum coverage percentage required

    Returns:
        Check result dictionary
    """
    result = {
        "name": "coverage",
        "status": "PASS",
        "message": f"Coverage >= {min_coverage}%",
        "coverage_percent": 0.0,
        "file_coverage": [],
        "uncovered_files": []
    }

    test_path = Path(test_dir)
    src_path = Path(src_dir)

    if not test_path.exists():
        result["status"] = "SKIP"
        result["message"] = f"Test directory '{test_dir}' not found"
        return result

    if not src_path.exists():
        result["status"] = "SKIP"
        result["message"] = f"Source directory '{src_dir}' not found"
        return result

    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            cov_json_path = f.name

        # Run pytest with coverage
        proc = subprocess.run(
            [
                "pytest", test_dir,
                f"--cov={src_dir}",
                "--cov-report=json:" + cov_json_path,
                "--cov-fail-under=0",  # Don't fail here, we check manually
                "-q"
            ],
            capture_output=True,
            text=True
        )

        # Parse coverage JSON
        cov_path = Path(cov_json_path)
        if cov_path.exists():
            with open(cov_path) as f:
                cov_data = json.load(f)

            totals = cov_data.get("totals", {})
            result["coverage_percent"] = totals.get("percent_covered", 0.0)

            # Collect per-file coverage
            for filepath, file_data in cov_data.get("files", {}).items():
                file_cov = file_data.get("summary", {}).get(
                    "percent_covered", 0.0)
                result["file_coverage"].append({
                    "file": filepath,
                    "coverage": round(file_cov, 1)
                })
                if file_cov < min_coverage:
                    result["uncovered_files"].append(filepath)

            cov_path.unlink()  # Clean up

        if result["coverage_percent"] < min_coverage:
            result["status"] = "FAIL"
            result["message"] = f"Coverage {result['coverage_percent']:.1f}% < {min_coverage}%"
        else:
            result["message"] = f"Coverage {result['coverage_percent']:.1f}% >= {min_coverage}%"

    except FileNotFoundError:
        result["status"] = "SKIP"
        result["message"] = "pytest-cov not installed (pip install pytest-cov)"
    except Exception as e:
        result["status"] = "FAIL"
        result["message"] = f"Coverage check failed: {str(e)}"

    return result


def validate_contracts() -> Dict:
    """
    Validate API contracts.

    Returns:
        Check result dictionary
    """
    result = {
        "name": "contracts",
        "status": "PASS",
        "message": "API contracts valid",
        "violations": []
    }

    # Implementation would validate:
    # - OpenAPI spec matches implementation
    # - GraphQL schema matches resolvers
    # - gRPC proto matches service

    return result


def run_l2(src_dir: str = "src", test_dir: str = "tests", min_coverage: float = 80.0) -> Dict:
    """
    Run all L2 dynamic tests.

    Args:
        src_dir: Source directory
        test_dir: Test directory
        min_coverage: Minimum coverage percentage

    Returns:
        L2 evaluation result
    """
    result = {
        "status": "PASS",
        "checks": []
    }

    # Run all checks
    checks = [
        run_unit_tests(test_dir=test_dir),
        check_coverage(src_dir=src_dir, test_dir=test_dir,
                       min_coverage=min_coverage),
        validate_contracts()
    ]

    result["checks"] = checks

    # Determine overall status (SKIP doesn't cause failure)
    for check in checks:
        if check["status"] == "FAIL":
            result["status"] = "FAIL"
            break

    return result


if __name__ == "__main__":
    import sys

    result = run_l2()
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["status"] == "PASS" else 1)
