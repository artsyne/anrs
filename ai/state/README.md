---
name: state-system
description: |
  State management system documentation. Read when:
  (1) Understanding state.json structure
  (2) Learning about SSOT (Single Source of Truth)
  (3) Working with scratchpad
---

# State System

`state.json` is the Single Source of Truth (SSOT).

## Files

| File | Purpose |
|------|---------|
| `state.json` | Current state (SSOT) |
| `state.schema.json` | JSON Schema validation |
| `scratchpad/current.md` | Short-term memory for reflection |

## Access Control

- **Read**: All components
- **Write**: ONLY `update-state` and `atomic-commit` skills
- Direct modification is PROHIBITED

## State Fields

### status
```
idle      → No active task
running   → Task in progress
blocked   → Waiting for input
completed → Task finished successfully
failed    → Task failed after max retries
```

### execution.next_action
```
continue  → Proceed to next step
retry     → Retry current step
reflect   → Enter reflection mode
escalate  → Request human help
```

## State Transitions

```
idle → running → completed
              → blocked → (human input) → running
              → failed → (reset) → idle
```

## Scratchpad

Temporary reflection data in `scratchpad/` directory.

**Rules**: WRITE during reflection | READ when retrying | CLEAR after completion

**Format**:
```markdown
# Scratchpad - {task_id}
## Error
{error message}
## Analysis
{root cause}
## Fix Plan
{proposed solution}
```
