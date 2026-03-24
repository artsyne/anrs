#!/bin/bash
# Simple L1 harness check for hello-world example

set -e

echo "Running L1 checks..."

# Check if greet function exists
if grep -q "def greet" src/hello.py; then
    echo "✓ greet() function found"
else
    echo "✗ greet() function not found"
    exit 1
fi

# Check syntax
python3 -m py_compile src/hello.py
echo "✓ Syntax OK"

# Run basic test
OUTPUT=$(python3 -c "from src.hello import greet; print(greet('World'))" 2>/dev/null || echo "FAIL")
if [[ "$OUTPUT" == *"Hello"* ]]; then
    echo "✓ Function works correctly"
else
    echo "✗ Function output incorrect: $OUTPUT"
    exit 1
fi

echo ""
echo "========================================="
echo "✓ L1 Check Passed"
echo "========================================="
