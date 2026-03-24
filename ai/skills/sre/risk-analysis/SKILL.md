---
name: risk-analysis
description: |
  AI-driven risk analysis for code changes. Use when:
  (1) Before committing significant code changes
  (2) L3 stability evaluation needs risk assessment
  (3) Need to evaluate Severity, Occurrence, Detection scores
---

# Risk Analysis

Analyze potential risks in code changes before commit. This is an AI-native approach where the AI agent performs the analysis using its understanding of code semantics.

## Input

```yaml
changed_files: list    # Files modified in current task
task_context: string   # What the task is trying to accomplish
```

## Output

```yaml
risk_report: object
  overall_score: high | medium | low
  items: list
  recommendations: list
```

## Checklist

- [ ] List all changed files
- [ ] Assess Severity for each file
- [ ] Assess Occurrence likelihood
- [ ] Assess Detection difficulty
- [ ] Calculate overall risk score
- [ ] Provide mitigation recommendations

## Analysis Framework

### Severity (S) — Impact if this code fails

Questions:
- Is this in a critical path? (auth, payment, data persistence)
- Does it mutate data? (write > read)
- Does it interact with external systems?
- Are there security implications?

Score: 1-3 (Low), 4-6 (Medium), 7-10 (High)

### Occurrence (O) — Likelihood of failure

Indicators:
- Code complexity
- Git history (has this file had bugs before?)
- Dependencies count
- Unhandled edge cases

Score: 1-3 (Low), 4-6 (Medium), 7-10 (High)

### Detection (D) — How hard to detect failure

Indicators:
- Test coverage
- Error handling quality
- Logging/observability
- Assertions/invariants

Score: 1-3 (Easy), 4-6 (Moderate), 7-10 (Hard)

## Risk Score Calculation

```
Risk Priority Number (RPN) = S × O × D

Classification:
  - RPN < 50:  LOW    → Proceed with normal review
  - RPN 50-100: MEDIUM → Add extra tests, review carefully
  - RPN > 100: HIGH   → Require human review before merge
```

## Output Format

```json
{
  "risk_report": {
    "overall_score": "medium",
    "total_rpn": 72,
    "items": [
      {
        "file": "src/auth/login.py",
        "severity": 8,
        "occurrence": 3,
        "detection": 3,
        "rpn": 72,
        "concerns": ["Handles authentication"],
        "mitigation": "Add integration tests"
      }
    ],
    "recommendations": [
      "Add test coverage for login failures"
    ]
  }
}
```

## Constraints

- Focus on changed files only
- Be specific about concerns (not generic warnings)
- Provide actionable recommendations
- Do not block low-risk changes unnecessarily

## Related

- `harness/evaluators/l3_stability.py` — L3 evaluator
- `ai/skills/core/reflection/SKILL.md` — Post-failure analysis
