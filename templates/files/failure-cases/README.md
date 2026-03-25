# Failure Cases

Archive of unrecoverable failures for learning and pattern analysis.

## When to Archive

- Task failed after 3+ retry attempts
- Root cause identified but requires human intervention
- Novel failure pattern worth documenting

## File Format

```markdown
# FC-{id}: {title}

## Context
- Task: {task_id}
- Date: {date}

## Failure Summary
What happened.

## Root Cause
Why it happened.

## Attempted Solutions
What was tried.

## Resolution
How it was eventually resolved (or why escalated).

## Lessons Learned
What to do differently next time.
```
