# Skill: Atomic Commit

<!--
  💾 SKILL: atomic-commit
  
  Commit code and state changes atomically.
-->

---

## 🎯 Purpose

Ensure code and state are always in sync through atomic commits.

---

## 📥 Input

```yaml
message: string        # Commit message
files: list            # Files to commit
task_id: string        # Related task
```

---

## 📤 Output

```yaml
commit_hash: string
committed_files: list
state_synced: boolean
```

---

## 📋 Checklist

- [ ] All harness checks passed
- [ ] Commit message follows convention
- [ ] All related files staged
- [ ] State.json included
- [ ] Commit successful
- [ ] Rollback point created

---

## 🔧 Execution

### Step 1: Pre-Commit Validation

```bash
# Verify harness passed
if [ ! -f harness/reports/latest.json ]; then
  exit 1
fi

# Check last result was PASS
result=$(jq .result harness/reports/latest.json)
if [ "$result" != "PASS" ]; then
  exit 1
fi
```

### Step 2: Stage Files

```bash
# Stage code changes
git add src/

# Stage state
git add ai/state/state.json

# Stage plan updates
git add plans/
```

### Step 3: Commit

```bash
# Commit with conventional message
git commit -m "feat(task-001): implement user login

- Add login endpoint
- Add JWT validation
- Add tests

Task: task-001
Harness: PASS"
```

### Step 4: Verify

```bash
# Verify commit exists
git log -1

# Verify all files included
git show --stat HEAD
```

---

## 📝 Commit Message Format

```
{type}({scope}): {subject}

{body}

Task: {task_id}
Harness: {PASS|FAIL}
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code refactoring
- `test`: Test additions
- `docs`: Documentation

---

## ⚠️ Constraints

- MUST pass harness before commit
- MUST include state.json
- MUST follow message format
- MUST be rollback-able

---

## 🔗 Related

- `scripts/rollback.sh` — Rollback tool
- `harness/reports/latest.json` — Harness result
