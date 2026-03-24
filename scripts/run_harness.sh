#!/bin/bash

# ============================================
# AHES Harness Runner
# ============================================
# Usage: ./run_harness.sh [--level L1|L2|L3] [--verbose]
#
# Runs the quality gate evaluation cascade.
# ============================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Default values
LEVEL="L3"
VERBOSE=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --level)
            LEVEL="$2"
            shift 2
            ;;
        --verbose|-v)
            VERBOSE="--verbose"
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo "🧪 AHES Harness Runner"
echo "======================"
echo "Level: $LEVEL"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR]${NC} Python 3 is required but not installed."
    exit 1
fi

# Run quality gate
cd "$PROJECT_ROOT"
python3 harness/quality_gate.py --level "$LEVEL" $VERBOSE

# Check result
RESULT=$(python3 -c "import json; print(json.load(open('harness/reports/latest.json'))['result'])")

echo ""
if [ "$RESULT" == "PASS" ]; then
    echo -e "${GREEN}✅ Harness PASSED${NC}"
    exit 0
else
    echo -e "${RED}❌ Harness FAILED${NC}"
    echo "See harness/reports/latest.json for details"
    exit 1
fi
