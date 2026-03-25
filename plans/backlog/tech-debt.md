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

### [Low] Failure Case Machine-Readable Index
- **Description**: Failure cases are archived as Markdown files. Adding a `failure_index.json` would enable AI to perform pattern analysis and RAG retrieval.
- **Impact**: AI cannot efficiently analyze failure patterns across cases
- **Effort**: 1 day
- **Location**: `evals/failure-cases/`

### [Medium] Add adapter auto-generation
- **Description**: `generate_adapters.sh` needs full implementation
- **Impact**: Manual adapter creation required currently
- **Effort**: 1 day
- **Location**: `scripts/generate_adapters.sh`

### [Low] Add more skill templates
- **Description**: Engineering and SRE skills need detailed checklists
- **Impact**: Skills work but provide less detailed guidance
- **Effort**: 1-2 hours per skill
- **Location**: `spec/skills/`

## Resolved

| Item | Resolution Date | Notes |
|------|-----------------|-------|
| Add real evaluator implementations | 2026-03-25 | Integrated ruff, pytest, bandit, gitleaks |
