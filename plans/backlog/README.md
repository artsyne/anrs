---
name: backlog-index
description: |
  Future work and technical debt tracker. Read when:
  (1) Planning upcoming work
  (2) Reviewing technical debt
  (3) Prioritizing tasks for promotion to active/
---

# Backlog

Future tasks, feature requests, and technical debt awaiting execution.

## Structure

```
backlog/
├── README.md         # This index
├── tech-debt.md      # Technical debt items
└── {feature}.md      # Future feature plans
```

## Item Format

```markdown
### [Priority] Title
- **Description**: What is the issue/feature
- **Impact**: Why it matters
- **Effort**: Estimated time (S/M/L or hours/days)
- **Dependencies**: Prerequisites (optional)
```

## Priorities

| Priority | Meaning | Action |
|----------|---------|--------|
| **Critical** | Blocking issues | Promote to active immediately |
| **High** | Important improvements | Schedule for next sprint |
| **Medium** | Nice to have | Plan when capacity allows |
| **Low** | Minor enhancements | Track for future |

## Workflow

```
1. Add item to backlog/{category}.md
2. Review and prioritize regularly
3. When ready: promote to plans/active/task-{id}.md
4. After completion: archive to plans/completed/
```

## Current Backlog Files

| File | Description |
|------|-------------|
| [tech-debt.md](tech-debt.md) | Technical debt and code quality issues |
