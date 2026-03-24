# Skill: Generate FMEA Report

<!--
  📊 SKILL: generate-fmea-report
  
  Generate Failure Mode and Effects Analysis report.
-->

---

## 🎯 Purpose

Systematically analyze potential failure modes and their effects.

---

## 📥 Input

```yaml
component: string      # System component to analyze
scope: string          # Analysis scope
```

---

## 📤 Output

```yaml
fmea_report: file      # Generated report
risk_items: list
recommendations: list
```

---

## 📋 Checklist

- [ ] Component identified
- [ ] Failure modes listed
- [ ] Effects analyzed
- [ ] Severity scored
- [ ] Mitigations proposed
- [ ] Report generated

---

## 🔧 Execution

### Step 1: Identify Failure Modes

```
For each component, ask:
- What can fail?
- How can it fail?
- When might it fail?
```

### Step 2: Analyze Effects

```
For each failure mode:
- What is the immediate effect?
- What is the system-wide effect?
- What is the user-facing effect?
```

### Step 3: Score Risk

```
Risk Priority Number (RPN) = Severity × Occurrence × Detection

Severity (1-10):    Impact of failure
Occurrence (1-10):  Likelihood of failure
Detection (1-10):   Difficulty detecting before impact
```

### Step 4: Propose Mitigations

```
For high RPN items:
- How to reduce severity?
- How to reduce occurrence?
- How to improve detection?
```

---

## 📝 Report Format

```markdown
# FMEA Report: {component}

## Summary
- Total failure modes: N
- High risk items: M
- Date: YYYY-MM-DD

## Failure Modes

| ID | Failure Mode | Effect | S | O | D | RPN | Mitigation |
|----|--------------|--------|---|---|---|-----|------------|
| 1  | DB timeout   | 503    | 8 | 3 | 4 | 96  | Add retry  |

## Recommendations

1. Implement circuit breaker
2. Add monitoring alerts
3. Increase timeout budget
```

---

## ⚠️ Constraints

- Focus on critical paths first
- Include detection mechanisms
- Propose actionable mitigations

---

## 🔗 Related

- `harness/evaluators/l3_stability_fmea.py` — FMEA evaluator
- `docs/architecture/system.md` — System architecture
