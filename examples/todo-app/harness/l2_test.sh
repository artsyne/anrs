#!/bin/bash
# L2: Dynamic tests (unit tests with coverage)
# Requirements: pip install pytest pytest-cov

set -e
cd "$(dirname "$0")/.."

MIN_COVERAGE=70

# Run pytest with coverage (if pytest-cov available)
if python3 -c "import pytest_cov" 2>/dev/null; then
    echo "  Running tests with coverage..."
    python3 -m pytest tests/ -v --tb=short --cov=src --cov-report=term-missing --cov-fail-under=$MIN_COVERAGE
    echo "  ✓ All tests passed with coverage >= ${MIN_COVERAGE}%"
else
    echo "  Running tests (no coverage)..."
    python3 -m pytest tests/ -v --tb=short
    echo "  ✓ All tests passed"
    echo "  ⚠ pytest-cov not installed, skipping coverage"
fi
