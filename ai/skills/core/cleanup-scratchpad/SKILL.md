# Skill: Cleanup Scratchpad

<!--
  🧹 SKILL: cleanup-scratchpad
  
  Clear temporary data after successful completion.
-->

---

## 🎯 Purpose

Remove temporary reflection data after a task completes successfully.

---

## 📥 Input

```yaml
task_id: string        # Completed task
archive: boolean       # Archive before delete (default: false)
```

---

## 📤 Output

```yaml
cleaned: boolean
archived_to: string    # If archived
```

---

## 📋 Checklist

- [ ] Task completed successfully
- [ ] Archive if needed
- [ ] Clear scratchpad
- [ ] Verify cleanup

---

## 🔧 Execution

### Step 1: Verify Completion

```
1. Check state.json status = completed
2. Check harness result = PASS
3. Check commit exists
```

### Step 2: Archive (Optional)

```bash
# If archive requested
cp ai/state/scratchpad/current.md \
   ai/state/scratchpad/archive/{task_id}.md
```

### Step 3: Clear Scratchpad

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

### Step 4: Verify

```
1. Scratchpad is clean
2. Archive exists (if requested)
```

---

## ⚠️ Constraints

- ONLY after successful completion
- Preserve archive if requested
- Must follow template format

---

## 🔗 Related

- `ai/skills/core/task-completion/` — Task finalization
