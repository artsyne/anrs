# Orchestrator Protocol

<!--
  🚦 EXECUTION PROTOCOL
  
  This is the core execution loop for all AI agents.
  FOLLOW THIS PROTOCOL EXACTLY.
-->

---

## 🎯 Purpose

The orchestrator defines the **deterministic execution protocol** that all AI agents must follow.

---

## 🔄 Standard Execution Loop

```
┌─────────────────────────────────────────────────────────────────┐
│                    AHES EXECUTION LOOP                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  1. READ STATE                                          │    │
│  │     → ai/state/state.json                               │    │
│  └─────────────────────────────────────────────────────────┘    │
│                          │                                       │
│                          ▼                                       │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  2. LOCATE TASK                                         │    │
│  │     → plans/active/{current_task}.md                    │    │
│  └─────────────────────────────────────────────────────────┘    │
│                          │                                       │
│                          ▼                                       │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  3. SELECT SKILL                                        │    │
│  │     → ai/skills/index.json                              │    │
│  │     → Match task requirements to skill triggers         │    │
│  └─────────────────────────────────────────────────────────┘    │
│                          │                                       │
│                          ▼                                       │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  4. EXECUTE SKILL                                       │    │
│  │     → ai/skills/{category}/{skill}/SKILL.md             │    │
│  │     → Follow checklist completely                       │    │
│  └─────────────────────────────────────────────────────────┘    │
│                          │                                       │
│                          ▼                                       │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  5. RUN HARNESS                                         │    │
│  │     → ./scripts/run_harness.sh                          │    │
│  │     → L1 → L2 → L3 cascade                              │    │
│  └─────────────────────────────────────────────────────────┘    │
│                          │                                       │
│                          ▼                                       │
│                  ┌───────────────┐                               │
│                  │    PASS?      │                               │
│                  └───────┬───────┘                               │
│                          │                                       │
│          ┌───────────────┼───────────────┐                      │
│          │ YES           │               │ NO                    │
│          ▼               │               ▼                       │
│  ┌──────────────┐        │       ┌──────────────┐               │
│  │ 6. COMMIT    │        │       │ 7. REFLECT   │               │
│  │ atomic-commit│        │       │ reflection   │               │
│  └──────┬───────┘        │       └──────┬───────┘               │
│         │                │              │                        │
│         ▼                │              ▼                        │
│  ┌──────────────┐        │       ┌──────────────┐               │
│  │ 8. UPDATE    │        │       │ SCRATCHPAD   │               │
│  │ update-state │        │       │ write error  │               │
│  └──────┬───────┘        │       └──────┬───────┘               │
│         │                │              │                        │
│         ▼                │              ▼                        │
│  ┌──────────────┐        │       ┌──────────────┐               │
│  │ 9. CLEANUP   │        │       │ NEW PLAN     │               │
│  │ scratchpad   │        │       │ fix strategy │               │
│  └──────┬───────┘        │       └──────┬───────┘               │
│         │                │              │                        │
│         ▼                │              └───────▶ RETRY (step 4) │
│      [DONE]              │                                       │
│                          │                                       │
└──────────────────────────┴───────────────────────────────────────┘
```

---

## 📋 Step Details

### Step 1: Read State

```json
// Read from ai/state/state.json
{
  "current_task": "task-001",
  "status": "running",
  "execution": {
    "last_skill": "write-plan",
    "last_result": "success",
    "retry_count": 0,
    "next_action": "continue"
  }
}
```

### Step 2: Locate Task

```markdown
// Read from plans/active/{task_id}.md
# Task: task-001

## Objective
Implement user authentication

## Requirements
- Add login endpoint
- Add JWT validation
- Add tests
```

### Step 3: Select Skill

```json
// Match from ai/skills/index.json
{
  "selected_skill": "test-driven-dev",
  "reason": "Task requires adding new feature with tests"
}
```

### Step 4: Execute Skill

- Read `SKILL.md` for the skill
- Follow all checklist items
- Produce required outputs

### Step 5: Run Harness

```bash
./scripts/run_harness.sh
# Runs L1 → L2 → L3
# Returns: PASS or FAIL with error codes
```

### Step 6-9: Success Path

```
1. atomic-commit → Commit code + state together
2. update-state → Mark task progress
3. cleanup-scratchpad → Clear temporary data
```

### Step 7+: Failure Path

```
1. reflection → Analyze failure
2. scratchpad → Write error + analysis
3. new plan → Create fix strategy
4. retry → Go back to step 4
```

---

## 🔄 Retry Policy

```yaml
max_retries: 3
retry_conditions:
  - harness_failure
  - transient_error
no_retry_conditions:
  - safety_violation
  - critical_constraint_violation
on_max_retries:
  action: escalate
  set_status: blocked
```

---

## 🚦 Strategy Selection

See `strategies/` for specialized protocols:

| Strategy | Use When |
|----------|----------|
| `default.md` | Normal development |
| `debug.md` | Investigating bugs |
| `refactor.md` | Code refactoring |

---

## 🔗 Related

- `ai/ENTRY.md` — Agent entry point
- `ai/rules/global.md` — Global constraints
- `ai/skills/index.json` — Skill registry
