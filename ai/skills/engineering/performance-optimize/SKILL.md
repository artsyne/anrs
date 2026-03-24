---
name: performance-optimize
description: |
  Optimize code performance with measurement and validation. Use when:
  (1) Performance issues identified
  (2) Need to improve response time or throughput
  (3) Optimizing based on profiling data
---

# Performance Optimization

Improve code performance based on measurement, not guessing.

## Input

```yaml
target: string         # What to optimize
current_metric: number # Current performance
goal_metric: number    # Target performance
```

## Output

```yaml
optimizations_applied: list
new_metric: number
improvement_percent: number
```

## Checklist

- [ ] Baseline measured
- [ ] Bottleneck identified
- [ ] Optimization applied
- [ ] New measurement taken
- [ ] Improvement validated
- [ ] No regressions

## Execution

### 1. Measure Baseline

```bash
go test -bench=. -benchmem > baseline.txt
go test -cpuprofile=cpu.prof
go tool pprof cpu.prof
```

### 2. Identify Bottleneck

Common bottlenecks:
- N+1 queries
- Unnecessary allocations
- Missing indexes
- Inefficient algorithms
- Missing caching

### 3. Optimize

```go
// Before: N+1 queries
for _, user := range users {
    orders := db.GetOrders(user.ID)
}

// After: Batch query
userIDs := extractIDs(users)
orders := db.GetOrdersForUsers(userIDs)
```

### 4. Validate

```bash
go test -bench=. -benchmem > optimized.txt
benchstat baseline.txt optimized.txt
```

## Optimization Techniques

| Technique | Impact | Risk |
|-----------|--------|------|
| Add index | High | Low |
| Caching | High | Medium |
| Batch queries | High | Low |
| Algorithm change | High | High |
| Remove allocations | Medium | Low |

## Constraints

- MUST measure before optimizing
- MUST validate improvement
- MUST check for regressions
- NO premature optimization

## Related

- `harness/evaluators/l2_dynamic_tests.py` — Benchmark runner
- `harness/metrics/performance.json` — Performance metrics
