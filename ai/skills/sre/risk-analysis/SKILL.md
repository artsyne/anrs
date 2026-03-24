# Skill: Risk Analysis

<!--
  📊 SKILL: risk-analysis
  
  AI-driven risk analysis for code changes.
  Evaluates Severity, Occurrence, Detection to calculate risk score.
-->

---

## Purpose

Analyze potential risks in code changes before commit. This is an AI-native approach where the AI agent performs the analysis using its understanding of code semantics.

---

## Input

```yaml
changed_files: list    # Files modified in current task
task_context: string   # What the task is trying to accomplish
```

---

## Output

```yaml
risk_report: object
  overall_score: high | medium | low
  items: list
  recommendations: list
```

---

## Checklist

- [ ] List all changed files
- [ ] For each file, assess Severity
- [ ] For each file, assess Occurrence likelihood
- [ ] For each file, assess Detection difficulty
- [ ] Calculate overall risk score
- [ ] Provide mitigation recommendations
- [ ] Output structured report

---

## Analysis Framework

### Severity (S) — Impact if this code fails

Ask for each changed file:

```
□ Is this in a critical path? (auth, payment, data persistence)
□ Does it mutate data? (write operations > read operations)
□ Does it interact with external systems? (APIs, databases)
□ Are there security implications? (input validation, auth checks)

Score:
  - 1-3: Low impact (UI, logging, comments)
  - 4-6: Medium impact (business logic, validation)
  - 7-10: High impact (auth, payment, data, security)
```

### Occurrence (O) — Likelihood of failure

Check these indicators:

```
□ Code complexity: Is the logic complex or simple?
□ Git history: Has this file had bugs before? (check git log)
□ Dependencies: How many other modules depend on this?
□ Edge cases: Are there obvious edge cases not handled?

Score:
  - 1-3: Low likelihood (simple, well-tested patterns)
  - 4-6: Medium likelihood (moderate complexity)
  - 7-10: High likelihood (complex, many edge cases)
```

### Detection (D) — How hard to detect failure

Check these indicators:

```
□ Test coverage: Are there tests for this code?
□ Error handling: Does code handle errors gracefully?
□ Logging: Are failures logged for observability?
□ Assertions: Are invariants checked?

Score:
  - 1-3: Easy to detect (good tests, logging)
  - 4-6: Moderate detection difficulty
  - 7-10: Hard to detect (no tests, silent failures)
```

---

## Risk Score Calculation

```
Risk Priority Number (RPN) = S × O × D

Classification:
  - RPN < 50:  LOW risk    → Proceed with normal review
  - RPN 50-100: MEDIUM risk → Add extra tests, review carefully
  - RPN > 100: HIGH risk   → Require human review before merge
```

---

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
        "concerns": ["Handles user authentication", "Password validation"],
        "mitigation": "Add integration tests for edge cases"
      }
    ],
    "recommendations": [
      "Add test coverage for login failure scenarios",
      "Ensure rate limiting is in place"
    ]
  }
}
```

---

## Integration with Harness

This skill is called by L3 evaluator:

```
harness/evaluators/l3_stability_fmea.py
  └─▶ AI executes risk-analysis skill
      └─▶ Output saved to harness/reports/risk-analysis.json
```

---

## Constraints

- Focus on changed files only (not entire codebase)
- Be specific about concerns (not generic warnings)
- Provide actionable recommendations
- Do not block low-risk changes unnecessarily

---

## Related

- `harness/evaluators/l3_stability_fmea.py` — L3 evaluator
- `ai/skills/core/reflection/SKILL.md` — Post-failure analysis
