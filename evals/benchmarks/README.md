---
name: evals-benchmarks
description: |
  Performance and accuracy benchmarks. Read when:
  (1) Measuring harness evaluation speed
  (2) Comparing AI model performance
  (3) Tracking regression over time
---

# Benchmarks

Performance and accuracy benchmarks for ANRS evaluation system.

## Benchmark Types

| Type | Measures | Target |
|------|----------|--------|
| Harness Speed | L1/L2/L3 execution time | < 30s total |
| Accuracy | False positive/negative rate | < 5% |
| Coverage | Code path coverage | > 80% |

## Running Benchmarks

```bash
# Run all benchmarks
./scripts/run_benchmarks.sh

# Run specific benchmark
python -m evals.benchmarks.harness_speed
```

## Benchmark Results Format

```json
{
  "benchmark": "harness_speed",
  "timestamp": "ISO8601",
  "results": {
    "L1_ms": 500,
    "L2_ms": 2000,
    "L3_ms": 5000,
    "total_ms": 7500
  }
}
```

## Current Benchmarks

*No benchmarks yet. Add benchmark scripts here.*
