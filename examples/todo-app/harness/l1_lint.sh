#!/bin/bash
# L1: Static checks (lint, syntax, complexity)
# Requirements: pip install ruff radon

set -e
cd "$(dirname "$0")/.."

echo "  Checking Python syntax..."
python3 -m py_compile src/todo.py
echo "  ✓ Syntax OK"

# Check for required functions
for func in "def add_todo" "def list_todos" "def complete_todo"; do
    if ! grep -q "$func" src/todo.py; then
        echo "  ✗ Missing: $func"
        exit 1
    fi
done
echo "  ✓ Required functions found"

# Run ruff linter (if available)
if command -v ruff &> /dev/null; then
    echo "  Running ruff linter..."
    if ruff check src/ --quiet; then
        echo "  ✓ No lint issues"
    else
        echo "  ⚠ Lint issues found (non-blocking)"
    fi
else
    echo "  ⚠ ruff not installed, skipping lint"
fi

# Run complexity check (if available)
if command -v radon &> /dev/null; then
    echo "  Checking complexity..."
    # Check for high complexity (C grade or worse, complexity > 10)
    HIGH_CC=$(radon cc src/ -n C --total-average 2>/dev/null | grep -c "^src/" || true)
    if [ "$HIGH_CC" -gt 0 ]; then
        echo "  ⚠ $HIGH_CC function(s) with high complexity"
    else
        echo "  ✓ Complexity within limits"
    fi
else
    echo "  ⚠ radon not installed, skipping complexity"
fi
