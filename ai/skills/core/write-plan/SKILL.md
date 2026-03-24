---
name: write-plan
description: |
  Create an execution plan for a given task. Use when:
  (1) Starting a new task
  (2) Task description needs to be broken into actionable steps
  (3) Need to define acceptance criteria before execution
---

# Write Plan

Transform a task description into a structured, actionable plan.

## Input

```yaml
task_id: string        # e.g., "task-001"
task_description: text # What needs to be done
constraints: list      # Any limitations
```

## Output

```yaml
plan_file: plans/active/{task_id}.md
plan_structure:
  - objective
  - requirements
  - steps
  - acceptance_criteria
  - estimated_effort
```

## Checklist

- [ ] Read task description completely
- [ ] Identify all requirements
- [ ] Break down into atomic steps
- [ ] Define clear acceptance criteria
- [ ] Create plan file

## Execution

### 1. Analyze Task

1. Read task description
2. Identify key objectives
3. List all requirements
4. Note any constraints

### 2. Decompose

Each subtask should be:
- Atomic (single action)
- Testable (verifiable)
- Independent (minimal dependencies)

### 3. Structure Plan

```markdown
# Task: {task_id}

## Objective
{clear, single-sentence objective}

## Requirements
- {requirement 1}
- {requirement 2}

## Steps
1. {step 1}
2. {step 2}

## Acceptance Criteria
- [ ] {criterion 1}
- [ ] {criterion 2}

## Estimated Effort
{time estimate}
```

### 4. Validate

- All requirements addressed?
- Steps are atomic?
- Acceptance criteria measurable?
- No ambiguous terms?

## Constraints

- Plan must be < 200 lines
- Each step must be actionable
- No vague language ("improve", "optimize" without metrics)

## Related

- `ai/skills/core/execute-plan/` — Execute the plan
- `plans/active/` — Where plans are stored
