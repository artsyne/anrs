# AHES: AI Harness Engineering Standard

> A deterministic, transactional framework for AI-driven development.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.1-blue.svg)]()
[![Standard](https://img.shields.io/badge/AI%20Native-Repo%20Spec-green.svg)]()

---

## 🎯 What is AHES?

AHES (AI Harness Engineering Standard) is the **first vendor-neutral, deterministic, and transactional framework** for AI-driven software engineering.

Unlike traditional AI coding assistants that operate unpredictably, AHES provides:

- **Deterministic Execution** — Every AI action follows a defined protocol
- **Transactional Safety** — Code changes are atomic and reversible
- **Vendor Neutral** — Works with any AI tool (Cursor, Claude, OpenAI, etc.)
- **Self-Evolving** — Learns from failures to improve over time

---

## 🏗 Architecture Overview

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

## 📁 Directory Structure

```
.
├── README.md              # Human entry point (this file)
├── LICENSE                # Apache 2.0
├── CONTRIBUTING.md        # How to contribute
│
├── ai/                    # 🔥 Core specification layer
│   ├── ENTRY.md           # AI agent entry point
│   ├── rules/             # Global rules & constraints
│   ├── agents/            # Agent definitions & behaviors
│   ├── state/             # State management (SSOT)
│   ├── orchestrator/      # Execution protocols
│   ├── skills/            # Skill definitions
│   └── contracts/         # Schema definitions
│
├── harness/               # 🧪 Evaluation system
│   ├── evaluators/        # L1/L2/L3 evaluators
│   ├── metrics/           # Quality metrics
│   └── quality_gate.py    # Evaluation entry point
│
├── docs/                  # 📚 Documentation
├── plans/                 # 🗺 Task management
├── evals/                 # 🔁 Evolution system
├── adapters/              # 🔌 Vendor adapters
├── scripts/               # 🛠 Utility scripts
└── src/                   # 💻 Your business code
```

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/artsyne/AHES.git
cd AHES
```

### 2. Initialize your project

```bash
# Copy AHES structure to your project
cp -r AHES/* your-project/
```

### 3. Configure your AI tool

```bash
# Generate adapter for your AI tool
./scripts/generate_adapters.sh cursor
```

### 4. Start working

Point your AI tool to `ai/ENTRY.md` and start coding!

---

## 🔑 Core Concepts

### State (SSOT)

All task state is stored in `ai/state/state.json`. This is the **Single Source of Truth** for the AI agent.

### Orchestrator

The orchestrator defines the execution protocol. See `ai/orchestrator/ORCHESTRATOR.md` for the standard loop.

### Skills

Skills are reusable action templates. Each skill has:
- Input/output schema
- Constraints
- Checklist

### Harness

The harness evaluates code changes across three levels:
- **L1**: Static checks (lint, complexity)
- **L2**: Dynamic tests (unit tests, contracts)
- **L3**: Stability (FMEA, chaos engineering)

---

## 📖 Documentation

- [Core Beliefs](docs/core-beliefs.md) — First principles
- [System Architecture](docs/architecture/system.md) — Technical design
- [Contributing Guide](CONTRIBUTING.md) — How to contribute

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📄 License

Apache License 2.0 — See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

AHES is inspired by the challenges of making AI-driven development reliable, predictable, and safe.

---

**Built with ❤️ for the AI-native future.**
