---
name: update-state
description: |
  Safely update the state.json file. Use when:
  (1) Task status changes (idle/running/completed/failed)
  (2) Current task assignment changes
  (3) Execution context needs to be recorded
---

# Update State

Update state.json following the schema and access rules.

## Input

```yaml
updates:
  status: string       # New status (optional)
  current_task: string # Task ID (optional)
  execution: object    # Execution context (optional)
```

## Output

```yaml
state_updated: boolean
previous_state: object
new_state: object
```

## Checklist

- [ ] Read current state
- [ ] Validate updates against schema
- [ ] Apply updates
- [ ] Write state file

## Execution

### 1. Read Current

```json
// Read .anrs/state.json
{
  "status": "running",
  "current_task": "task-001"
}
```

### 2. Validate Updates

1. Check field names are valid
2. Check values match schema types
3. Check enum values are allowed
4. Check required fields present

### 3. Apply Updates

```json
{
  ...current_state,
  ...updates,
  "last_updated": "NOW()"
}
```

### 4. Write State

1. Validate complete state against schema
2. Write to `.anrs/state.json`
3. Verify write success

## Constraints

- ONLY this skill can write to state.json
- Must validate against schema
- Must update timestamp

## Related

- `.anrs/state.json` — State file
- `.anrs/state.schema.json` — Schema
