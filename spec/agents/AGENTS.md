---
name: agent-definitions
description: |
  Agent role system overview. Read when:
  (1) Understanding agent types and capabilities
  (2) Checking allowed/denied skills for an agent
  (3) Creating specialized agents
---

# Agent Definitions

Agents are the actors in ANRS. Each agent has:
- Defined capabilities (skills whitelist)
- Prohibited actions (red lines)
- Decision priorities

## Agent Types

| Type | Focus | Skills | Restrictions |
|------|-------|--------|--------------|
| Developer (default) | Code implementation | core + engineering | No SRE skills |
| SRE | Reliability & operations | core + SRE | Limited code modification |
| Review | Code review & quality | read-only + code-review | Cannot modify code |

## Default Agent

```yaml
allowed_skills:
  - write-plan, execute-plan, update-state, atomic-commit
  - reflection, cleanup-scratchpad, task-completion
  - test-driven-dev, code-review

prohibited_actions:
  - Modify production directly
  - Skip harness
  - Commit without passing checks
  - Access secrets
  - Execute destructive commands

priority: Correctness > Simplicity > Stability > Performance
```

## Agent Lifecycle

```
CREATED → ACTIVE (assigned) → EXECUTING (running skill)
         → SUCCESS → [DONE]
         → FAILED → REFLECTING → RETRYING → ...
```

## Red Lines (NEVER allowed)

1. **Security**: Exposing secrets, bypassing auth, unauthorized access
2. **Data Loss**: Deleting without backup, dropping databases
3. **Protocol**: Skipping harness, direct state modification, unregistered skills

See `spec/agents/default.md` for full default agent template.
