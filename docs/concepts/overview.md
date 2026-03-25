---
name: system-architecture
description: |
  ANRS framework architecture overview. Read when:
  (1) Understanding component relationships
  (2) Learning data flow
  (3) Integrating with external systems
---

# System Architecture

ANRS is a protocol-driven framework for AI-assisted software development.

## Components

```
User Project (after anrs init)
├── .anrs/
│   ├── ENTRY.md       → AI entry point
│   ├── state.json     → Execution state (SSOT)
│   ├── config.json    → Project configuration
│   ├── scratchpad.md  → Temporary notes
│   ├── plans/         → Task plans
│   ├── skills/        → Custom skills (full level)
│   └── failure-cases/ → Failed attempts (full level)
├── harness/           → Quality gate (full level)
└── .cursorrules       → AI adapter
```

## Data Flow

```
User Request → Read State → Load Plan → Select Skill → Execute
                                                         ↓
                                                    Run Harness
                                                         ↓
                                              PASS? → Commit
                                              FAIL? → Reflect & Retry
```

## Access Control

| Component | Read | Write |
|-----------|------|-------|
| Rules | All | Admin |
| State | All | Orchestrator |
| Skills | All | Registry |
| Code | All | Skill Execution |

## Trust Boundaries

**Trusted Zone**: Harness, State
**Untrusted Zone**: AI Agent, Code Output

## Integration

Adapters (installed via `anrs adapter install`):
- Cursor: `.cursorrules`
- Claude Code: `CLAUDE.md`
- Codex: `AGENTS.md`
- OpenCode: `opencode.json`

External: Git, GitHub Actions, CI/CD pipelines
