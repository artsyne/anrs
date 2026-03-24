---
name: reflection
description: |
  Analyze failures and plan recovery. Use when:
  (1) Harness check fails
  (2) Need to identify root cause of failure
  (3) Need to create a fix plan for retry
---

# Reflection

When harness fails, analyze the root cause and create a fix plan.

## Input

```yaml
error_code: string     # Harness error code
error_message: string  # Full error details
failed_step: string    # Which step failed
attempt_number: number # Current retry count
```

## Output

```yaml
root_cause: string
fix_plan: list
scratchpad_updated: boolean
ready_for_retry: boolean
```

## Checklist

- [ ] Error parsed correctly
- [ ] Root cause identified
- [ ] Fix plan created
- [ ] Scratchpad updated
- [ ] Ready for retry

## Execution

### 1. Parse Error

1. Read `harness/reports/latest.json`
2. Extract error code
3. Look up in `harness/error_codes.json`

### 2. Analyze

Questions to answer:
- What exactly failed?
- Why did it fail?
- What was the expected vs actual behavior?
- Is this a code issue or test issue?

### 3. Identify Root Cause

Common causes:
- Syntax error → Read error line
- Test failure → Check assertion
- Lint failure → Check rules
- Type error → Check types

### 4. Create Fix Plan

```markdown
## Fix Plan

### Root Cause
{description}

### Fix Steps
1. {step 1}
2. {step 2}

### Verification
- {how to verify fix}
```

### 5. Update Scratchpad

Write to `ai/state/scratchpad/current.md`:

```markdown
# Scratchpad - {task_id}

## Error
{error code}: {message}

## Analysis
{root cause analysis}

## Fix Plan
{steps to fix}
```

## Constraints

- Must identify specific root cause
- Fix plan must be actionable
- Maximum 3 fix steps
- Must update scratchpad

## Related

- `ai/state/scratchpad/current.md` — Scratchpad
- `harness/error_codes.json` — Error reference
