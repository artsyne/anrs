---
name: harness-overview
description: |
  Harness evaluation system architecture. Read when:
  (1) Understanding quality gate execution flow
  (2) Implementing or extending evaluators
  (3) Debugging evaluation failures
---

# Harness Evaluation System

> **Implementation Status**: Protocol skeleton. Evaluators return placeholder results.
> Projects adopting ANRS should implement actual evaluation logic.

Multi-level quality gate for AI-assisted development.

## Execution Flow

```
quality_gate.py
│
├── Security (cross-level, runs first)
│   └── evaluators/security_scan.py
│       ├── dependency_scan
│       ├── secret_detection
│       └── sast
│
└── Cascade (stops on failure)
    ├── L1: evaluators/l1_static_checks.py
    │   ├── syntax
    │   ├── lint
    │   └── complexity
    │
    ├── L2: evaluators/l2_dynamic_tests.py
    │   ├── unit_tests
    │   ├── coverage
    │   └── contracts
    │
    └── L3: evaluators/l3_stability.py
        ├── risk_analysis (AI-driven)
        ├── slo
        └── chaos (optional)
```

## Usage

```bash
# Full evaluation (Security + L1 + L2 + L3)
python quality_gate.py -v

# Run up to L2 only
python quality_gate.py --level L2 -v

# Skip security checks
python quality_gate.py --skip-security -v

# JSON output
python quality_gate.py --json
```

## Components

| File | Purpose |
|------|---------|
| `quality_gate.py` | Main entry point, orchestrates evaluation |
| `evaluators/l1_static_checks.py` | Syntax, lint, complexity |
| `evaluators/l2_dynamic_tests.py` | Tests, coverage, contracts |
| `evaluators/l3_stability.py` | Risk analysis, SLO, chaos |
| `evaluators/security_scan.py` | Security scans (cross-level) |
| `metrics/code_quality.json` | Quality thresholds config |
| `error_codes.json` | Error code definitions |
| `reports/` | Evaluation reports output |

## Output Schema

```json
{
  "result": "PASS|FAIL",
  "timestamp": "ISO8601",
  "security": { "status": "...", "checks": [...] },
  "levels": {
    "L1": { "status": "...", "checks": [...] },
    "L2": { "status": "...", "checks": [...] },
    "L3": { "status": "...", "checks": [...] }
  },
  "duration_ms": 123
}
```

## Integration

Called by `scripts/run_harness.sh` after every code change.

```bash
# From project root
./scripts/run_harness.sh
```

Returns exit code 0 on PASS, 1 on FAIL.
