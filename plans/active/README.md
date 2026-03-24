---
name: active-plans-index
description: |
  Currently executing task plans. Read when:
  (1) Finding the current task (execution loop step 2)
  (2) Checking task progress
  (3) Understanding what AI should work on
---

# Active Plans

Task plans currently being executed by AI agents.

## Usage

AI agents **LOCATE** tasks here during the execution loop:

```
1. READ   → ai/state/state.json
2. LOCATE → plans/active/{task_id}.md  ← YOU ARE HERE
3. SELECT → ai/skills/index.json
4. EXECUTE→ Follow skill checklist
5. HARNESS→ Verify before commit
```

## Active Tasks

| Task ID | Description | Status |
|---------|-------------|--------|
| [task-001](task-001.md) | Example Hello World endpoint | In Progress |

## Workflow

```
plans/backlog/     →  plans/active/     →  plans/completed/
  (prioritize)          (execute)            (archive)
```

### Promoting from Backlog
```bash
cp plans/templates/task-template.md plans/active/task-{id}.md
# Edit task details
# Update ai/state/state.json with current_task_id
```

### Completing a Task
After harness passes, use `task-completion` skill to:
1. Move plan to `plans/completed/`
2. Update state to idle
3. Create atomic commit
