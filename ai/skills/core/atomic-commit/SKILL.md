---
name: atomic-commit
description: |
  Commit code and state changes atomically. Use when:
  (1) All harness checks have passed
  (2) Ready to persist changes to git
  (3) Need to sync code + state.json together
---

# Atomic Commit

Ensure code and state are always in sync through atomic commits.

## Input

```yaml
message: string        # Commit message
files: list            # Files to commit
task_id: string        # Related task
```

## Output

```yaml
commit_hash: string
committed_files: list
state_synced: boolean
```

## Checklist

- [ ] All harness checks passed
- [ ] Commit message follows convention
- [ ] All related files staged
- [ ] State.json included
- [ ] Commit successful

## Execution

### 1. Pre-Commit Validation

```bash
# Verify harness passed
result=$(jq .result harness/reports/latest.json)
[ "$result" = "PASS" ] || exit 1
```

### 2. Stage Files

```bash
git add src/
git add ai/state/state.json
git add plans/
```

### 3. Commit

```bash
git commit -m "feat(task-001): implement user login

- Add login endpoint
- Add JWT validation

Task: task-001
Harness: PASS"
```

### 4. Verify

```bash
git log -1 --stat
```

## Commit Message Format

```
{type}({scope}): {subject}

{body}

Task: {task_id}
Harness: {PASS|FAIL}
```

Types: `feat`, `fix`, `refactor`, `test`, `docs`

## Constraints

- MUST pass harness before commit
- MUST include state.json
- MUST follow message format

## Related

- `scripts/rollback.sh` — Rollback tool
- `harness/reports/latest.json` — Harness result
