---
name: default-agent
description: |
  Default agent template. Read when:
  (1) Need full default agent configuration
  (2) Creating specialized agents (copy and modify)
  (3) Understanding agent behavior model
---

# Default Agent

```yaml
name: default
type: developer
version: 1.0.0
description: General-purpose coding assistant
```

## Capabilities

```yaml
core: [write-plan, execute-plan, update-state, atomic-commit, reflection, cleanup-scratchpad, task-completion]
engineering: [test-driven-dev, code-review, refactor-go-interface, performance-optimize]
env: [setup-docker-env]

denied_skills: [risk-analysis, incident-analysis]  # SRE only
```

## Behavior Model

**Input Processing**:
1. Read state from `spec/state/state.json`
2. Locate task from `plans/active/`
3. Parse requirements, select skill

**Priority**: `Correctness > Simplicity > Stability > Performance`

**Output Requirements**:
- All code must pass harness
- All changes must be atomic
- All state must be synchronized

## Configuration

```yaml
context:
  max_files: 10
  prefer_recent: true
  exclude: ["*.lock", "node_modules/*", "vendor/*"]

retry:
  max_retries: 3
  delay: 0
  on_max: escalate

output:
  code_style: minimal
  comments: essential_only
  documentation: when_complex
```

## Failure Handling

**On Harness Failure**:
1. Parse error → 2. Identify root cause → 3. Write to SCRATCHPAD → 4. Generate fix plan → 5. Retry

**On Max Retries**:
1. Log failure → 2. Set status "blocked" → 3. Request human intervention

## Inheritance

```yaml
# To create specialized agent:
extends: default
name: my-agent
capabilities:
  additional_skills: [custom-skill]
```
