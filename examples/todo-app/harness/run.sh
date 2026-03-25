#!/bin/bash
# ANRS Harness Runner - Todo App Example
# Runs Security → L1 → L2 → L3 cascade evaluation
#
# Requirements:
#   pip install ruff radon pytest pytest-cov bandit
#   brew install gitleaks  # optional

set -e
cd "$(dirname "$0")/.."

echo "========================================="
echo "ANRS Harness - Todo App"
echo "========================================="
echo ""

# Security: Run security checks first (cross-level)
echo "[Security] Running security scans..."
SEC_FAIL=0

# Secret detection (if gitleaks available)
if command -v gitleaks &> /dev/null; then
    echo "  Checking for secrets..."
    if gitleaks detect --source . --no-git -q 2>/dev/null; then
        echo "  ✓ No secrets detected"
    else
        echo "  ✗ Secrets detected!"
        SEC_FAIL=1
    fi
else
    echo "  ⚠ gitleaks not installed, skipping secret detection"
fi

# SAST with bandit (if available)
if command -v bandit &> /dev/null; then
    echo "  Running SAST scan..."
    if bandit -r src/ -ll -q 2>/dev/null; then
        echo "  ✓ No high-severity issues"
    else
        echo "  ✗ Security issues found!"
        SEC_FAIL=1
    fi
else
    echo "  ⚠ bandit not installed, skipping SAST"
fi

if [ $SEC_FAIL -ne 0 ]; then
    echo "✗ Security checks FAILED"
    exit 1
fi
echo "✓ Security Passed"
echo ""

# L1: Static Checks
echo "[L1] Running static checks..."
./harness/l1_lint.sh
echo "✓ L1 Passed"
echo ""

# L2: Dynamic Tests
echo "[L2] Running tests..."
./harness/l2_test.sh
echo "✓ L2 Passed"
echo ""

# L3: Risk Analysis
echo "[L3] Running risk analysis..."
./harness/l3_risk.sh
echo "✓ L3 Passed"
echo ""

echo "========================================="
echo "✓ ALL CHECKS PASSED"
echo "========================================="
