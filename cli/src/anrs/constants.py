"""ANRS CLI constants and configuration."""

import logging
from pathlib import Path
from typing import Dict, List, Tuple

# CLI directory (cli/src/anrs/constants.py -> cli/src/anrs -> cli/src -> cli)
CLI_DIR = Path(__file__).parent.parent.parent

# Data directories
DATA_DIR = CLI_DIR / "data"
TEMPLATES_DIR = DATA_DIR / "templates"
ADAPTERS_DIR = DATA_DIR / "adapters"

# Manifest and template paths
MANIFESTS_DIR = TEMPLATES_DIR / "manifests"
FILES_DIR = TEMPLATES_DIR / "files"

# Supported adapters and their config files
ADAPTERS: Dict[str, Dict[str, str]] = {
    "cursor": {
        "name": "Cursor AI",
        "config_file": ".cursorrules",
        "description": "Cursor AI editor integration",
    },
    "claude-code": {
        "name": "Claude Code",
        "config_file": "CLAUDE.md",
        "description": "Anthropic Claude Code integration",
    },
    "codex": {
        "name": "OpenAI Codex",
        "config_file": "AGENTS.md",
        "description": "OpenAI Codex CLI integration",
    },
    "opencode": {
        "name": "OpenCode",
        "config_file": "opencode.json",
        "description": "OpenCode AI integration",
    },
}

# Installation levels
LEVELS = ["minimal", "standard", "full"]
DEFAULT_LEVEL = "standard"

# Harness levels
HARNESS_LEVELS = ["L1", "L2", "L3", "security", "all"]
HARNESS_SCRIPTS = {
    "L1": "l1_lint.sh",
    "L2": "l2_test.sh",
    "L3": "l3_risk.sh",
    "security": "security_scan.sh",
}

# Fields to preserve during upgrade
PRESERVE_FIELDS = [
    "current_task",
    "status",
    "last_completed",
    "history",
    "context",
    "project",
]

# Logging configuration
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = logging.INFO


def get_adapter_config_file(adapter_name: str) -> str:
    """Get config file name for an adapter."""
    if adapter_name not in ADAPTERS:
        raise ValueError(f"Unknown adapter: {adapter_name}")
    return ADAPTERS[adapter_name]["config_file"]


def get_adapter_files(adapter_name: str) -> List[Tuple[str, str]]:
    """Get list of (source, target) file pairs for an adapter."""
    config_file = get_adapter_config_file(adapter_name)
    return [(config_file, config_file)]
