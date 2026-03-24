# AHES Entry Point (Hello World)

You are an AI agent operating under the AHES framework.

---

## Current Task

Read `ai/state/state.json` to get the current task.

---

## Protocol

1. READ state.json
2. IF current_task exists:
   - Implement the required change in src/
   - Run harness/check.sh
   - IF pass: update state to idle
   - IF fail: analyze and retry
3. IF no task: wait for instructions

---

## Constraints

- Only modify files in src/
- Always run harness before considering task complete
- Update state.json after successful completion
