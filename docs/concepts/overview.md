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
ANRS Framework
├── Rules (spec/rules/)      → Constraints & standards
├── State (spec/state/)      → Execution state (SSOT)
├── Skills (spec/skills/)    → Executable actions
├── Orchestrator (spec/orchestrator/) → Execution flow
└── Harness (harness/)     → Code quality evaluation
```

### Directory Layout

```
spec/rules/        → global.md, coding.md, safety.md
spec/state/        → state.json, scratchpad/
spec/skills/       → index.json, core/, engineering/, sre/
spec/orchestrator/ → ORCHESTRATOR.md, strategies/
harness/         → quality_gate.py, evaluators/ (L1/L2/L3)
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

Adapters: `adapters/cursor/`, `adapters/claude-code/`, `adapters/codex/`
External: Git, GitHub Actions, Prometheus/Grafana
