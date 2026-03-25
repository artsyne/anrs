---
name: entry-point
description: |
  AI Agent entry point for hello-world example. Read FIRST when:
  (1) Starting work in this project
  (2) Need execution protocol
---

# ANRS Entry Point (Hello World)

## Protocol

1. READ `ai/state/state.json`
2. IF current_task: Implement in src/ → Run harness/check.sh → Update state
3. IF no task: Wait for instructions

## Constraints

- Only modify files in src/
- Always run harness before completion
- Update state.json after success
