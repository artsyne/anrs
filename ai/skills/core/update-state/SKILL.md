# Skill: Update State

<!--
  🔄 SKILL: update-state
  
  Safely update the state.json file.
-->

---

## 🎯 Purpose

Update state.json following the schema and access rules.

---

## 📥 Input

```yaml
updates:
  status: string       # New status (optional)
  current_task: string # Task ID (optional)
  execution: object    # Execution context (optional)
```

---

## 📤 Output

```yaml
state_updated: boolean
previous_state: object
new_state: object
```

---

## 📋 Checklist

- [ ] Read current state
- [ ] Validate updates against schema
- [ ] Apply updates
- [ ] Validate new state
- [ ] Write state file

---

## 🔧 Execution

### Step 1: Read Current

```json
// Read ai/state/state.json
{
  "status": "running",
  "current_task": "task-001",
  ...
}
```

### Step 2: Validate Updates

```
1. Check field names are valid
2. Check values match schema types
3. Check enum values are allowed
4. Check required fields present
```

### Step 3: Apply Updates

```json
// Merge updates
{
  ...current_state,
  ...updates,
  "last_updated": "NOW()"
}
```

### Step 4: Write State

```
1. Validate complete state
2. Write to state.json
3. Verify write success
```

---

## ⚠️ Constraints

- ONLY this skill can write to state.json
- Must validate against schema
- Must preserve history
- Must update timestamp

---

## 🔗 Related

- `ai/state/state.json` — State file
- `ai/state/state.schema.json` — Schema
