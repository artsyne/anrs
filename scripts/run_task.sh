#!/bin/bash

# ============================================
# AHES Task Runner
# ============================================
# Usage: ./run_task.sh [task_id]
# 
# Executes a task following the AHES protocol.
# ============================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Read current state
read_state() {
    if [ -f "$PROJECT_ROOT/ai/state/state.json" ]; then
        cat "$PROJECT_ROOT/ai/state/state.json"
    else
        log_error "State file not found!"
        exit 1
    fi
}

# Check if task exists
check_task() {
    local task_id=$1
    local task_file="$PROJECT_ROOT/plans/active/$task_id.md"
    
    if [ ! -f "$task_file" ]; then
        log_error "Task file not found: $task_file"
        exit 1
    fi
    
    log_info "Found task: $task_file"
}

# Main execution
main() {
    local task_id=${1:-"task-001"}
    
    log_info "=== AHES Task Runner ==="
    log_info "Task ID: $task_id"
    
    # Step 1: Read state
    log_info "Step 1: Reading state..."
    read_state > /dev/null
    
    # Step 2: Check task exists
    log_info "Step 2: Checking task..."
    check_task "$task_id"
    
    # Step 3: Execute (placeholder - actual execution would be AI-driven)
    log_info "Step 3: Task ready for execution"
    log_info "Use your AI assistant with ai/ENTRY.md as entry point"
    
    # Step 4: Run harness
    log_info "Step 4: To run harness, use: ./scripts/run_harness.sh"
    
    log_info "=== Done ==="
}

main "$@"
