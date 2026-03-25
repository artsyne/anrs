---
name: todo-001
description: |
  Implement basic Todo CRUD operations.
---

# Task: todo-001

## Objective

Implement basic Todo CRUD operations.

## Requirements

1. `add_todo(text: str) -> dict`: Create todo, generate unique ID, return created
2. `list_todos() -> list`: Return all todos with completed status
3. `complete_todo(id: str) -> bool`: Mark completed, return True if found

## Acceptance Criteria

- [ ] All functions in `src/todo.py`
- [ ] Unit tests pass (`tests/test_todo.py`)
- [ ] No lint errors
- [ ] Type hints included

## Notes

- Use in-memory storage
- ID format: "todo-{timestamp}"
