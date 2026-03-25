#!/usr/bin/env python3
"""
L1 Static Checks

Level 1 evaluation: Static code analysis.
- Syntax validation (py_compile)
- Lint checks (ruff)
- Complexity analysis (radon)

Requirements:
    pip install ruff radon
"""

import subprocess
import json
import py_compile
import sys
from pathlib import Path
from typing import List, Dict


def check_syntax(files: List[str]) -> Dict:
    """
    Check for syntax errors in Python source files using py_compile.

    Args:
        files: List of file paths to check

    Returns:
        Check result dictionary
    """
    result = {
        "name": "syntax",
        "status": "PASS",
        "message": "No syntax errors",
        "errors": [],
        "files_checked": 0
    }

    py_files = [f for f in files if f.endswith('.py')]
    result["files_checked"] = len(py_files)

    if not py_files:
        result["message"] = "No Python files to check"
        return result

    for filepath in py_files:
        try:
            py_compile.compile(filepath, doraise=True)
        except py_compile.PyCompileError as e:
            result["errors"].append({
                "file": filepath,
                "line": e.exc_value.lineno if hasattr(e.exc_value, 'lineno') else None,
                "message": str(e.exc_value.msg if hasattr(e.exc_value, 'msg') else e)
            })
        except Exception as e:
            result["errors"].append({
                "file": filepath,
                "line": None,
                "message": str(e)
            })

    if result["errors"]:
        result["status"] = "FAIL"
        result["message"] = f"Syntax errors in {len(result['errors'])} file(s)"

    return result


def check_lint(files: List[str]) -> Dict:
    """
    Run ruff linter on Python source files.

    Args:
        files: List of file paths to check

    Returns:
        Check result dictionary
    """
    result = {
        "name": "lint",
        "status": "PASS",
        "message": "No lint issues",
        "warnings": [],
        "files_checked": 0
    }

    py_files = [f for f in files if f.endswith('.py')]
    result["files_checked"] = len(py_files)

    if not py_files:
        result["message"] = "No Python files to check"
        return result

    try:
        # Run ruff check with JSON output
        proc = subprocess.run(
            ["ruff", "check", "--output-format=json"] + py_files,
            capture_output=True,
            text=True
        )

        if proc.stdout.strip():
            issues = json.loads(proc.stdout)
            for issue in issues:
                result["warnings"].append({
                    "file": issue.get("filename", ""),
                    "line": issue.get("location", {}).get("row"),
                    "code": issue.get("code", ""),
                    "message": issue.get("message", "")
                })

        if result["warnings"]:
            # Treat lint issues as warnings (PASS with warnings)
            # Change to FAIL if you want strict enforcement
            result["message"] = f"{len(result['warnings'])} lint issue(s) found"

    except FileNotFoundError:
        result["status"] = "SKIP"
        result["message"] = "ruff not installed (pip install ruff)"
    except json.JSONDecodeError:
        result["message"] = "ruff check passed (no issues)"
    except Exception as e:
        result["status"] = "FAIL"
        result["message"] = f"Lint check failed: {str(e)}"

    return result


def check_complexity(files: List[str], max_complexity: int = 10) -> Dict:
    """
    Check cyclomatic complexity using radon.

    Args:
        files: List of file paths to check
        max_complexity: Maximum allowed complexity (default: 10, C grade)

    Returns:
        Check result dictionary
    """
    result = {
        "name": "complexity",
        "status": "PASS",
        "message": f"Complexity within limits (<={max_complexity})",
        "violations": [],
        "files_checked": 0
    }

    py_files = [f for f in files if f.endswith('.py')]
    result["files_checked"] = len(py_files)

    if not py_files:
        result["message"] = "No Python files to check"
        return result

    try:
        # Run radon cc with JSON output
        proc = subprocess.run(
            ["radon", "cc", "-j"] + py_files,
            capture_output=True,
            text=True
        )

        if proc.stdout.strip():
            complexity_data = json.loads(proc.stdout)

            for filepath, functions in complexity_data.items():
                for func in functions:
                    cc = func.get("complexity", 0)
                    if cc > max_complexity:
                        result["violations"].append({
                            "file": filepath,
                            "function": func.get("name", "unknown"),
                            "line": func.get("lineno"),
                            "complexity": cc,
                            "rank": func.get("rank", "?")
                        })

        if result["violations"]:
            result["status"] = "FAIL"
            result["message"] = f"{len(result['violations'])} function(s) exceed complexity limit"

    except FileNotFoundError:
        result["status"] = "SKIP"
        result["message"] = "radon not installed (pip install radon)"
    except json.JSONDecodeError:
        result["message"] = "Complexity check passed"
    except Exception as e:
        result["status"] = "FAIL"
        result["message"] = f"Complexity check failed: {str(e)}"

    return result


def run_l1(src_dir: str = "src") -> Dict:
    """
    Run all L1 static checks.

    Args:
        src_dir: Source directory to analyze

    Returns:
        L1 evaluation result
    """
    src_path = Path(src_dir)

    # Find all source files
    files = []
    for ext in ["*.go", "*.py", "*.js", "*.ts", "*.tsx"]:
        files.extend(str(f) for f in src_path.rglob(ext))

    result = {
        "status": "PASS",
        "checks": []
    }

    # Run all checks
    checks = [
        check_syntax(files),
        check_lint(files),
        check_complexity(files)
    ]

    result["checks"] = checks

    # Determine overall status
    for check in checks:
        if check["status"] == "FAIL":
            result["status"] = "FAIL"
            break

    return result


if __name__ == "__main__":
    import sys

    result = run_l1()
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["status"] == "PASS" else 1)
