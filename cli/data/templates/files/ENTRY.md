# ANRS Entry Point

> **Read this file FIRST** before taking any action in this repository.

## Protocol

1. **READ** state → `.anrs/state.json`
2. **LOCATE** task → `.anrs/plans/active/{task_id}.md`
3. **EXECUTE** → Follow plan steps, modify only allowed files
4. **VERIFY** → Run harness before completion
5. **COMPLETE** → Update state, commit changes

## Constraints

- **NEVER** skip harness verification
- **NEVER** modify `.anrs/state.json` directly (use `update-state` skill)
- **ALWAYS** read state before acting
- **ONLY** modify files within allowed scope

## File Locations

| File | Purpose |
|------|---------|
| `.anrs/state.json` | Current task state (SSOT) |
| `.anrs/config.json` | Project configuration |
| `.anrs/plans/active/` | Current task plans |
| `.anrs/harness/` | Quality verification scripts (full level) |

## On Failure

If harness fails:
1. Analyze the failure message
2. Fix the issue
3. Re-run harness
4. If still failing after 3 attempts → Escalate to human
