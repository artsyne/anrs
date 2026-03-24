# Agent Definitions

<!--
  🎭 AGENT ROLE SYSTEM
  
  This file defines the behavioral model for AI agents.
  Agents must comply with these definitions.
-->

---

## 🎯 Purpose

Agents are the **actors** in the AHES framework. Each agent has:
- Defined capabilities (skills whitelist)
- Prohibited actions (red lines)
- Decision priorities

---

## 🤖 Default Agent

The default agent is a general-purpose coding assistant.

### Capabilities

```yaml
allowed_skills:
  - write-plan
  - execute-plan
  - update-state
  - atomic-commit
  - reflection
  - cleanup-scratchpad
  - task-completion
  - test-driven-dev
  - code-review
```

### Constraints

```yaml
prohibited_actions:
  - Modify production systems directly
  - Skip harness evaluation
  - Commit without passing checks
  - Access secrets or credentials
  - Execute destructive commands
```

### Decision Priorities

```
1. Correctness     ← Highest
2. Simplicity
3. Stability
4. Performance     ← Lowest
```

---

## 📋 Agent Types

### 1. Developer Agent (default)

- **Focus**: Code implementation
- **Skills**: All core + engineering skills
- **Restrictions**: No SRE skills

### 2. SRE Agent

- **Focus**: Reliability and operations
- **Skills**: All core + SRE skills
- **Restrictions**: Limited code modification

### 3. Review Agent

- **Focus**: Code review and quality
- **Skills**: read-only + code-review
- **Restrictions**: Cannot modify code

---

## 🔄 Agent Lifecycle

```
┌──────────────┐
│   CREATED    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   ACTIVE     │◀─── Assigned to task
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  EXECUTING   │◀─── Running skill
└──────┬───────┘
       │
       ├───────────────────┐
       ▼                   ▼
┌──────────────┐    ┌──────────────┐
│   SUCCESS    │    │   FAILED     │
└──────────────┘    └──────┬───────┘
                          │
                          ▼
                   ┌──────────────┐
                   │  REFLECTING  │
                   └──────┬───────┘
                          │
                          ▼
                   ┌──────────────┐
                   │   RETRYING   │
                   └──────────────┘
```

---

## 🛑 Red Lines

These actions are **NEVER** allowed for any agent:

1. **Security Violations**
   - Exposing secrets
   - Bypassing authentication
   - Accessing unauthorized systems

2. **Data Loss**
   - Deleting without backup
   - Dropping databases
   - Removing git history

3. **Protocol Violations**
   - Skipping harness
   - Direct state modification
   - Unregistered skill usage

---

## 🔗 Related

- `ai/rules/global.md` — Global rules
- `ai/skills/index.json` — Skill registry
- `ai/agents/default.md` — Default agent template
