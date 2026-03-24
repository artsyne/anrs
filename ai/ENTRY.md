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
1. READ   → ai/state/state.json
2. LOCATE → plans/active/{task_id}.md
3. SELECT → ai/skills/index.json
4. EXECUTE→ ai/skills/{category}/{skill}/SKILL.md
5. HARNESS→ ./scripts/run_harness.sh

IF PASS: atomic-commit → update-state → cleanup
IF FAIL: reflection → SCRATCHPAD → new plan → RETRY
```

## Prohibited Actions (MUST NOT)

- Modify code without plan in `plans/active/`
- Skip harness evaluation
- Directly modify `state.json` (use `update-state` skill)
- Commit without passing harness
- Use unregistered skills

## Key Files

| File | Purpose |
|------|---------|
| `ai/state/state.json` | Current state (SSOT) |
| `ai/orchestrator/ORCHESTRATOR.md` | Detailed protocol (sequential + parallel modes) |
| `ai/rules/global.md` | Global constraints |
| `ai/skills/index.json` | Skill registry (15 skills) |
| `harness/quality_gate.py` | Evaluation entry (Security → L1 → L2 → L3) |
| `docs/references/` | Architecture graph, dependency map, API contracts |

## Decision Tree

```
Starting new task?     → Read state.json → plans/active/ → Execute
Task in progress?      → Read state.json → Continue
Harness failed?        → Reflect → SCRATCHPAD → Retry
Task completed?        → Atomic commit → Update state
Unsure?                → Read ai/orchestrator/ORCHESTRATOR.md
```
