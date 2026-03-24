---
name: incident-analysis
description: |
  Analyze production incidents and create postmortems. Use when:
  (1) A production incident has occurred
  (2) Need to perform root cause analysis
  (3) Creating a blameless postmortem document
---

# Incident Analysis

Systematically analyze incidents to prevent recurrence.

## Input

```yaml
incident_id: string    # Incident identifier
timeline: list         # Events timeline
impact: object         # Impact metrics
```

## Output

```yaml
postmortem: file
root_causes: list
action_items: list
```

## Checklist

- [ ] Timeline reconstructed
- [ ] Impact quantified
- [ ] Root causes identified
- [ ] Contributing factors noted
- [ ] Action items created
- [ ] Postmortem documented

## Execution

### 1. Reconstruct Timeline

| Time (UTC) | Event |
|------------|-------|
| 14:00 | Deploy started |
| 14:05 | Error rate increased |
| 14:10 | Alert triggered |
| 14:15 | Incident declared |
| 14:35 | Rollback initiated |
| 14:40 | Service restored |

### 2. Quantify Impact

- Duration: X minutes
- Users affected: X
- Requests failed: X
- Revenue impact: $X
- SLA breach: Yes/No

### 3. Root Cause Analysis (5 Whys)

1. Why did the service fail? → DB connection exhausted
2. Why were connections exhausted? → Connection leak
3. Why was there a leak? → Missing connection close
4. Why was it missing? → Not caught in review
5. Why not caught? → No static analysis for this

### 4. Create Action Items

| Priority | Action | Owner | Due |
|----------|--------|-------|-----|
| P1 | Fix connection leak | @dev | Done |
| P1 | Add monitoring | @sre | 1 week |
| P2 | Add static analysis | @platform | 2 weeks |

## Postmortem Format

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

## Action Items
{Table of actions}

## Lessons Learned
{What we learned}
```

## Constraints

- Blameless analysis
- Focus on systems, not people
- Actionable items only

## Related

- `ai/skills/sre/risk-analysis/` — Preventive analysis
