# ANRS Documentation

> **AI-Native Repository Specification** - A practical specification for structuring AI-friendly code repositories.

---

## What is ANRS?

ANRS defines how to structure a repository so that AI agents can work within it **safely** and **effectively**.

<div class="grid cards" markdown>

-   :material-state-machine:{ .lg .middle } __Explicit State__

    ---

    Single source of truth for AI execution. No more fragile chat history.

    [:octicons-arrow-right-24: Learn about State](concepts/state.md)

-   :material-format-list-checks:{ .lg .middle } __Defined Skills__

    ---

    AI operates within documented boundaries. No undefined behaviors.

    [:octicons-arrow-right-24: Explore Skills](concepts/skills.md)

-   :material-check-decagram:{ .lg .middle } __Mandatory Harness__

    ---

    Every change must pass verification. No blind commits.

    [:octicons-arrow-right-24: Understand Harness](concepts/harness.md)

</div>

## Quick Start

```bash
# Install CLI
pip install anrs

# Initialize in your project
cd your-project
anrs init

# Add AI adapter
anrs adapter install cursor

# Check status
anrs status
```

[:octicons-arrow-right-24: Full Getting Started Guide](getting-started.md)

## Why ANRS?

Traditional AI assistants are **unpredictable**, **unverified**, and have **no rollback** capability.

ANRS treats AI as a **constrained executor**, not an autonomous agent:

| Traditional AI | ANRS |
|---------------|------|
| Fragile chat history | Persistent state file |
| Open-ended guessing | Documented skill checklists |
| Blind commits | Mandatory harness checks |
| No rollback | Atomic changes + backups |

## Design Principles

- **Deterministic Execution** — AI follows a fixed loop: Read → Plan → Execute → Verify
- **Atomic Changes** — Code and state update together. Always rollback-safe.
- **Vendor Neutral** — Works with Cursor, Claude, Codex, and others.
- **Layered Verification** — Security → Lint → Test → Risk. Gate before commit.

## Installation Levels

| Level | What You Get |
|-------|--------------|
| `minimal` | `.anrs/` with ENTRY, state, config |
| `standard` | + plans/, scratchpad *(default)* |
| `full` | + skills/, harness/, failure-cases/ |

```bash
anrs init --level full
```

## Supported AI Tools

| Platform | Command |
|----------|---------|
| Cursor | `anrs adapter install cursor` |
| Claude Code | `anrs adapter install claude-code` |
| Codex | `anrs adapter install codex` |
| OpenCode | `anrs adapter install opencode` |

## Project Status

- **Specification**: v1.0.0 (Stable)
- **CLI**: v0.1.0 (Alpha)
- **Test Coverage**: 97%

## Next Steps

<div class="grid cards" markdown>

-   [:octicons-rocket-24: Getting Started](getting-started.md)

    5-minute quick start guide

-   [:octicons-download-24: Installation](installation.md)

    Detailed installation options

-   [:octicons-book-24: Core Concepts](concepts/overview.md)

    Understand the architecture

-   [:octicons-code-24: CLI Reference](api-reference.md)

    Complete command documentation

</div>
