---
name: tech-debt
description: |
  Technical debt tracker. Read when:
  (1) Reviewing known issues
  (2) Planning improvements
  (3) Prioritizing work
---

# Technical Debt

## Format

```
### [Priority] Title
- Description: What is the issue
- Impact: Why it matters
- Effort: Estimated fix time
```

## Debt Items

### [Low] Add more evaluator implementations
- Description: Current harness evaluators are placeholders
- Impact: Full evaluation requires real implementations
- Effort: 2-3 days per evaluator

### [Medium] Add adapter auto-generation
- Description: `generate_adapters.sh` needs full implementation
- Impact: Manual adapter creation required
- Effort: 1 day

### [Low] Add more skill templates
- Description: Engineering and SRE skills need detailed checklists
- Impact: Skills work but less detailed guidance
- Effort: 1-2 hours per skill

## Resolved

_No resolved items yet_
