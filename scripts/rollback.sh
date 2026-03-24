#!/bin/bash

# ============================================
# AHES Rollback Script
# ============================================
# Usage: ./rollback.sh [commit_hash]
#
# Safely rollback to a previous commit.
# ============================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if git is available
check_git() {
    if ! command -v git &> /dev/null; then
        log_error "Git is required but not installed."
        exit 1
    fi
    
    if ! git rev-parse --is-inside-work-tree &> /dev/null; then
        log_error "Not a git repository."
        exit 1
    fi
}

# Check for uncommitted changes
check_clean() {
    if ! git diff --quiet || ! git diff --cached --quiet; then
        log_warn "You have uncommitted changes."
        read -p "Continue anyway? (y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

# Perform rollback
rollback() {
    local target=$1
    
    log_info "Rolling back to: $target"
    
    # Create a backup branch
    local backup_branch="backup-$(date +%Y%m%d-%H%M%S)"
    git branch "$backup_branch"
    log_info "Created backup branch: $backup_branch"
    
    # Perform soft reset (keeps changes staged)
    git reset --soft "$target"
    log_info "Reset to $target"
    
    # Show status
    log_info "Current status:"
    git status --short
}

# Main
main() {
    local target=${1:-"HEAD~1"}
    
    log_info "=== AHES Rollback Script ==="
    
    check_git
    check_clean
    
    log_warn "This will rollback to: $target"
    read -p "Are you sure? (y/N) " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rollback "$target"
        log_info "Rollback complete."
        log_info "To restore: git checkout backup-* && git cherry-pick HEAD"
    else
        log_info "Rollback cancelled."
    fi
}

main "$@"
