---
name: dependency-map
description: |
  Project dependency requirements. Read when:
  (1) Setting up development environment
  (2) Checking version requirements
  (3) Troubleshooting missing dependencies
---

# Dependency Map

Format: `Package -> Dependency (version) [purpose]`

## Core Framework

```
ANRS -> Python (3.10+) [harness runtime]
ANRS -> Git (2.x) [version control]
ANRS -> JSON Schema (draft-07) [validation]
```

## Harness Dependencies

```
harness/quality_gate.py -> argparse [CLI]
harness/quality_gate.py -> json [parsing]
harness/quality_gate.py -> pathlib [file ops]
```

## Language-specific Tools (Optional)

### Go Projects
```
Go_Projects -> golangci-lint (1.55+) [linting]
Go_Projects -> gocyclo [complexity]
Go_Projects -> govulncheck [security]
```

### Python Projects
```
Python_Projects -> ruff (0.1+) [linting]
Python_Projects -> pytest (7+) [testing]
Python_Projects -> bandit [security]
```

### Node Projects
```
Node_Projects -> eslint (8+) [linting]
Node_Projects -> typescript (5+) [types]
Node_Projects -> vitest (1+) [testing]
```

## Adapter Dependencies

```
adapters/cursor -> Cursor IDE (0.40+)
adapters/claude -> Claude API (2024+)
adapters/openai -> OpenAI API (4+)
```
