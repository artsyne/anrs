---
name: debug-strategy
description: |
  Bug investigation strategy. Use when:
  (1) Runtime errors
  (2) Test failures
  (3) Performance issues
  (4) Unexpected behavior
---

# Debug Strategy

## Protocol

**Phase 1: Reproduce**
1. Read error message/logs
2. Identify reproduction steps
3. Create minimal test case
4. Verify reproducible

**Phase 2: Investigate**
1. Trace code execution path
2. Identify root cause
3. Document findings in scratchpad
4. Form hypothesis

**Phase 3: Fix**
1. Write failing test first
2. Implement minimal fix
3. Verify test passes
4. Check for regressions

**Phase 4: Validate**
1. Run full harness
2. Verify no new issues
3. Commit atomically
4. Document fix

## Config

```yaml
strategy: debug
max_retries: 5
harness_levels: [L1, L2, L3]
extra_logging: true
preserve_scratchpad: true
```

## Checklist

- [ ] Error captured
- [ ] Reproduction steps documented
- [ ] Root cause identified
- [ ] Test written before fix
- [ ] Fix is minimal
- [ ] No regressions
