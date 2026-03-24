# Skill: Incident Analysis

<!--
  🚨 SKILL: incident-analysis
  
  Analyze production incidents and create postmortems.
-->

---

## 🎯 Purpose

Systematically analyze incidents to prevent recurrence.

---

## 📥 Input

```yaml
incident_id: string    # Incident identifier
timeline: list         # Events timeline
impact: object         # Impact metrics
```

---

## 📤 Output

```yaml
postmortem: file
root_causes: list
action_items: list
```

---

## 📋 Checklist

- [ ] Timeline reconstructed
- [ ] Impact quantified
- [ ] Root causes identified
- [ ] Contributing factors noted
- [ ] Action items created
- [ ] Postmortem documented

---

## 🔧 Execution

### Step 1: Reconstruct Timeline

```markdown
## Timeline

| Time (UTC) | Event |
|------------|-------|
| 14:00 | Deploy started |
| 14:05 | Error rate increased |
| 14:10 | Alert triggered |
| 14:15 | Incident declared |
| 14:30 | Root cause identified |
| 14:35 | Rollback initiated |
| 14:40 | Service restored |
```

### Step 2: Quantify Impact

```markdown
## Impact

- Duration: 40 minutes
- Users affected: 10,000
- Requests failed: 50,000
- Revenue impact: $X
- SLA breach: Yes/No
```

### Step 3: Root Cause Analysis

```
Use 5 Whys:
1. Why did the service fail? → DB connection exhausted
2. Why were connections exhausted? → Connection leak
3. Why was there a leak? → Missing connection close
4. Why was it missing? → Not caught in review
5. Why not caught? → No static analysis for this
```

### Step 4: Create Action Items

```markdown
## Action Items

| Priority | Action | Owner | Due |
|----------|--------|-------|-----|
| P1 | Fix connection leak | @dev | Done |
| P1 | Add connection monitoring | @sre | 1 week |
| P2 | Add static analysis rule | @platform | 2 weeks |
```

---

## 📝 Postmortem Format

```markdown
# Incident Postmortem: {incident_id}

## Summary
{One paragraph summary}

## Impact
{Quantified impact}

## Timeline
{Detailed timeline}

## Root Cause
{5 Whys analysis}

## Contributing Factors
{What made this worse}

## Action Items
{Table of actions}

## Lessons Learned
{What we learned}
```

---

## ⚠️ Constraints

- Blameless analysis
- Focus on systems, not people
- Actionable items only
- Follow up on items

---

## 🔗 Related

- `ai/skills/sre/risk-analysis/` — Preventive analysis
