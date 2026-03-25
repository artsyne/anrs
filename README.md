# ANRS: AI-Native Repo Spec

> A deterministic, transactional framework for AI-friendly repository governance.

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.1-blue.svg)]()
[![Standard](https://img.shields.io/badge/AI%20Native-Repo%20Spec-green.svg)]()

---

## What is ANRS?

ANRS (AI-Native Repo Spec) is a vendor-neutral specification framework that defines how to structure a repository to be AI-friendly and AI-safe. It provides a rigorous execution protocol and multi-layer evaluation harness for AI-driven software engineering.

Traditional AI coding often suffers from "Context Drift" and "Instruction Decay." ANRS addresses this by introducing a System of Record (SSOT) for AI agents:

- **State-Aware** — AI always knows "where it is" via a machine-readable `state.json`
- **Skill-Bound** — AI is restricted to a whitelist of registered Skills, preventing undefined operations
- **Harness-Governed** — No code is considered complete until it passes the mandatory multi-stage evaluation

> **Note**: ANRS is a **specification framework**, not a production-ready tool. The harness evaluators are protocol skeletons demonstrating the expected interfaces. The example code is intentionally incomplete — it serves as a scenario for AI agents to practice following the ANRS protocol.

---

## Core

**Deterministic Orchestration** — Every AI action follows a defined execution loop (Read → Plan → Execute → Verify), ensuring consistent results regardless of the underlying model.

**Transactional Integrity** — Code changes and state updates are treated as a single atomic unit. The codebase remains in a valid, reversible state at all times.

**Vendor Agnostic** — Through its adapter layer, ANRS bridges different AI ecosystems (Cursor, Claude, OpenAI, open-source models) without vendor lock-in.

**Multi-Layer Verification** — A quadruple-layer gate—security checks, static checks (L1), functional tests (L2), and stability audits (L3)—ensures production-grade reliability.

**Closed-Loop Evolution** — Systematic capture and analysis of failure cases creates a feedback loop for self-correction.

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
