# Skill: Write Plan

<!--
  📝 SKILL: write-plan
  
  Create an execution plan for a given task.
-->

---

## 🎯 Purpose

Transform a task description into a structured, actionable plan.

---

## 📥 Input

```yaml
task_id: string        # e.g., "task-001"
task_description: text # What needs to be done
constraints: list      # Any limitations
```

---

## 📤 Output

```yaml
plan_file: plans/active/{task_id}.md
plan_structure:
  - objective
  - requirements
  - steps
  - acceptance_criteria
  - estimated_effort
```

---

## 📋 Checklist

- [ ] Read task description completely
- [ ] Identify all requirements
- [ ] Break down into atomic steps
- [ ] Define clear acceptance criteria
- [ ] Estimate effort
- [ ] Create plan file
- [ ] Validate plan structure

---

## 🔧 Execution

### Step 1: Analyze Task

```
1. Read task description
2. Identify key objectives
3. List all requirements
4. Note any constraints
```

### Step 2: Decompose

```
1. Break into subtasks
2. Each subtask should be:
   - Atomic (single action)
   - Testable (verifiable)
   - Independent (minimal dependencies)
```

### Step 3: Structure Plan

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

### Step 4: Validate

```
1. All requirements addressed?
2. Steps are atomic?
3. Acceptance criteria measurable?
4. No ambiguous terms?
```

---

## ⚠️ Constraints

- Plan must be < 200 lines
- Each step must be actionable
- No vague language ("improve", "optimize" without metrics)

---

## 🔗 Related

- `ai/skills/core/execute-plan/` — Execute the plan
- `plans/active/` — Where plans are stored
