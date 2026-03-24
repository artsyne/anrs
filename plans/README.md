---
name: plans-index
description: |
  Task plan management hub. Read when:
  (1) Understanding plan lifecycle (backlog → active → completed)
  (2) Creating new task plans
  (3) Locating current or past tasks
---

# Plans

Task planning and tracking for AHES-governed development.

## Directory Structure

```
plans/
├── active/       # Tasks currently being executed
├── completed/    # Archived finished tasks
├── backlog/      # Future tasks and technical debt
└── templates/    # Plan templates
```

## Plan Lifecycle

```
backlog/          →    active/           →    completed/
(future work)          (in progress)          (archived)
     ↓                      ↓                      ↓
  Prioritize           Execute via            Reference for
  & refine             AHES protocol          future work
```

## Quick Reference

| Directory | Purpose | AI Action |
|-----------|---------|-----------|
| `active/` | Current tasks | **LOCATE** task here (execution loop step 2) |
| `completed/` | Finished tasks | Reference past implementations |
| `backlog/` | Future work, tech debt | Prioritize and promote to active |
| `templates/` | Plan templates | Copy to create new plans |

## Creating a New Task

1. Copy template: `cp templates/task-template.md active/task-{id}.md`
2. Fill in objective, requirements, and steps
3. Update `ai/state/state.json` with new task reference

## Plan Format

All plans use YAML frontmatter + Markdown:

```yaml
---
name: task-xxx
description: |
  Brief task description. Read when:
  (1) Condition 1
  (2) Condition 2
---

# Task: task-xxx

## Objective
What this task achieves.

## Requirements
- Requirement 1
- Requirement 2

## Steps
1. [ ] Step 1
2. [ ] Step 2

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
```

## Related Files

| File | Purpose |
|------|---------|
| `ai/ENTRY.md` | Execution loop references `plans/active/` |
| `ai/state/state.json` | Contains `current_task_id` |
| `ai/skills/workflow/task-completion/` | Moves plans to `completed/` |
