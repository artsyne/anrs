# Global Rules

<!--
  ⚖️ HIGHEST PRIORITY RULES
  
  These rules apply to ALL AI agents and ALL tasks.
  Violation of any rule is a critical failure.
-->

---

## 🔴 Critical Constraints (MUST)

### 1. Harness First

- **MUST** run harness after every code change
- **MUST** pass all harness checks before commit
- **MUST NOT** bypass harness under any circumstance

### 2. Transactional Integrity

- **MUST** use atomic commit for all changes
- **MUST** sync state.json with code changes
- **MUST** be able to rollback any change

### 3. Plan Before Code

- **MUST** have a plan in `plans/active/` before coding
- **MUST NOT** modify code without approved plan
- **MUST** update plan if requirements change

### 4. Skill-Based Execution

- **MUST** use registered skills only
- **MUST NOT** improvise outside skill definitions
- **MUST** follow skill checklists completely

### 5. State Management

- **MUST** read state.json before any action
- **MUST** update state.json after task completion
- **MUST NOT** directly edit state.json (use update-state skill)

---

## 🟡 Guidelines (SHOULD)

### 1. Simplicity First

- **SHOULD** prefer simple solutions over clever ones
- **SHOULD** avoid premature optimization
- **SHOULD** keep changes minimal and focused

### 2. Stability Over Features

- **SHOULD** prioritize stability over new features
- **SHOULD** add tests before new code
- **SHOULD** consider failure modes

### 3. Documentation

- **SHOULD** document non-obvious decisions
- **SHOULD** update docs when behavior changes
- **SHOULD** keep docs concise

---

## 🟢 Preferences (MAY)

### 1. Performance

- **MAY** optimize after correctness is verified
- **MAY** use caching if complexity is justified
- **MAY** parallelize if safe

### 2. Tooling

- **MAY** use external tools if registered
- **MAY** create new skills if needed
- **MAY** suggest adapter improvements

---

## ⚠️ Error Handling

When a rule is violated:

1. **STOP** current action immediately
2. **LOG** the violation in scratchpad
3. **REFLECT** on the cause
4. **RECOVER** using rollback if needed
5. **RETRY** with corrected approach

---

## 📝 Rule Precedence

```
1. Critical Constraints (MUST)     ← Highest
2. Guidelines (SHOULD)
3. Preferences (MAY)               ← Lowest
```

When rules conflict, higher precedence wins.
