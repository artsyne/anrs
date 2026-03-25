# Installation Guide

Detailed installation instructions for ANRS.

## Installation Levels

ANRS supports three installation levels:

| Level | Command | Includes |
|-------|---------|----------|
| Minimal | `anrs init --level minimal` | `.anrs/` (ENTRY, state, config) |
| Standard | `anrs init` | + scratchpad, plans/ |
| Full | `anrs init --level full` | + skills/, failure-cases/, harness/ |

## CLI Installation

### From PyPI (Recommended)

```bash
pip install anrs
```

### From Source

```bash
git clone https://github.com/artsyne/anrs.git
cd anrs/cli
pip install -e .
```

## Project Setup

### Initialize

```bash
# Standard setup (recommended)
anrs init

# Minimal setup
anrs init --level minimal

# Full setup with harness
anrs init --level full

# Specify path
anrs init /path/to/project
```

### Install Adapter

```bash
# List available adapters
anrs adapter list

# Install specific adapter
anrs adapter install cursor
anrs adapter install claude-code
anrs adapter install codex
```

### Verify Installation

```bash
anrs status
```

## Directory Structure

After `anrs init` (standard):

```
your-project/
├── .anrs/
│   ├── ENTRY.md          # AI entry point
│   ├── state.json        # Current state (SSOT)
│   ├── config.json       # Project configuration
│   ├── scratchpad.md     # Temporary notes
│   └── plans/
│       ├── active/       # Current tasks
│       ├── backlog/      # Future tasks
│       ├── completed/    # Archived tasks
│       └── templates/    # Task templates
├── .cursorrules          # Adapter (if installed)
└── ... (your code)
```

After `anrs init --level full`:

```
your-project/
├── .anrs/
│   ├── ...               # (all standard files)
│   ├── skills/           # Custom skill definitions
│   └── failure-cases/    # Failed attempt archive
├── harness/              # Quality gate (at root for CI/CD)
└── ... (your code)
```

## Upgrading

```bash
# Upgrade .anrs/ to latest version
anrs upgrade

# Preview changes without applying
anrs upgrade --dry-run
```

## Uninstalling

To remove ANRS from a project:

```bash
rm -rf .anrs/
rm -rf harness/          # if full level
rm .cursorrules          # or other adapter files
```
