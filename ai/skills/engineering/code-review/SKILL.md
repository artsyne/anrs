---
name: code-review
description: |
  Review code for quality, security, and best practices. Use when:
  (1) Before merging a pull request
  (2) Need systematic code quality assessment
  (3) Security or best practice audit required
---

# Code Review

Systematically review code to identify issues and improvements.

## Input

```yaml
files: list            # Files to review
focus_areas: list      # Specific concerns (optional)
```

## Output

```yaml
issues: list
suggestions: list
approved: boolean
```

## Checklist

- [ ] Code compiles/runs
- [ ] Tests pass
- [ ] No security issues
- [ ] Follows coding standards
- [ ] No obvious bugs

## Execution

### 1. Static Analysis

Check for:
- Syntax errors
- Lint violations
- Type errors
- Unused code

### 2. Logic Review

Check for:
- Correct behavior
- Edge cases handled
- Error handling
- Resource cleanup

### 3. Security Review

Check for:
- Input validation
- SQL injection
- XSS vulnerabilities
- Secrets in code

### 4. Quality Review

Check for:
- Code readability
- Naming conventions
- Function size
- Complexity

## Issue Categories

| Category | Priority |
|----------|----------|
| Security | Critical |
| Bug | High |
| Performance | Medium |
| Style | Low |

## Review Output Format

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

## Constraints

- Review ONE file at a time
- Document ALL issues found
- Provide actionable fixes

## Related

- `ai/rules/coding.md` — Coding standards
- `ai/rules/safety.md` — Security rules
