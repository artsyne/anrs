"""Tests for Todo module."""

import pytest
from src.todo import add_todo, list_todos, complete_todo


class TestAddTodo:
    def test_add_todo_returns_dict(self):
        result = add_todo("Test task")
        assert isinstance(result, dict)

    def test_add_todo_has_id(self):
        result = add_todo("Test task")
        assert "id" in result

    def test_add_todo_has_text(self):
        result = add_todo("Test task")
        assert result["text"] == "Test task"

    def test_add_todo_not_completed_by_default(self):
        result = add_todo("Test task")
        assert result["completed"] is False


class TestListTodos:
    def test_list_todos_returns_list(self):
        result = list_todos()
        assert isinstance(result, list)


class TestCompleteTodo:
    def test_complete_existing_todo(self):
        todo = add_todo("Task to complete")
        result = complete_todo(todo["id"])
        assert result is True

    def test_complete_nonexistent_todo(self):
        result = complete_todo("nonexistent-id")
        assert result is False
