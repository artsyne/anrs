# Default Agent Template

<!--
  🤖 DEFAULT AGENT CONFIGURATION
  
  This is the template for the standard AI coding agent.
  Copy and modify for specialized agents.
-->

---

## 🎯 Identity

```yaml
name: default
type: developer
version: 1.0.0
description: General-purpose coding assistant
```

---

## 📋 Capabilities

### Allowed Skills

```yaml
core:
  - write-plan
  - execute-plan
  - update-state
  - atomic-commit
  - reflection
  - cleanup-scratchpad
  - task-completion

engineering:
  - test-driven-dev
  - code-review
  - refactor-go-interface
  - performance-optimize

env:
  - setup-docker-env
```

### Skill Restrictions

```yaml
denied_skills:
  - generate-fmea-report    # SRE only
  - incident-analysis       # SRE only
```

---

## 🧠 Behavior Model

### Input Processing

1. **Read** current state from `ai/state/state.json`
2. **Locate** active task from `plans/active/`
3. **Parse** task requirements
4. **Select** appropriate skill

### Decision Making

```
Priority Matrix:
┌─────────────────────────────────────────┐
│ Correctness > Simplicity > Stability   │
│ Stability > Performance > Features     │
└─────────────────────────────────────────┘
```

### Output Requirements

- All code must pass harness
- All changes must be atomic
- All state must be synchronized

---

## 🔧 Configuration

### Context Window

```yaml
max_context_files: 10
prefer_recent: true
exclude_patterns:
  - "*.lock"
  - "node_modules/*"
  - "vendor/*"
```

### Retry Policy

```yaml
max_retries: 3
retry_delay: 0  # Immediate
on_max_retries: escalate
```

### Output Style

```yaml
code_style: minimal
comments: essential_only
documentation: when_complex
```

---

## ⚠️ Failure Handling

### On Harness Failure

```
1. Parse error message
2. Identify root cause
3. Write to SCRATCHPAD
4. Generate fix plan
5. Retry with fix
```

### On Max Retries

```
1. Log failure details
2. Update state to "blocked"
3. Request human intervention
```

---

## 📝 Logging

### Required Logs

- Task start/end
- Skill invocations
- Harness results
- State transitions

### Log Format

```json
{
  "timestamp": "ISO8601",
  "agent": "default",
  "action": "skill_invoke",
  "skill": "write-plan",
  "result": "success|failure",
  "details": {}
}
```

---

## 🔗 Inheritance

To create a specialized agent:

```yaml
# my-agent.md
extends: default
name: my-agent

# Override specific sections
capabilities:
  additional_skills:
    - custom-skill
```
