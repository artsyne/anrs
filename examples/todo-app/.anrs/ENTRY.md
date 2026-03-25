---
name: entry-point
description: |
  AI Agent entry point for todo-app example. Read FIRST when:
  (1) Starting work in this project
  (2) Need execution protocol
---

# ANRS Entry Point

## Execution Protocol

```
1. READ state     → .anrs/state/state.json
2. LOCATE task    → plans/active/{task_id}.md
3. SELECT skill   → .anrs/skills/index.json
4. EXECUTE        → Modify src/
5. RUN harness    → ./harness/run.sh

PASS → Commit → Update state → Cleanup
FAIL → Analyze → Reflect → Retry (max 3) → Escalate
```

## Constraints

- NEVER skip harness
- NEVER modify state.json directly
- ONLY use registered skills
- ALWAYS read state first

## File Locations

- State: `.anrs/state/state.json`
- Skills: `.anrs/skills/index.json`
- Plans: `plans/active/`
- Harness: `harness/run.sh`
