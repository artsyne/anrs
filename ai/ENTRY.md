# AI Agent Entry Point

<!--
  🤖 AI AGENT: This is your entry point.
  
  READ THIS FILE FIRST before any action.
  FOLLOW the protocol defined below.
  DO NOT deviate from the standard execution loop.
-->

---

## 🎯 Purpose

This file defines the **mandatory execution protocol** for all AI agents working in this repository.

---

## 📋 Standard Execution Loop

```
┌─────────────────────────────────────────────────┐
│              AHES Execution Loop                │
└─────────────────────────────────────────────────┘

LOOP:
  1. READ state         → ai/state/state.json
  2. LOCATE task        → plans/active/{task_id}.md
  3. SELECT skill       → ai/skills/index.json
  4. EXECUTE skill      → ai/skills/{category}/{skill}/SKILL.md
  5. RUN harness        → ./scripts/run_harness.sh
  
  IF harness PASS:
    → atomic commit     → ai/skills/core/atomic-commit/
    → update state      → ai/skills/core/update-state/
    → cleanup scratchpad
    
  IF harness FAIL:
    → reflection        → ai/skills/core/reflection/
    → write to SCRATCHPAD
    → new plan
    → RETRY (goto step 4)
```

---

## 🚫 Prohibited Actions

1. **DO NOT** modify code without a plan in `plans/active/`
2. **DO NOT** skip the harness evaluation
3. **DO NOT** directly modify `state.json` (use `update-state` skill)
4. **DO NOT** commit without passing harness
5. **DO NOT** use skills not registered in `ai/skills/index.json`

---

## 📁 Key Files Reference

| File | Purpose |
|------|---------|
| `ai/state/state.json` | Current task state (SSOT) |
| `ai/orchestrator/ORCHESTRATOR.md` | Detailed execution protocol |
| `ai/rules/global.md` | Global constraints |
| `ai/skills/index.json` | Skill registry |
| `harness/quality_gate.py` | Evaluation entry |

---

## ⚡ Quick Decision Tree

```
What should I do?

├── Starting a new task?
│   └── Read state.json → Find task in plans/active/ → Execute
│
├── Task already in progress?
│   └── Read state.json → Continue from last checkpoint
│
├── Harness failed?
│   └── Read error → Reflect → Update SCRATCHPAD → Retry
│
├── Task completed?
│   └── Atomic commit → Update state → Cleanup
│
└── Unsure?
    └── Read ai/orchestrator/ORCHESTRATOR.md
```

---

## 🔗 Next Steps

1. Read `ai/state/state.json` for current state
2. Read `ai/orchestrator/ORCHESTRATOR.md` for detailed protocol
3. Read `ai/rules/global.md` for constraints
