# Skill: Code Review

<!--
  🔍 SKILL: code-review
  
  Review code for quality, security, and best practices.
-->

---

## 🎯 Purpose

Systematically review code to identify issues and improvements.

---

## 📥 Input

```yaml
files: list            # Files to review
focus_areas: list      # Specific concerns (optional)
```

---

## 📤 Output

```yaml
issues: list
suggestions: list
approved: boolean
```

---

## 📋 Checklist

- [ ] Code compiles/runs
- [ ] Tests pass
- [ ] No security issues
- [ ] Follows coding standards
- [ ] No obvious bugs
- [ ] Documentation adequate

---

## 🔧 Execution

### Step 1: Static Analysis

```
Check for:
- Syntax errors
- Lint violations
- Type errors
- Unused code
```

### Step 2: Logic Review

```
Check for:
- Correct behavior
- Edge cases handled
- Error handling
- Resource cleanup
```

### Step 3: Security Review

```
Check for:
- Input validation
- SQL injection
- XSS vulnerabilities
- Secrets in code
```

### Step 4: Quality Review

```
Check for:
- Code readability
- Naming conventions
- Function size
- Complexity
```

---

## 📊 Issue Categories

| Category | Priority |
|----------|----------|
| Security | Critical |
| Bug | High |
| Performance | Medium |
| Style | Low |

---

## 📝 Review Output Format

```markdown
## Code Review: {file}

### Issues

#### [Critical] Security: SQL Injection
- Line: 45
- Issue: User input directly in query
- Fix: Use parameterized query

### Suggestions

#### [Low] Style: Function length
- Line: 100-180
- Suggestion: Extract into smaller functions

### Verdict
[ ] Approved
[x] Changes Required
```

---

## ⚠️ Constraints

- Review ONE file at a time
- Document ALL issues found
- Provide actionable fixes

---

## 🔗 Related

- `ai/rules/coding.md` — Coding standards
- `ai/rules/safety.md` — Security rules
