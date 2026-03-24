# Skill: Task Completion

<!--
  ✅ SKILL: task-completion
  
  Finalize and archive a completed task.
-->

---

## 🎯 Purpose

Properly close out a task, moving it to completed and updating all records.

---

## 📥 Input

```yaml
task_id: string        # Task to complete
```

---

## 📤 Output

```yaml
completed: boolean
archived_to: string
state_updated: boolean
```

---

## 📋 Checklist

- [ ] All acceptance criteria met
- [ ] Harness passed
- [ ] Commit created
- [ ] Plan moved to completed
- [ ] State updated
- [ ] Scratchpad cleaned

---

## 🔧 Execution

### Step 1: Verify Completion

```
1. Read plans/active/{task_id}.md
2. Check all acceptance criteria
3. Verify all steps completed
4. Confirm harness passed
```

### Step 2: Archive Plan

```bash
# Move plan to completed
mv plans/active/{task_id}.md \
   plans/completed/{task_id}.md

# Add completion metadata
echo "
---
Completed: $(date -Iseconds)
Commit: $(git rev-parse HEAD)
" >> plans/completed/{task_id}.md
```

### Step 3: Update State

```json
{
  "status": "idle",
  "current_task": null,
  "execution": {
    "last_skill": "task-completion",
    "last_result": "success",
    "retry_count": 0,
    "next_action": null
  },
  "history": [
    {
      "task_id": "{task_id}",
      "status": "completed",
      "completed_at": "{timestamp}"
    },
    ...previous_history
  ]
}
```

### Step 4: Cleanup

```
1. Call cleanup-scratchpad skill
2. Verify all temporary files removed
```

---

## ⚠️ Constraints

- All criteria MUST be verified
- Cannot skip any step
- Must archive before state update

---

## 🔗 Related

- `ai/skills/core/cleanup-scratchpad/` — Cleanup
- `ai/skills/core/update-state/` — State update
