# Refactor Strategy

<!--
  ♻️ REFACTOR EXECUTION STRATEGY
  
  Protocol for safe code refactoring.
-->

---

## 🎯 When to Use

- Code cleanup
- Architecture changes
- Performance optimization
- Technical debt reduction

---

## 📋 Protocol

### Phase 1: Analyze

1. **Map** current code structure
2. **Identify** refactoring scope
3. **Document** expected changes
4. **Verify** test coverage exists

### Phase 2: Prepare

1. **Ensure** all tests pass (baseline)
2. **Create** backup/branch point
3. **Plan** incremental changes
4. **Define** success criteria

### Phase 3: Execute

1. **Make** ONE change at a time
2. **Run** harness after each change
3. **Commit** each successful change
4. **Document** changes made

### Phase 4: Verify

1. **Run** full test suite
2. **Compare** behavior (before/after)
3. **Check** performance metrics
4. **Review** code quality

---

## 🔧 Configuration

```yaml
strategy: refactor
max_retries: 3
harness_levels: [L1, L2, L3]
incremental_commits: true
rollback_on_regression: true
```

---

## ⚠️ Safety Rules

1. **NEVER** refactor without tests
2. **ALWAYS** commit incrementally
3. **VERIFY** behavior preserved
4. **ROLLBACK** if regression detected

---

## 📊 Refactoring Types

```
Type                    → Approach
────────────────────────────────────────
Extract function        → Small, test after
Rename                  → IDE-assisted, bulk
Move file               → Update imports, verify
Change interface        → Adapter pattern first
Performance             → Profile before/after
```
