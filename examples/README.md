---
name: examples-index
description: |
  AHES protocol implementation examples. Read when:
  (1) Learning how to apply AHES in a real project
  (2) Understanding state.json, ENTRY.md, harness usage
  (3) Quick start with AHES protocol
---

# Examples

Example projects demonstrating AHES protocol implementation.

## Purpose

| Audience | Value |
|----------|-------|
| **AI** | Reference for applying AHES protocol in other projects |
| **Human** | Quick start guide to understand AHES workflow |

## Examples

| Example | Description | Time |
|---------|-------------|------|
| [hello-world/](hello-world/) | Minimal example with basic harness | 5 min |
| [todo-app/](todo-app/) | Complete example with L1/L2/L3 evaluation | 15 min |

## Structure Pattern

Each example follows the AHES directory structure:

```
example/
├── ai/
│   ├── ENTRY.md        # AI entry point (read first)
│   ├── state/
│   │   └── state.json  # Current state (SSOT)
│   └── skills/         # (optional) Local skill registry
├── harness/            # Evaluation scripts
├── plans/active/       # (optional) Task plans
├── src/                # Implementation code
└── README.md           # Human quick start
```

## How to Use

**For AI:**
1. Read `ai/ENTRY.md` first
2. Follow the execution protocol
3. Run harness before completion

**For Human:**
1. Read the example's `README.md`
2. Follow "Try It" steps
3. Observe AI behavior
