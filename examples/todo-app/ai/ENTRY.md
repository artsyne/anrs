# AHES Entry Point

You are an AI agent operating under the AHES framework.

---

## Execution Protocol

```
LOOP:
  1. READ state     → ai/state/state.json
  2. LOCATE task    → plans/active/{task_id}.md
  3. SELECT skill   → ai/skills/index.json
  4. EXECUTE        → Modify src/ per skill checklist
  5. RUN harness    → ./harness/run.sh

  IF harness PASS:
    → Commit changes
    → Update state to idle
    → Cleanup scratchpad

  IF harness FAIL:
    → Analyze error
    → Write reflection to scratchpad
    → Retry (max 3 times)
    → Escalate if still failing
```

---

## Constraints

- NEVER skip harness evaluation
- NEVER modify state.json directly (update through protocol)
- ONLY use skills registered in ai/skills/index.json
- ALWAYS read state before any action

---

## File Locations

- State: `ai/state/state.json`
- Skills: `ai/skills/index.json`
- Active Plans: `plans/active/`
- Harness: `harness/run.sh`
