#!/bin/bash
# L2: Dynamic tests (unit tests)

set -e
cd "$(dirname "$0")/.."

# Run pytest
python3 -m pytest tests/ -v --tb=short

echo "  All tests passed"
