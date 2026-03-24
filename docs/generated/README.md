---
name: generated-docs-index
description: |
  Auto-generated documentation directory. Read when:
  (1) Looking for generated API docs
  (2) Finding auto-generated reports
  (3) Checking CI-generated artifacts
---

# Generated Documents

This directory contains auto-generated documentation. **Do not manually edit files here.**

## Generated Content Types

| Type | Source | Tool |
|------|--------|------|
| API docs | `src/` code comments | godoc / typedoc |
| Coverage reports | Test runs | go test / pytest |
| Dependency graphs | `go.mod` / `package.json` | go mod graph |

## Regeneration

```bash
# Regenerate all docs
./scripts/generate-docs.sh

# Or via CI
# Docs are auto-generated on main branch push
```

## Current Files

*No generated documents yet.*
