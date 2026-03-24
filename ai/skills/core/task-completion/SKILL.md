---
name: task-completion
description: |
  Finalize and archive a completed task. Use when:
  (1) All acceptance criteria are met
  (2) Harness has passed
  (3) Commit has been created
  (4) Ready to close out the task
---

# Task Completion

Properly close out a task, moving it to completed and updating all records.

## Input

```yaml
task_id: string        # Task to complete
```

## Output

```yaml
completed: boolean
archived_to: string
state_updated: boolean
```

## Checklist

- [ ] All acceptance criteria met
- [ ] Harness passed
- [ ] Commit created
- [ ] Plan moved to completed
- [ ] State updated
- [ ] Scratchpad cleaned

## Execution

### 1. Verify Completion

1. Read `plans/active/{task_id}.md`
2. Check all acceptance criteria
3. Verify all steps completed
4. Confirm harness passed

### 2. Archive Plan

```bash
mv plans/active/{task_id}.md plans/completed/{task_id}.md

# Add completion metadata
echo "
---
Completed: $(date -Iseconds)
Commit: $(git rev-parse HEAD)
" >> plans/completed/{task_id}.md
```

### 3. Update State

```json
{
  "status": "idle",
  "current_task": null,
  "execution": {
    "last_skill": "task-completion",
    "last_result": "success"
  }
}
```

### 4. Cleanup

Call `cleanup-scratchpad` skill.

## Constraints

- All criteria MUST be verified
- Cannot skip any step
- Must archive before state update

## Related

- `ai/skills/core/cleanup-scratchpad/` — Cleanup
- `ai/skills/core/update-state/` — State update
