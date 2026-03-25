---
name: entry-point
description: |
  AI Agent mandatory entry point. Read this FIRST when:
  (1) Starting work in this repository
  (2) Unsure what to do next
  (3) Need to understand the execution protocol
---

# AI Agent Entry Point

> **Protocol Version**: 0.1.0 | **Status**: Stable

**Normative Language**: MUST (required) / SHOULD (recommended) / MAY (optional)

## Execution Loop

```
1. READ   → .anrs/state.json
2. LOCATE → .anrs/plans/active/{task_id}.md
3. SELECT → .anrs/skills/index.json
4. EXECUTE→ .anrs/skills/{category}/{skill}/SKILL.md
5. HARNESS→ anrs harness

IF PASS: atomic-commit → update-state → cleanup
IF FAIL: reflection → SCRATCHPAD → new plan → RETRY
```

## Prohibited Actions (MUST NOT)

- Modify code without plan in `.anrs/plans/active/`
- Skip harness evaluation
- Directly modify `state.json` (use `update-state` skill)
- Commit without passing harness
- Use unregistered skills

## Key Files

| File | Purpose |
|------|---------|
| `.anrs/state.json` | Current state (SSOT) |
| `.anrs/ENTRY.md` | Detailed protocol (sequential + parallel modes) |
| `.anrs/config.json` | Project configuration |
| `.anrs/skills/index.json` | Skill registry |
| `.anrs/plans/active/` | Plan lifecycle (backlog → active → completed) |
| `.anrs/harness/` | Quality verification (full level) |

## Decision Tree

```
Starting new task?     → Read .anrs/state.json → .anrs/plans/active/ → Execute
Task in progress?      → Read .anrs/state.json → Continue
Harness failed?        → Reflect → SCRATCHPAD → Retry
Task completed?        → Atomic commit → Update state
Unsure?                → Read .anrs/ENTRY.md
```
