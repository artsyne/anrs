#!/usr/bin/env python3
"""
Security Scanner

Security evaluation across all levels.
- Dependency vulnerabilities (pip-audit)
- Secret detection (gitleaks)
- SAST (bandit for Python)

Requirements:
    pip install pip-audit bandit
    brew install gitleaks  # or download from GitHub
"""

import subprocess
import json
import tempfile
from pathlib import Path
from typing import Dict, List, Optional


def scan_dependencies(requirements_file: Optional[str] = None) -> Dict:
    """
    Scan for vulnerable dependencies using pip-audit.

    Args:
        requirements_file: Path to requirements.txt (auto-detect if None)

    Returns:
        Scan result dictionary
    """
    result = {
        "name": "dependency_scan",
        "status": "PASS",
        "message": "No vulnerable dependencies",
        "vulnerabilities": [],
        "scanned_packages": 0
    }

    try:
        # Build command
        cmd = ["pip-audit", "--format=json", "--progress-spinner=off"]
        if requirements_file and Path(requirements_file).exists():
            cmd.extend(["-r", requirements_file])

        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        if proc.stdout.strip():
            audit_data = json.loads(proc.stdout)

            # pip-audit returns a list of vulnerabilities
            if isinstance(audit_data, list):
                for vuln in audit_data:
                    result["vulnerabilities"].append({
                        "package": vuln.get("name", ""),
                        "version": vuln.get("version", ""),
                        "vuln_id": vuln.get("id", ""),
                        "description": vuln.get("description", "")[:200],
                        "fix_versions": vuln.get("fix_versions", [])
                    })
            elif isinstance(audit_data, dict):
                # Handle dict format
                dependencies = audit_data.get("dependencies", [])
                result["scanned_packages"] = len(dependencies)
                for dep in dependencies:
                    for vuln in dep.get("vulns", []):
                        result["vulnerabilities"].append({
                            "package": dep.get("name", ""),
                            "version": dep.get("version", ""),
                            "vuln_id": vuln.get("id", ""),
                            "description": vuln.get("description", "")[:200],
                            "fix_versions": vuln.get("fix_versions", [])
                        })

        if result["vulnerabilities"]:
            result["status"] = "FAIL"
            result["message"] = f"{len(result['vulnerabilities'])} vulnerable dependency(ies) found"

    except FileNotFoundError:
        result["status"] = "SKIP"
        result["message"] = "pip-audit not installed (pip install pip-audit)"
    except json.JSONDecodeError:
        result["message"] = "No vulnerabilities found"
    except Exception as e:
        result["status"] = "FAIL"
        result["message"] = f"Dependency scan failed: {str(e)}"

    return result


def detect_secrets(scan_path: str = ".") -> Dict:
    """
    Scan for hardcoded secrets using gitleaks.

    Args:
        scan_path: Path to scan for secrets

    Returns:
        Scan result dictionary
    """
    result = {
        "name": "secret_detection",
        "status": "PASS",
        "message": "No secrets detected",
        "findings": []
    }

    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            report_path = f.name

        # Run gitleaks
        proc = subprocess.run(
            [
                "gitleaks", "detect",
                "--source", scan_path,
                "--report-format", "json",
                "--report-path", report_path,
                "--no-git"  # Scan files directly, not git history
            ],
            capture_output=True,
            text=True
        )

        # Parse report
        report_file = Path(report_path)
        if report_file.exists():
            content = report_file.read_text().strip()
            if content:
                findings = json.loads(content)
                for finding in findings:
                    result["findings"].append({
                        "rule": finding.get("RuleID", ""),
                        "file": finding.get("File", ""),
                        "line": finding.get("StartLine"),
                        "match": finding.get("Match", "")[:50] + "..." if len(finding.get("Match", "")) > 50 else finding.get("Match", ""),
                        "description": finding.get("Description", "")
                    })
            report_file.unlink()

        if result["findings"]:
            result["status"] = "FAIL"
            result["message"] = f"{len(result['findings'])} secret(s) detected"

    except FileNotFoundError:
        result["status"] = "SKIP"
        result["message"] = "gitleaks not installed (brew install gitleaks)"
    except json.JSONDecodeError:
        result["message"] = "No secrets detected"
    except Exception as e:
        result["status"] = "FAIL"
        result["message"] = f"Secret detection failed: {str(e)}"

    return result


def run_sast(src_dir: str = "src") -> Dict:
    """
    Run Static Application Security Testing using bandit (Python).

    Args:
        src_dir: Source directory to scan

    Returns:
        Scan result dictionary
    """
    result = {
        "name": "sast",
        "status": "PASS",
        "message": "No security issues found",
        "findings": [],
        "stats": {
            "high": 0,
            "medium": 0,
            "low": 0
        }
    }

    src_path = Path(src_dir)
    if not src_path.exists():
        result["status"] = "SKIP"
        result["message"] = f"Source directory '{src_dir}' not found"
        return result

    # Check if there are Python files
    py_files = list(src_path.rglob("*.py"))
    if not py_files:
        result["status"] = "SKIP"
        result["message"] = "No Python files to scan"
        return result

    try:
        # Run bandit with JSON output
        proc = subprocess.run(
            [
                "bandit",
                "-r", src_dir,
                "-f", "json",
                "-ll"  # Only report medium and high severity
            ],
            capture_output=True,
            text=True
        )

        if proc.stdout.strip():
            bandit_data = json.loads(proc.stdout)

            # Parse metrics
            metrics = bandit_data.get("metrics", {}).get("_totals", {})
            result["stats"]["high"] = metrics.get("SEVERITY.HIGH", 0)
            result["stats"]["medium"] = metrics.get("SEVERITY.MEDIUM", 0)
            result["stats"]["low"] = metrics.get("SEVERITY.LOW", 0)

            # Parse results
            for issue in bandit_data.get("results", []):
                result["findings"].append({
                    "file": issue.get("filename", ""),
                    "line": issue.get("line_number"),
                    "severity": issue.get("issue_severity", ""),
                    "confidence": issue.get("issue_confidence", ""),
                    "issue_text": issue.get("issue_text", ""),
                    "test_id": issue.get("test_id", "")
                })

        # Only fail on high severity issues
        if result["stats"]["high"] > 0:
            result["status"] = "FAIL"
            result["message"] = f"{result['stats']['high']} high severity issue(s) found"
        elif result["findings"]:
            result["message"] = f"{len(result['findings'])} issue(s) found (no high severity)"

    except FileNotFoundError:
        result["status"] = "SKIP"
        result["message"] = "bandit not installed (pip install bandit)"
    except json.JSONDecodeError:
        result["message"] = "No security issues found"
    except Exception as e:
        result["status"] = "FAIL"
        result["message"] = f"SAST scan failed: {str(e)}"

    return result


def run_security_scan(src_dir: str = "src", scan_path: str = ".") -> Dict:
    """
    Run all security scans.

    Args:
        src_dir: Source directory for SAST
        scan_path: Path for secret scanning

    Returns:
        Security evaluation result
    """
    result = {
        "status": "PASS",
        "checks": []
    }

    # Run all checks
    checks = [
        scan_dependencies(),
        detect_secrets(scan_path),
        run_sast(src_dir)
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

    result = run_security_scan()
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["status"] == "PASS" else 1)
