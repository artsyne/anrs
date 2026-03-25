# ANRS CLI

Command-line tool for managing ANRS-compliant repositories.

## Installation

```bash
# From source
cd cli
pip install -e .

# Or with dev dependencies
pip install -e ".[dev]"
```

## Usage

```bash
# Initialize ANRS in a repository
anrs init                    # Standard level
anrs init --level minimal    # Minimal setup
anrs init --level full       # Full setup

# Check repository status
anrs status

# Run quality checks
anrs harness                 # All levels
anrs harness --level L1      # Static checks only
anrs harness --strict        # Fail on any error

# Manage adapters
anrs adapter list
anrs adapter install cursor
anrs adapter install claude-code
```

## Commands

| Command | Description |
|---------|-------------|
| `anrs init` | Initialize ANRS in a repository |
| `anrs status` | Show ANRS status and current state |
| `anrs harness` | Run quality gate checks |
| `anrs adapter` | Install and manage AI tool adapters |

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=anrs --cov-report=html
```
