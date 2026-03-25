#!/bin/bash

# ============================================
# ANRS Adapter Generator
# ============================================
# Usage: ./generate_adapters.sh [adapter_name]
#
# Generates adapter configuration from ANRS rules.
# ============================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

# Generate Cursor adapter
generate_cursor() {
    log_info "Generating Cursor adapter..."
    
    local output="$PROJECT_ROOT/adapters/cursor/.cursorrules"
    
    # Adapter already exists as template
    # In full implementation, this would read from ai/rules/constraints.json
    # and generate the .cursorrules file dynamically
    
    log_info "Cursor adapter: $output"
}

# Generate Claude adapter
generate_claude() {
    log_info "Generating Claude adapter..."
    
    local output="$PROJECT_ROOT/adapters/claude/system-prompt.txt"
    
    # Adapter already exists as template
    
    log_info "Claude adapter: $output"
}

# Generate OpenAI adapter
generate_openai() {
    log_info "Generating OpenAI adapter..."
    
    local output="$PROJECT_ROOT/adapters/openai/agent-config.json"
    
    # Adapter already exists as template
    
    log_info "OpenAI adapter: $output"
}

# Generate all adapters
generate_all() {
    log_info "Generating all adapters..."
    generate_cursor
    generate_claude
    generate_openai
}

# Main
main() {
    local adapter=${1:-"all"}
    
    log_info "=== ANRS Adapter Generator ==="
    log_info "Source: ai/rules/constraints.json"
    echo ""
    
    case $adapter in
        cursor)
            generate_cursor
            ;;
        claude)
            generate_claude
            ;;
        openai)
            generate_openai
            ;;
        all)
            generate_all
            ;;
        *)
            echo "Unknown adapter: $adapter"
            echo "Available: cursor, claude, openai, all"
            exit 1
            ;;
    esac
    
    echo ""
    log_info "Done!"
    log_warn "Note: Full generation from constraints.json is not yet implemented."
    log_warn "Current adapters are pre-built templates."
}

main "$@"
