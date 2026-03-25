# ANRS: AI-Native Repo Spec

> A practical specification for structuring AI-friendly code repositories.

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.1-blue.svg)]()
[![Standard](https://img.shields.io/badge/AI%20Native-Repo%20Spec-green.svg)]()

---

## What is ANRS?

ANRS (AI-Native Repo Spec) is a vendor-neutral specification that defines how to structure a repository so that AI agents can work within it safely and effectively.

When AI agents operate in traditional codebases, they often lose track of their current task, hallucinate commands, or modify unrelated files. ANRS solves this by providing a standard set of boundaries and context:

- **Explicit State (`state.json`)** — Replaces fragile chat history. The AI always reads this file first to know "what task I am doing" and "what step I am on."
- **Defined Skills (`skills/`)** — Replaces open-ended guessing. The AI is restricted to documented checklists, preventing undefined behaviors.
- **Mandatory Harness (`harness/`)** — Replaces blind commits. AI-generated code must pass checks and tests before task completion.

> **Note**: ANRS is a **specification**, not a runtime tool. It's a standardized folder structure (`ai/`, `harness/`, `plans/`) plus execution protocols that any AI tool can follow.

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
1. READ STATE    → ai/state/state.json
2. LOAD PLAN     → plans/active/{task_id}.md
3. SELECT SKILL  → ai/skills/index.json
4. EXECUTE       → Follow SKILL.md checklist
5. RUN HARNESS   → L1 (Static) → L2 (Tests) → L3 (Stability)

PASS → Atomic commit → Update state → Done
FAIL → Reflect → Retry (max 3) → Escalate to human
```

---

## Quick Start

### Option 1: Try the Example

```bash
git clone https://github.com/artsyne/anrs.git
cd anrs/examples/hello-world
cat README.md
```

### Option 2: Apply to Your Project

```bash
git clone https://github.com/artsyne/anrs.git
cp -r anrs/ai your-project/
cp -r anrs/harness your-project/
```

Point your AI tool to `ai/ENTRY.md` as the entry point.

### Option 3: Configure Your AI Platform

ANRS provides ready-to-use adapters with **multi-mode support** (build/plan/review):

| Platform | Modes | Quick Start |
|----------|-------|-------------|
| **Claude Code** | build, plan, review | `cp adapters/claude-code/CLAUDE.md .` |
| **Cursor** | build, plan | `cp adapters/cursor/.cursorrules .` |
| **Codex** | build, plan, review | `cp adapters/codex/AGENTS.md .` |
| **OpenCode** | build, plan, review | Copy `adapters/opencode/` to `.opencode/` |

```bash
# Cursor (build mode)
cp adapters/cursor/.cursorrules your-project/.cursorrules

# Cursor (plan mode - read only)
cp adapters/cursor/modes/cursorrules-plan your-project/.cursorrules
```

See [adapters/README.md](adapters/README.md) for all platforms and modes.

---

## Core Concepts

**State (SSOT)** — `ai/state/state.json` — Single Source of Truth for task state. AI reads this before any action.

**Orchestrator** — `ai/orchestrator/ORCHESTRATOR.md` — Defines the execution protocol (Read → Plan → Execute → Verify loop). Supports sequential and parallel (subagent) execution modes.

**Skills** — `ai/skills/index.json` — 15 registered action templates with input/output schemas and constraints.

**Harness** — `harness/quality_gate.py` — Multi-layer evaluation gate (Security → L1: static → L2: tests → L3: stability).

---

## Key Files Reference

- `ai/ENTRY.md` — AI agent entry point
- `ai/rules/global.md` — Global constraints (must follow)
- `ai/rules/constraints.json` — Machine-readable rules
- `ai/skills/index.json` — Skill registry
- `harness/error_codes.json` — Error code definitions for reflection

---

## Documentation

- [Hello World Example](examples/hello-world/) — 5-minute quick start
- [Todo App Example](examples/todo-app/) — Complete workflow demo
- [Core Beliefs](docs/core-beliefs.md) — Design principles
- [System Architecture](docs/architecture/system.md) — Technical design
- [Architecture Graph](docs/references/architecture-graph.md) — Component relationships
- [API Contracts](docs/references/api-contracts.md) — Endpoint definitions
- [Contributing Guide](CONTRIBUTING.md) — How to contribute

---

## License

MIT License — See [LICENSE](LICENSE) for details.
