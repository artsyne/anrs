---
name: execute-plan
description: |
  Execute steps from an existing plan. Use when:
  (1) A plan exists in plans/active/
  (2) Ready to implement the next step
  (3) Need to make code changes according to plan
---

# Execute Plan

Implement the steps defined in an active plan.

## Input

```yaml
task_id: string        # Task to execute
step_index: number     # Which step (optional, default: next)
```

## Output

```yaml
code_changes: list     # Files modified
test_results: object   # Test outcomes
ready_for_harness: boolean
```

## Checklist

- [ ] Plan exists and is valid
- [ ] Current step identified
- [ ] Prerequisites met
- [ ] Implementation complete
- [ ] Local tests pass
- [ ] Ready for harness

## Execution

### 1. Load Plan

1. Read `plans/active/{task_id}.md`
2. Parse steps list
3. Identify current step
4. Check step dependencies

### 2. Implement

1. Follow step instructions exactly
2. Make minimal changes
3. Add/update tests
4. Document non-obvious decisions

### 3. Verify

1. Run relevant tests
2. Check linting
3. Verify step completion
4. Update step status

## Constraints

- Execute ONE step at a time
- Stop on any failure
- No skipping steps
- No modifying plan during execution

## Related

- `spec/skills/core/write-plan/` — Create plans
- `spec/skills/core/atomic-commit/` — Commit changes
