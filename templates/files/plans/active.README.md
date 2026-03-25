# Active Plans

Task plans currently being executed.

## Usage

AI agents locate tasks here during the execution loop:

```
1. READ   → .anrs/state.json
2. LOCATE → plans/active/{task_id}.md  ← HERE
3. EXECUTE → Follow plan steps
4. VERIFY → Run harness
5. COMPLETE → Move to plans/completed/
```

## Workflow

```
plans/backlog/ → plans/active/ → plans/completed/
```
