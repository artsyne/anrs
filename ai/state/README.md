# State System

<!--
  🧠 STATE MANAGEMENT
  
  This directory contains the state management system.
  state.json is the Single Source of Truth (SSOT).
-->

---

## 📋 Overview

The state system tracks:
- Current task
- Execution status
- Last action results
- Task history

---

## 📁 Files

| File | Purpose |
|------|---------|
| `state.json` | Current state (SSOT) |
| `state.schema.json` | JSON Schema for validation |
| `scratchpad/current.md` | Short-term memory for reflection |

---

## 🔒 Access Control

### Read Access

All components can read `state.json`.

### Write Access

**ONLY** the following can modify state:
- `ai/skills/core/update-state/`
- `ai/skills/core/atomic-commit/`

Direct modification is **PROHIBITED**.

---

## 📊 State Fields

### `status`

| Value | Meaning |
|-------|---------|
| `idle` | No active task |
| `running` | Task in progress |
| `blocked` | Waiting for input |
| `completed` | Task finished successfully |
| `failed` | Task failed after max retries |

### `execution.next_action`

| Value | Meaning |
|-------|---------|
| `continue` | Proceed to next step |
| `retry` | Retry current step |
| `reflect` | Enter reflection mode |
| `escalate` | Request human help |

---

## 🔄 State Transitions

```
idle ──────────────────▶ running
  ▲                        │
  │                        ├───▶ completed
  │                        │
  │                        ├───▶ blocked ──▶ (human input) ──▶ running
  │                        │
  │                        └───▶ failed
  │                               │
  └───────────────────────────────┘
           (reset)
```

---

## 🧹 Scratchpad

The `scratchpad/` directory contains temporary reflection data.

### Rules

1. **WRITE** only during reflection phase
2. **READ** when retrying after failure
3. **CLEAR** after task completion

### Format

```markdown
# Scratchpad - {task_id}

## Error
{error message}

## Analysis
{root cause analysis}

## Fix Plan
{proposed solution}
```

---

## 🔗 Related

- `ai/skills/core/update-state/` — State update skill
- `ai/orchestrator/ORCHESTRATOR.md` — Execution protocol
