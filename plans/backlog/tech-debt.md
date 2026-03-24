---
name: tech-debt
description: |
  Technical debt tracker. Read when:
  (1) Reviewing known issues
  (2) Planning improvements
  (3) Prioritizing refactoring work
---

# Technical Debt

Known technical debt items awaiting resolution.

## Item Format

```
### [Priority] Title
- **Description**: What is the issue
- **Impact**: Why it matters
- **Effort**: Estimated fix time
- **Location**: Files/modules affected (optional)
```

## Current Items

### [Low] Add more evaluator implementations
- **Description**: Current harness evaluators are protocol skeletons
- **Impact**: Full evaluation requires real implementations
- **Effort**: 2-3 days per evaluator
- **Location**: `harness/evaluators/`

### [Medium] Add adapter auto-generation
- **Description**: `generate_adapters.sh` needs full implementation
- **Impact**: Manual adapter creation required currently
- **Effort**: 1 day
- **Location**: `scripts/generate_adapters.sh`

### [Low] Add more skill templates
- **Description**: Engineering and SRE skills need detailed checklists
- **Impact**: Skills work but provide less detailed guidance
- **Effort**: 1-2 hours per skill
- **Location**: `ai/skills/`

## Resolved

| Item | Resolution Date | Notes |
|------|-----------------|-------|
| *No resolved items yet* | - | - |
