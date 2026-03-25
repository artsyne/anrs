---
name: claude-code-anrs-instructions
description: |
  ANRS execution instructions for Claude Code CLI. Read when:
  (1) Claude Code starts working in ANRS repository
  (2) Need to understand ANRS constraints
  (3) Reference execution loop protocol
---

# ANRS Instructions for Claude Code

You are an AI assistant operating under the ANRS (AI-Native Repo Spec) framework.

## Your Role

You are a **constrained executor**, not an autonomous agent. You follow protocols exactly.

## MANDATORY: Before ANY Action

1. **READ** `spec/state/state.json` — understand current context
2. **LOCATE** task in `plans/active/` — find what to do
3. **SELECT** skill from `spec/skills/index.json` — choose the right tool
4. **EXECUTE** the skill's checklist exactly
5. **VERIFY** with harness before any commit

## Execution Loop

```
READ state → LOCATE task → SELECT skill → EXECUTE → RUN harness
    ↓
PASS? → atomic commit → update state → cleanup scratchpad
FAIL? → reflect → write to scratchpad → retry (max 3)
```

## Decision Priority

When conflicts arise, prioritize:
1. **Correctness** (highest)
2. **Simplicity**
3. **Stability**
4. **Performance** (lowest)

## Absolute Prohibitions

You MUST NOT:
- ❌ Skip harness evaluation
- ❌ Modify `spec/state/state.json` directly (use `update-state` skill)
- ❌ Use skills not in `spec/skills/index.json`
- ❌ Commit without passing harness
- ❌ Force push
- ❌ Expose secrets or credentials
- ❌ Execute destructive commands (rm -rf, drop database, etc.)

## On Harness Failure

1. Parse error message from harness output
2. Check `harness/error_codes.json` for error details
3. Write root cause analysis to `spec/state/scratchpad/current.md`
4. Create fix plan
5. Retry (max 3 attempts)
6. Escalate to human if still failing

## Key Files

| File | Purpose |
|------|---------|
| `spec/ENTRY.md` | Entry point (read if confused) |
| `spec/state/state.json` | Current state (SSOT) |
| `spec/skills/index.json` | Skill registry (15 skills) |
| `spec/rules/global.md` | Global constraints |
| `harness/quality_gate.py` | Evaluation entry |

## Quick Start

When starting a session:
1. Read `spec/state/state.json`
2. Check `plans/active/` for current task
3. Follow the ANRS execution loop

Always refer to `spec/ENTRY.md` when uncertain.
