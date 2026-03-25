# Skill System

Skills are structured instructions that guide AI behavior.

## What is a Skill?

A skill is a markdown file containing:
- **Input**: What the skill needs
- **Output**: What it produces
- **Checklist**: Steps to follow
- **Execution**: Detailed instructions

## Skill Structure

```markdown
---
name: skill-name
description: |
  When to use this skill.
---

# Skill Name

## Input
- Required input

## Output
- Expected output

## Checklist
- [ ] Step 1
- [ ] Step 2

## Execution
Detailed steps...
```

## Skill Categories

| Category | Purpose |
|----------|---------|
| `core/` | Essential operations (update-state, reflection) |
| `engineering/` | Development tasks (code-review, test-driven-dev) |
| `sre/` | Operations (incident-analysis, risk-analysis) |
| `env/` | Environment setup |

## Using Skills

### AI selects skill from registry

```
1. READ state
2. LOCATE task
3. SELECT skill from spec/skills/index.json
4. EXECUTE skill checklist
```

### Skill Registry

Location: `spec/skills/index.json`

```json
{
  "skills": [
    {
      "name": "update-state",
      "path": "core/update-state/SKILL.md"
    }
  ]
}
```

## Custom Skills

Add project-specific skills to `.anrs/skills/`:

```
.anrs/
└── skills/
    └── my-custom-skill/
        └── SKILL.md
```
