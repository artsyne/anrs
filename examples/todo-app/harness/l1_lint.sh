#!/bin/bash
# L1: Static checks (lint, syntax)

set -e
cd "$(dirname "$0")/.."

# Check Python syntax
python3 -m py_compile src/todo.py

# Check for required functions
for func in "def add_todo" "def list_todos" "def complete_todo"; do
    if ! grep -q "$func" src/todo.py; then
        echo "✗ Missing: $func"
        exit 1
    fi
done

echo "  Syntax OK"
echo "  Required functions found"
