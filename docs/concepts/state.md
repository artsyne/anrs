# State Management

ANRS uses `state.json` as the Single Source of Truth (SSOT) for AI execution.

## Purpose

State management ensures:
- AI knows the current task
- AI knows its execution status
- No context is lost between sessions

## State File

Location: `.anrs/state.json`

```json
{
  "current_task": "task-001",
  "status": "in_progress",
  "last_completed": "task-000",
  "context": {
    "project_type": "python",
    "language": "python"
  },
  "metadata": {
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
}
```

## Status Values

| Status | Meaning |
|--------|---------|
| `idle` | No active task |
| `pending` | Task assigned, not started |
| `in_progress` | Task being executed |
| `blocked` | Waiting for input |

## Usage

### AI reads state first

```
1. READ .anrs/state.json
2. IF current_task: Load task from .anrs/plans/active/
3. EXECUTE task
4. UPDATE state on completion
```

### State updates

AI should use the `update-state` skill rather than editing directly.

## Best Practices

- **Never edit state.json manually** during AI execution
- **Always backup** before major changes
- **Use scratchpad** for temporary notes, not state
