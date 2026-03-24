---
name: refactor-strategy
description: |
  Safe refactoring strategy. Use when:
  (1) Code cleanup
  (2) Architecture changes
  (3) Performance optimization
  (4) Technical debt reduction
---

# Refactor Strategy

## Protocol

**Phase 1: Analyze**
1. Map current code structure
2. Identify refactoring scope
3. Document expected changes
4. Verify test coverage exists

**Phase 2: Prepare**
1. Ensure all tests pass (baseline)
2. Create backup/branch point
3. Plan incremental changes
4. Define success criteria

**Phase 3: Execute**
1. Make ONE change at a time
2. Run harness after each change
3. Commit each successful change
4. Document changes made

**Phase 4: Verify**
1. Run full test suite
2. Compare behavior (before/after)
3. Check performance metrics
4. Review code quality

## Safety Rules

- NEVER refactor without tests
- ALWAYS commit incrementally
- VERIFY behavior preserved
- ROLLBACK if regression detected

## Config

```yaml
strategy: refactor
max_retries: 3
incremental_commits: true
rollback_on_regression: true
```

## Refactoring Types

```
Extract function   → Small, test after
Rename             → IDE-assisted, bulk
Move file          → Update imports, verify
Change interface   → Adapter pattern first
Performance        → Profile before/after
```
