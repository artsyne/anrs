# AHES: AI Harness Engineering Standard

> A deterministic, transactional framework for AI-driven development.

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.1-blue.svg)]()
[![Standard](https://img.shields.io/badge/AI%20Native-Repo%20Spec-green.svg)]()

---

## What is AHES?

AHES (AI Harness Engineering Standard) is a vendor-neutral, transactional framework that defines a rigorous execution protocol and multi-layer evaluation harness for AI-driven software engineering.

Traditional AI coding often suffers from "Context Drift" and "Instruction Decay." AHES addresses this by introducing a System of Record (SSOT) for AI agents:

- **State-Aware** — AI always knows "where it is" via a machine-readable `state.json`
- **Skill-Bound** — AI is restricted to a whitelist of registered Skills, preventing undefined operations
- **Harness-Governed** — No code is considered complete until it passes the mandatory multi-stage evaluation

> **Note**: AHES is a **specification framework**, not a production-ready tool. The harness evaluators are protocol skeletons demonstrating the expected interfaces. The example code is intentionally incomplete — it serves as a scenario for AI agents to practice following the AHES protocol.

---

## Core

**Deterministic Orchestration** — Every AI action follows a defined execution loop (Read → Plan → Execute → Verify), ensuring consistent results regardless of the underlying model.

**Transactional Integrity** — Code changes and state updates are treated as a single atomic unit. The codebase remains in a valid, reversible state at all times.

**Vendor Agnostic** — Through its adapter layer, AHES bridges different AI ecosystems (Cursor, Claude, OpenAI, open-source models) without vendor lock-in.

**Multi-Layer Verification** — A triple-layer gate—static checks (L1), functional tests (L2), and stability audits (L3)—ensures production-grade reliability.

**Closed-Loop Evolution** — Systematic capture and analysis of failure cases creates a feedback loop for self-correction.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        AHES Framework                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐    ┌──────────────┐    ┌──────────┐               │
│  │  State   │───▶│ Orchestrator │───▶│  Skills  │               │
│  │  (SSOT)  │    │  (Protocol)  │    │ (Engine) │               │
│  └──────────┘    └──────────────┘    └──────────┘               │
│       │                │                   │                     │
│       │                ▼                   ▼                     │
│       │         ┌──────────────┐    ┌──────────┐                │
│       │         │   Harness    │◀───│   Code   │                │
│       │         │  (Evaluator) │    │  (src/)  │                │
│       │         └──────────────┘    └──────────┘                │
│       │                │                                         │
│       │                ▼                                         │
│       │    ┌─────────────────────────┐                          │
│       │    │     PASS?               │                          │
│       │    └─────────────────────────┘                          │
│       │         │            │                                   │
│       │        YES          NO                                   │
│       │         │            │                                   │
│       │         ▼            ▼                                   │
│       │    ┌────────┐   ┌────────────┐                          │
│       └────│ Commit │   │ Reflection │──▶ Retry Loop            │
│            └────────┘   └────────────┘                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Execution Workflow

The following diagram shows how a task flows through the AHES pipeline:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         TASK EXECUTION WORKFLOW                          │
└─────────────────────────────────────────────────────────────────────────┘

  ┌──────────┐
  │  START   │
  │  Task    │
  └────┬─────┘
       │
       ▼
  ┌──────────────────────────────────────────────────────────────────┐
  │  1. READ STATE                                                    │
  │     └─▶ ai/state/state.json (get current context)                │
  └────┬─────────────────────────────────────────────────────────────┘
       │
       ▼
  ┌──────────────────────────────────────────────────────────────────┐
  │  2. LOAD PLAN                                                     │
  │     └─▶ plans/active/{task_id}.md (get execution steps)          │
  └────┬─────────────────────────────────────────────────────────────┘
       │
       ▼
  ┌──────────────────────────────────────────────────────────────────┐
  │  3. SELECT & EXECUTE SKILL                                        │
  │     └─▶ ai/skills/{category}/{skill}/SKILL.md                    │
  │     └─▶ Modify src/ according to skill checklist                 │
  └────┬─────────────────────────────────────────────────────────────┘
       │
       ▼
  ┌──────────────────────────────────────────────────────────────────┐
  │  4. HARNESS EVALUATION (Cascade)                                  │
  │                                                                   │
  │     ┌─────────┐     ┌─────────┐     ┌─────────┐                  │
  │     │   L1    │────▶│   L2    │────▶│   L3    │                  │
  │     │ Static  │     │ Dynamic │     │Stability│                  │
  │     └────┬────┘     └────┬────┘     └────┬────┘                  │
  │          │               │               │                        │
  │     • Syntax         • Unit Tests    • Risk Analysis              │
  │     • Lint           • Coverage      • SLO Validation            │
  │     • Complexity     • Contracts     • Chaos (optional)          │
  │                                                                   │
  │     ⚠️  Fail at any level → Stop cascade, enter reflection       │
  └────┬─────────────────────────────────────────────────────────────┘
       │
       ▼
  ┌─────────────┐
  │   RESULT?   │
  └──────┬──────┘
         │
    ┌────┴────┐
    │         │
   PASS      FAIL
    │         │
    ▼         ▼
┌────────┐  ┌─────────────────────────────────────────────────────┐
│ATOMIC  │  │  REFLECTION                                         │
│COMMIT  │  │  ├─▶ Parse error from harness/error_codes.json      │
│        │  │  ├─▶ Analyze root cause                             │
│• Code  │  │  ├─▶ Write to ai/state/scratchpad/current.md        │
│• State │  │  └─▶ Generate fix plan                              │
│• Plan  │  │                                                      │
└───┬────┘  └────────────────────────┬────────────────────────────┘
    │                                │
    ▼                                │ retry_count < max_retries?
┌────────┐                           │
│UPDATE  │                      ┌────┴────┐
│STATE   │                      │         │
│        │                     YES        NO
│• idle  │                      │         │
│• done  │                      ▼         ▼
└───┬────┘                  [RETRY]   [ESCALATE]
    │                          │      (human)
    ▼                          │
┌────────┐                     │
│CLEANUP │◀────────────────────┘
│SCRATCH │
│PAD     │
└───┬────┘
    │
    ▼
  ┌──────────┐
  │   END    │
  └──────────┘
```

---

## Directory Structure

```
.
├── README.md              # Human entry point (this file)
├── LICENSE                # MIT
├── CONTRIBUTING.md        # How to contribute
│
├── ai/                    # Core specification layer
│   ├── ENTRY.md           # AI agent entry point
│   ├── rules/             # Global rules & constraints
│   ├── agents/            # Agent definitions & behaviors
│   ├── state/             # State management (SSOT)
│   ├── orchestrator/      # Execution protocols
│   ├── skills/            # Skill definitions
│   └── contracts/         # Schema definitions
│
├── harness/               # Evaluation system
│   ├── evaluators/        # L1/L2/L3 evaluators
│   ├── metrics/           # Quality metrics
│   └── quality_gate.py    # Evaluation entry point
│
├── examples/              # Quick start examples
│   ├── hello-world/       # Minimal example (5 min)
│   └── todo-app/          # Complete example
│
├── docs/                  # Documentation
├── plans/                 # Task management
├── evals/                 # Evolution system
├── adapters/              # Vendor adapters
├── scripts/               # Utility scripts
└── src/                   # Your business code
```

---

## Quick Start

### Option 1: Try the Example

```bash
git clone https://github.com/artsyne/AHES.git
cd AHES/examples/hello-world
cat README.md
```

### Option 2: Apply to Your Project

```bash
git clone https://github.com/artsyne/AHES.git
cp -r AHES/ai your-project/
cp -r AHES/harness your-project/
```

Point your AI tool to `ai/ENTRY.md` as the entry point.

---

## Core Concepts

**State (SSOT)** — `ai/state/state.json` — Single Source of Truth for task state. AI reads this before any action.

**Orchestrator** — `ai/orchestrator/ORCHESTRATOR.md` — Defines the execution protocol (Read → Plan → Execute → Verify loop).

**Skills** — `ai/skills/index.json` — Registered action templates with input/output schemas and constraints.

**Harness** — `harness/quality_gate.py` — Multi-layer evaluation gate (L1: static, L2: tests, L3: stability).

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
- [Contributing Guide](CONTRIBUTING.md) — How to contribute

---

## License

MIT License — See [LICENSE](LICENSE) for details.
