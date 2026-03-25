# Harness (Quality Gate)

The harness is ANRS's quality verification system.

## Purpose

Harness ensures AI-generated code:
- Compiles correctly
- Passes tests
- Meets quality standards
- Has no security issues

## Evaluation Levels

| Level | Name | Checks |
|-------|------|--------|
| L1 | Static | Syntax, lint, complexity |
| L2 | Dynamic | Unit tests, coverage |
| L3 | Stability | Risk analysis |
| Security | Scan | Vulnerabilities |

## Running Harness

### Via CLI

```bash
# Run all levels
anrs harness

# Run specific level
anrs harness --level L1
anrs harness --level L2

# Strict mode (fail on any error)
anrs harness --strict
```

### Via Python

```bash
# If .anrs/harness/quality_gate.py exists (full level)
python .anrs/harness/quality_gate.py --level L1
```

## Integration

Harness is mandatory before commits:

```
1. IMPLEMENT code
2. RUN harness
3. IF PASS: commit
4. IF FAIL: fix and retry
```

## Graceful Degradation

If tools are missing, harness returns `SKIP` instead of `FAIL`:

```json
{
  "level": "L1",
  "status": "SKIP",
  "message": "ruff not installed"
}
```

## Custom Harness

For project-specific checks (requires `anrs init --level full`):

```
your-project/
└── .anrs/
    └── harness/          # Quality gate
        ├── config.json   # Harness configuration
        └── ... (custom scripts)
```

Add custom evaluators and configure in `.anrs/harness/config.json`.
