# Default Strategy

<!--
  📋 DEFAULT EXECUTION STRATEGY
  
  Standard protocol for normal development tasks.
-->

---

## 🎯 When to Use

- New feature implementation
- Bug fixes (non-critical)
- Documentation updates
- Test additions

---

## 📋 Protocol

### Pre-Execution

1. **Verify** task is in `plans/active/`
2. **Read** current state
3. **Check** no blockers exist

### Execution

1. **Select** appropriate skill based on task type
2. **Execute** skill with full checklist
3. **Run** harness (L1 → L2 → L3)

### Post-Execution

- **On Success**: Commit → Update State → Cleanup
- **On Failure**: Reflect → Retry (max 3)

---

## 🔧 Configuration

```yaml
strategy: default
max_retries: 3
harness_levels: [L1, L2, L3]
commit_style: atomic
```

---

## 📊 Decision Matrix

```
Task Type           → Skill Selection
────────────────────────────────────────
New feature         → test-driven-dev
Bug fix             → execute-plan
Refactoring         → (use refactor.md strategy)
Documentation       → write-plan
```
