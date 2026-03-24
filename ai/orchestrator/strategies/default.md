---
name: default-strategy
description: |
  Standard execution strategy. Use when:
  (1) New feature implementation
  (2) Bug fixes (non-critical)
  (3) Documentation updates
  (4) Test additions
---

# Default Strategy

## Protocol

**Pre-Execution**:
1. Verify task in `plans/active/`
2. Read current state
3. Check no blockers

**Execution**:
1. Select skill based on task type
2. Execute skill with full checklist
3. Run harness (L1 → L2 → L3)

**Post-Execution**:
- Success: Commit → Update State → Cleanup
- Failure: Reflect → Retry (max 3)

## Config

```yaml
strategy: default
max_retries: 3
harness_levels: [L1, L2, L3]
commit_style: atomic
```

## Skill Selection

```
New feature   → test-driven-dev
Bug fix       → execute-plan
Refactoring   → use refactor.md
Documentation → write-plan
```
