# Task: todo-001

## Objective

Implement basic Todo CRUD operations.

---

## Requirements

### 1. add_todo(text: str) -> dict

- Create a new todo item
- Generate unique ID
- Return the created todo

### 2. list_todos() -> list

- Return all todos
- Include completed status

### 3. complete_todo(id: str) -> bool

- Mark todo as completed
- Return True if found, False otherwise

---

## Acceptance Criteria

- [ ] All functions implemented in src/todo.py
- [ ] Unit tests pass (tests/test_todo.py)
- [ ] No lint errors
- [ ] Type hints included

---

## Implementation Notes

- Use in-memory storage for simplicity
- ID format: "todo-{timestamp}"
