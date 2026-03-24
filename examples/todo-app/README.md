# Todo App Example

A complete AHES example demonstrating the full workflow including L1/L2/L3 evaluation.

---

## What This Example Shows

1. Complete AHES directory structure
2. Multi-level harness evaluation (L1 → L2 → L3)
3. State transitions through a task lifecycle
4. Skill-based execution
5. Reflection on failure

---

## Project Structure

```
todo-app/
├── README.md
├── ai/
│   ├── ENTRY.md
│   ├── state/
│   │   └── state.json
│   └── skills/
│       └── index.json
├── src/
│   ├── __init__.py
│   └── todo.py          # Main module (implement here)
├── tests/
│   └── test_todo.py
├── harness/
│   ├── run.sh           # Main harness runner
│   ├── l1_lint.sh       # Static checks
│   ├── l2_test.sh       # Unit tests
│   └── l3_risk.sh       # Risk analysis
└── plans/
    └── active/
        └── todo-001.md  # Current task
```

---

## The Task

Implement a simple Todo list with:
- `add_todo(text)` - Add a new todo
- `list_todos()` - List all todos
- `complete_todo(id)` - Mark todo as done

---

## Try It

### Step 1: Review the Plan

```bash
cat plans/active/todo-001.md
```

### Step 2: Check Current State

```bash
cat ai/state/state.json
```

### Step 3: Point AI to Entry

Open your AI tool and set `ai/ENTRY.md` as the entry point.

The AI will:
1. Read state.json
2. Load the active plan
3. Implement according to plan
4. Run harness
5. Commit or reflect

### Step 4: Run Harness Manually (optional)

```bash
./harness/run.sh
```

---

## Expected Flow

```
START
  │
  ▼
READ state.json
  │ status: pending
  │ task: todo-001
  ▼
LOAD plan
  │ plans/active/todo-001.md
  ▼
EXECUTE
  │ Implement add_todo, list_todos, complete_todo
  ▼
L1 CHECK
  │ Lint, syntax
  ▼
L2 CHECK
  │ Run tests/test_todo.py
  ▼
L3 CHECK
  │ Risk analysis (AI-driven)
  ▼
PASS? ─── NO ──▶ REFLECT ──▶ RETRY
  │
 YES
  │
  ▼
COMMIT
  │ Code + state
  ▼
UPDATE STATE
  │ status: idle
  ▼
END
```

---

## Key Files

- `ai/ENTRY.md` - AI reads this first
- `ai/state/state.json` - Current task state
- `plans/active/todo-001.md` - Task specification
- `harness/run.sh` - Evaluation pipeline
