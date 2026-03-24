# Hello World Example

A minimal AHES example demonstrating the core workflow in 5 minutes.

---

## What This Example Shows

1. State management via `ai/state/state.json`
2. Task execution following the AHES protocol
3. Harness evaluation (simplified L1 check)

---

## Project Structure

```
hello-world/
├── README.md           # This file
├── ai/
│   ├── ENTRY.md        # AI entry point
│   └── state/
│       └── state.json  # Task state
├── src/
│   └── hello.py        # Your code
└── harness/
    └── check.sh        # Simple L1 check
```

---

## Try It

### Step 1: View the Current State

```bash
cat ai/state/state.json
```

You'll see:
```json
{
  "current_task": "hello-001",
  "status": "pending"
}
```

### Step 2: Complete the Task

The task is to add a `greet(name)` function to `src/hello.py`.

Open your AI tool and point it to `ai/ENTRY.md`. Ask it to:

> "Complete task hello-001: add a greet function"

### Step 3: Run the Harness

```bash
./harness/check.sh
```

If the function exists and passes basic checks, you'll see:
```
✓ L1 Check Passed
```

### Step 4: Observe State Update

After success, state.json should update to:
```json
{
  "current_task": null,
  "status": "idle",
  "last_completed": "hello-001"
}
```

---

## Key Takeaways

- AI reads state before acting
- AI follows structured protocol
- Changes are verified before completion
- State is updated after success

This is the AHES workflow at its simplest.
