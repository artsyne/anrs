---
name: cleanup-scratchpad
description: |
  Clear temporary data after successful completion. Use when:
  (1) Task completed successfully
  (2) Need to reset scratchpad for next task
  (3) Called by task-completion skill
---

# Cleanup Scratchpad

Remove temporary reflection data after a task completes successfully.

## Input

```yaml
task_id: string        # Completed task
archive: boolean       # Archive before delete (default: false)
```

## Output

```yaml
cleaned: boolean
archived_to: string    # If archived
```

## Checklist

- [ ] Task completed successfully
- [ ] Archive if needed
- [ ] Clear scratchpad
- [ ] Verify cleanup

## Execution

### 1. Verify Completion

1. Check state.json status = completed
2. Check harness result = PASS
3. Check commit exists

### 2. Archive (Optional)

```bash
cp spec/state/scratchpad/current.md \
   spec/state/scratchpad/archive/{task_id}.md
```

### 3. Clear Scratchpad

Reset to template:

```markdown
# Scratchpad

## Current Task
_No active task_

## Error Log
_No errors_

## Analysis
_No analysis_

## Fix Plan
_No plan_
```

### 4. Verify

- Scratchpad is clean
- Archive exists (if requested)

## Constraints

- ONLY after successful completion
- Preserve archive if requested
- Must follow template format

## Related

- `spec/skills/core/task-completion/` — Task finalization
