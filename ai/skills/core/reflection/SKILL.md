# Skill: Reflection

<!--
  🪞 SKILL: reflection
  
  Analyze failures and plan recovery.
-->

---

## 🎯 Purpose

When harness fails, analyze the root cause and create a fix plan.

---

## 📥 Input

```yaml
error_code: string     # Harness error code
error_message: string  # Full error details
failed_step: string    # Which step failed
attempt_number: number # Current retry count
```

---

## 📤 Output

```yaml
root_cause: string
fix_plan: list
scratchpad_updated: boolean
ready_for_retry: boolean
```

---

## 📋 Checklist

- [ ] Error parsed correctly
- [ ] Root cause identified
- [ ] Fix plan created
- [ ] Scratchpad updated
- [ ] Ready for retry

---

## 🔧 Execution

### Step 1: Parse Error

```
1. Read harness/reports/latest.json
2. Extract error code
3. Look up in harness/error_codes.json
4. Understand error category
```

### Step 2: Analyze

```
Questions to answer:
1. What exactly failed?
2. Why did it fail?
3. What was the expected behavior?
4. What was the actual behavior?
5. Is this a code issue or test issue?
```

### Step 3: Identify Root Cause

```
Common causes:
- Syntax error → Read error line
- Test failure → Check assertion
- Lint failure → Check rules
- Type error → Check types
```

### Step 4: Create Fix Plan

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

### Step 5: Update Scratchpad

```markdown
# Scratchpad - task-001

## Error
{error code}: {message}

## Analysis
{root cause analysis}

## Fix Plan
{steps to fix}
```

---

## ⚠️ Constraints

- Must identify specific root cause
- Fix plan must be actionable
- Maximum 3 fix steps
- Must update scratchpad

---

## 🔗 Related

- `ai/state/scratchpad/current.md` — Scratchpad
- `harness/error_codes.json` — Error reference
