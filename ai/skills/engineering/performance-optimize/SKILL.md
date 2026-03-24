# Skill: Performance Optimization

<!--
  ⚡ SKILL: performance-optimize
  
  Optimize code performance with measurement and validation.
-->

---

## 🎯 Purpose

Improve code performance based on measurement, not guessing.

---

## 📥 Input

```yaml
target: string         # What to optimize
current_metric: number # Current performance
goal_metric: number    # Target performance
```

---

## 📤 Output

```yaml
optimizations_applied: list
new_metric: number
improvement_percent: number
```

---

## 📋 Checklist

- [ ] Baseline measured
- [ ] Bottleneck identified
- [ ] Optimization applied
- [ ] New measurement taken
- [ ] Improvement validated
- [ ] No regressions

---

## 🔧 Execution

### Step 1: Measure Baseline

```bash
# Run benchmark
go test -bench=. -benchmem > baseline.txt

# Profile
go test -cpuprofile=cpu.prof
go tool pprof cpu.prof
```

### Step 2: Identify Bottleneck

```
Common bottlenecks:
- N+1 queries
- Unnecessary allocations
- Missing indexes
- Inefficient algorithms
- Missing caching
```

### Step 3: Optimize

```go
// Before: N+1 queries
for _, user := range users {
    orders := db.GetOrders(user.ID)
}

// After: Batch query
userIDs := extractIDs(users)
orders := db.GetOrdersForUsers(userIDs)
```

### Step 4: Validate

```bash
# Run benchmark again
go test -bench=. -benchmem > optimized.txt

# Compare
benchstat baseline.txt optimized.txt
```

---

## 📊 Optimization Checklist

| Technique | Impact | Risk |
|-----------|--------|------|
| Add index | High | Low |
| Caching | High | Medium |
| Batch queries | High | Low |
| Algorithm change | High | High |
| Remove allocations | Medium | Low |

---

## ⚠️ Constraints

- MUST measure before optimizing
- MUST validate improvement
- MUST check for regressions
- NO premature optimization

---

## 🔗 Related

- `harness/evaluators/l2_dynamic_tests.py` — Benchmark runner
- `harness/metrics/performance.json` — Performance metrics
