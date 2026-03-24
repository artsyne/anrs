#!/bin/bash
# AHES Harness Runner - Todo App Example
# Runs L1 → L2 → L3 cascade evaluation

set -e
cd "$(dirname "$0")/.."

echo "========================================="
echo "AHES Harness - Todo App"
echo "========================================="
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
