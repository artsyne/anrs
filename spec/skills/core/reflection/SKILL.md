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
- [ ] **If unrecoverable or max retries reached**: Archive failure case

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

Write to `spec/state/scratchpad/current.md`:

```markdown
# Scratchpad - {task_id}

## Error
{error code}: {message}

## Analysis
{root cause analysis}

## Fix Plan
{steps to fix}
```

### 6. Archive Failure Case (If Unrecoverable)

> **When to archive**: `attempt_number >= 3` OR error is classified as unrecoverable.

This step ensures failure knowledge is captured for future learning.

#### 6.1 Determine Category

| Error Type | Category | Path |
|------------|----------|------|
| Syntax/Parse | `syntax` | `evals/failure-cases/syntax/` |
| Test Assertion | `test` | `evals/failure-cases/test/` |
| Security Violation | `security` | `evals/failure-cases/security/` |
| L3/Stability | `stability` | `evals/failure-cases/stability/` |

#### 6.2 Generate Failure Case File

Create file: `evals/failure-cases/{category}/FC-{timestamp}.md`

Timestamp format: `YYYYMMDD-HHMMSS`

```markdown
# Failure Case: FC-{timestamp}

## Context
- Task: {task_id}
- Skill: {skill_name}
- Harness Level: {L1/L2/L3/Security}
- Attempt: {attempt_number}
- Date: {ISO-8601 date}

## Error
```
{full_error_message}
```

## Root Cause
{root_cause_analysis}

## Fix Attempted
{list of fix steps tried}

## Why It Failed
{explanation of why fixes did not work}

## Prevention
- {recommendation 1}
- {recommendation 2}

## Tags
`{category}`, `{harness_level}`, `{error_code}`
```

#### 6.3 Update Output

When archiving, add to output:

```yaml
root_cause: string
fix_plan: []           # Empty since unrecoverable
scratchpad_updated: true
ready_for_retry: false  # Cannot retry
failure_archived: true
failure_case_path: "evals/failure-cases/{category}/FC-{timestamp}.md"
```

## Constraints

- Must identify specific root cause
- Fix plan must be actionable
- Maximum 3 fix steps
- Must update scratchpad
- **Must archive failure case if `attempt_number >= 3` or error is unrecoverable**

## Related

- `spec/state/scratchpad/current.md` — Scratchpad
- `harness/error_codes.json` — Error reference
- `evals/failure-cases/README.md` — Failure case template and categories
