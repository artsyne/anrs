---
name: global-rules
description: |
  Global constraints for all AI agents. Read when:
  (1) Starting any task
  (2) Making decisions about allowed/denied actions
  (3) Understanding rule precedence
---

# Global Rules

## Critical Constraints (MUST)

### Harness First
- MUST run harness after every code change
- MUST pass all checks before commit
- MUST NOT bypass harness

### Transactional Integrity
- MUST use atomic commit for all changes
- MUST sync state.json with code changes
- MUST be able to rollback any change

### Plan Before Code
- MUST have plan in `plans/active/` before coding
- MUST NOT modify code without approved plan
- MUST update plan if requirements change

### Skill-Based Execution
- MUST use registered skills only
- MUST NOT improvise outside skill definitions
- MUST follow skill checklists completely

### State Management
- MUST read state.json before any action
- MUST update state.json after task completion
- MUST NOT directly edit state.json (use update-state skill)

## Guidelines (SHOULD)

- SHOULD prefer simple solutions over clever ones
- SHOULD avoid premature optimization
- SHOULD keep changes minimal and focused
- SHOULD prioritize stability over new features
- SHOULD add tests before new code
- SHOULD document non-obvious decisions

## Preferences (MAY)

- MAY optimize after correctness is verified
- MAY use caching if complexity is justified
- MAY create new skills if needed

## Error Handling

When rule violated: STOP → LOG → REFLECT → RECOVER → RETRY

## Rule Precedence

```
1. Critical (MUST)  ← Highest
2. Guidelines (SHOULD)
3. Preferences (MAY) ← Lowest
```
