# ANRS: AI-Native Repo Spec

> A practical specification for structuring AI-friendly code repositories.

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.1-blue.svg)]()
[![Standard](https://img.shields.io/badge/AI%20Native-Repo%20Spec-green.svg)]()

[English](README.md) | [中文](README.zh.md)

---

## What is ANRS?

ANRS (AI-Native Repo Spec) is a vendor-neutral specification that defines how to structure a repository so that AI agents can work within it safely and effectively.

When AI agents operate in traditional codebases, they often lose track of their current task, hallucinate commands, or modify unrelated files. ANRS solves this by providing a standard set of boundaries and context:

- **Explicit State (`.anrs/state.json`)** — Replaces fragile chat history. The AI always reads this file first to know "what task I am doing" and "what step I am on."
- **Defined Skills (`.anrs/skills/`)** — Replaces open-ended guessing. The AI is restricted to documented checklists, preventing undefined behaviors.
- **Mandatory Harness (`.anrs/harness/`)** — Replaces blind commits. AI-generated code must pass checks and tests before task completion.

> **Note**: ANRS is a **specification**, not a runtime tool. It's a standardized folder structure (`.anrs/`) plus execution protocols that any AI tool can follow.

---

## Design Principles

- **Deterministic Execution** — AI follows a fixed loop: Read → Plan → Execute → Verify.
- **Atomic Changes** — Code and state update together. Always rollback-safe.
- **Vendor Neutral** — Works with Cursor, Claude, Codex, and others.
- **Layered Verification** — Security → Lint → Test → Risk. Gate before commit.
- **Learn from Failures** — Failed attempts are archived for future reference.

---

## Architecture Overview

```
                    ANRS Framework

    State (SSOT)  →  Orchestrator  →  Skills
         ↑              |              |
         |              v              v
         |           Harness  ←───  Code
         |              |
         |         [ PASS? ]
         |          /     \
         |        YES      NO
         |         |        |
         └── Commit       Reflection → Retry
```

---

## Execution Workflow

```
1. READ STATE    → .anrs/state.json
2. LOAD PLAN     → .anrs/plans/active/{task_id}.md
3. SELECT SKILL  → .anrs/skills/index.json
4. EXECUTE       → Follow SKILL.md checklist
5. RUN HARNESS   → L1 (Static) → L2 (Tests) → L3 (Stability)

PASS → Atomic commit → Update state → Done
FAIL → Reflect → Retry (max 3) → Escalate to human
```

---

## Quick Start

### Option 1: Use CLI (Recommended)

```bash
pip install anrs
cd your-project
anrs init                    # Standard setup
anrs adapter install cursor  # Add AI adapter
```

This creates:
```
your-project/
├── .anrs/
│   ├── ENTRY.md      # AI reads this first
│   ├── state.json    # Current state (SSOT)
│   ├── config.json   # Configuration
│   ├── scratchpad.md # Temporary notes
│   └── plans/        # Task plans
│       ├── active/   # Current tasks
│       ├── backlog/  # Future tasks
│       └── templates/
└── .cursorrules      # AI adapter
```

### Option 2: Explore the Source

```bash
git clone https://github.com/artsyne/anrs.git
cd anrs
ls -la spec/      # Protocol specification templates
ls -la cli/       # CLI tool source code
```

### Option 3: Configure Your AI Platform

ANRS provides ready-to-use adapters with **multi-mode support** (build/plan/review):

| Platform | Modes | Quick Start |
|----------|-------|--------------|
| **Cursor** | build, plan | `anrs adapter install cursor` |
| **Claude Code** | build, plan, review | `anrs adapter install claude-code` |
| **Codex** | build, plan, review | `anrs adapter install codex` |
| **OpenCode** | build, plan, review | `anrs adapter install opencode` |

See [adapters documentation](cli/src/anrs/data/adapters/README.md) for manual setup and mode switching.

---

## Core Concepts

**State (SSOT)** — `.anrs/state.json` — Single Source of Truth for task state. AI reads this before any action.

**Entry Point** — `.anrs/ENTRY.md` — AI agent entry point. Defines rules, constraints, and available skills.

**Skills** — `.anrs/skills/` — Registered action templates with input/output schemas and constraints.

**Harness** — `.anrs/harness/quality_gate.py` (full level) or `anrs harness` command — Multi-layer evaluation gate (Security → L1: static → L2: tests → L3: stability).

---

## Key Files Reference

| File | Description |
|------|-------------|
| `.anrs/ENTRY.md` | AI agent entry point |
| `.anrs/state.json` | Current execution state |
| `.anrs/config.json` | Project configuration |
| `.anrs/plans/active/` | Active task plans |
| `.anrs/harness/` | Quality gate evaluators (full level) |

---

## Documentation

- [Getting Started](docs/getting-started.md) — 5-minute quick start
- [Installation Guide](docs/installation.md) — Setup options (minimal/standard/full)
- [Core Concepts](docs/concepts/overview.md) — Architecture and data flow
- [Core Beliefs](spec/core-beliefs.md) — Design principles
- [Contributing Guide](CONTRIBUTING.md) — How to contribute

---

## License

MIT License — See [LICENSE](LICENSE) for details.
