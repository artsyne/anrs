---
name: core-beliefs
description: |
  ANRS foundational principles. Read when:
  (1) Understanding ANRS philosophy
  (2) Making architectural decisions
  (3) Evaluating trade-offs
---

# Core Beliefs

## Primary Beliefs

**Determinism Over Creativity**: Same input → Same output. No random exploration. Follow protocols exactly.

**Transactional Safety**: Every change must be atomic and reversible. Code + State must sync. No partial commits.

**Verification Before Trust**: Never trust AI output without verification. Always run harness. Fail fast, fix fast.

**Human Oversight**: AI assists, humans decide. Critical decisions need approval. Escalate when uncertain.

## Design Principles

```
Simplicity > Cleverness
Stability > Features
Correctness > Performance
```

## Safety Axioms

1. Never trust user input → Validate everything
2. Never expose secrets → Use environment variables
3. Never skip tests → Harness is mandatory
4. Never force push → History is sacred
5. Never bypass review → Code review catches mistakes

## Engineering Standards

```yaml
code_quality:
  functions: < 50 lines
  complexity: < 10
  coverage: > 80%
  lint_errors: 0

reliability:
  availability: > 99.9%
  latency_p99: < 200ms
  error_rate: < 0.1%
```

## Why ANRS

Traditional AI assistants: unpredictable, unverified, no rollback.
ANRS: AI as **constrained executor**, not autonomous agent.
