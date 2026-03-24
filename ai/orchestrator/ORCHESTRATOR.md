---
name: orchestrator-protocol
description: |
  Detailed execution protocol for AI agents. Read when:
  (1) Need step-by-step execution guidance
  (2) Understanding harness pass/fail handling
  (3) Configuring retry policy
---

# Orchestrator Protocol

## Execution Loop

```
1. READ STATE    → ai/state/state.json
2. LOCATE TASK   → plans/active/{task_id}.md
3. SELECT SKILL  → ai/skills/index.json (match task to triggers)
4. EXECUTE SKILL → Follow SKILL.md checklist completely
5. RUN HARNESS   → ./scripts/run_harness.sh (L1 → L2 → L3)

PASS → 6. atomic-commit → 7. update-state → 8. cleanup-scratchpad → DONE
FAIL → reflection → SCRATCHPAD → new plan → RETRY (step 4)
```

## Step Details

### 1. Read State
```json
{"current_task": "task-001", "status": "running", "execution": {"retry_count": 0}}
```

### 2. Locate Task
```markdown
# Task: task-001
## Objective: Implement user authentication
## Requirements: Add login endpoint, JWT validation, tests
```

### 3. Select Skill
```json
{"selected_skill": "test-driven-dev", "reason": "Task requires new feature with tests"}
```

### 4-5. Execute & Harness
- Read SKILL.md, follow all checklist items
- Run `./scripts/run_harness.sh` (L1 → L2 → L3)

### 6-8. Success Path
`atomic-commit` → `update-state` → `cleanup-scratchpad`

### Failure Path
`reflection` → SCRATCHPAD (error + analysis) → new plan → RETRY

## Retry Policy

```yaml
max_retries: 3
retry_conditions: [harness_failure, transient_error]
no_retry: [safety_violation, critical_constraint_violation]
on_max_retries: {action: escalate, set_status: blocked}
```

## Strategy Selection

| Strategy | Use When |
|----------|----------|
| `strategies/default.md` | Normal development |
| `strategies/debug.md` | Investigating bugs |
| `strategies/refactor.md` | Code refactoring |
