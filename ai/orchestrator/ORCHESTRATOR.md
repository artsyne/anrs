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
   └─ OR dispatch-subagent for parallel independent tasks
5. RUN HARNESS   → ./scripts/run_harness.sh (Security → L1 → L2 → L3)

PASS → 6. atomic-commit → 7. update-state → 8. cleanup-scratchpad → DONE
FAIL → reflection → SCRATCHPAD → new plan → RETRY (step 4)
```

## Step Details

### Prepare Phase

#### 1. Read State
```json
{"current_task": "task-001", "status": "running", "execution": {"retry_count": 0}}
```

#### 2. Locate Task
```markdown
# Task: task-001
## Objective: Implement user authentication
## Requirements: Add login endpoint, JWT validation, tests
```

#### 3. Select Skill
```json
{"selected_skill": "test-driven-dev", "reason": "Task requires new feature with tests"}
```

### Execute Phase

#### 4. Execute Skill
- Read SKILL.md, follow all checklist items
- OR use `dispatch-subagent` for parallel independent tasks

#### 5. Run Harness
- Run `./scripts/run_harness.sh` (Security → L1 → L2 → L3)
- Fail at any level → Stop cascade, enter Failure Path

### Finalize Phase (on PASS)

#### 6. Atomic Commit
Commit code + state changes together

#### 7. Update State
Set status to `idle`, clear `current_task`

#### 8. Cleanup Scratchpad
Clear temporary data from `ai/state/scratchpad/`

### Failure Path
`reflection` → SCRATCHPAD (error + analysis) → new plan → RETRY (step 4)

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

## Execution Modes

### Sequential (Default)
```
Task 1 → Task 2 → Task 3 → ...
```
Use `execute-plan` skill. Best for dependent tasks.

### Parallel (Subagent)
```
        ┌─ Task 1 ─┐
Main ───┼─ Task 2 ─┼─── Collect → Review → Harness
        └─ Task 3 ─┘
```
Use `dispatch-subagent` skill. Best for independent tasks.

**Parallel execution criteria:**
- Tasks have no dependencies
- Tasks modify different files
- Each task is self-contained (2-5 min)
