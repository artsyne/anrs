# ANRS Documentation

> Documentation hub for ANRS (AI-Native Repo Spec) - A practical specification for structuring AI-friendly code repositories.

## Quick Start

| Guide | Description |
|-------|-------------|
| [Getting Started](getting-started.md) | 5-minute quick start guide |
| [Installation](installation.md) | Detailed installation options (minimal/standard/full) |
| [Migration](migration.md) | Migrate existing projects to ANRS |

## Core Concepts

| Topic | Description |
|-------|-------------|
| [Overview](concepts/overview.md) | System architecture and data flow |
| [State](concepts/state.md) | Single Source of Truth (SSOT) for AI execution |
| [Skills](concepts/skills.md) | Registered action templates with schemas |
| [Harness](concepts/harness.md) | Multi-layer quality gate (L1/L2/L3) |
| [Adapters](concepts/adapters.md) | AI platform integrations (Cursor, Claude, Codex) |

## CLI Reference

See [API Reference](api-reference.md) for complete CLI documentation.

```bash
# Initialize project
anrs init [--level minimal|standard|full] [--adapter cursor|claude-code]

# Check status
anrs status

# Install adapter
anrs adapter list
anrs adapter install cursor [--force|--skip]

# Upgrade to latest
anrs upgrade [--dry-run]

# Run quality checks
anrs harness [--level L1|L2|L3|all]
```

See [Installation Guide](installation.md) for full CLI documentation.

## Examples

After installing ANRS in your project:

```bash
anrs init --level standard
anrs adapter install cursor
anrs status
```

See [Getting Started](getting-started.md) for a complete walkthrough.

## Additional Resources

| Resource | Description |
|----------|-------------|
| [Design Docs](design-docs/) | Internal design documents and RFCs |
| [Generated](generated/) | Auto-generated API documentation |
| [Contributing](../CONTRIBUTING.md) | How to contribute to ANRS |
| [Changelog](../CHANGELOG.md) | Version history and changes |

## Project Structure

```
anrs/
├── cli/               # CLI tool (pip install anrs)
│   ├── data/
│   │   ├── adapters/  # AI platform adapters (Cursor, Claude, Codex)
│   │   └── templates/ # Init templates (minimal/standard/full)
│   ├── src/           # CLI source code
│   └── tests/         # Unit tests (98% coverage)
├── docs/              # This documentation
└── spec/              # Protocol specification
    ├── ENTRY.md       # AI entry point template
    ├── rules/         # Global constraints
    ├── skills/        # Skill definitions
    └── state/         # State schema
```
