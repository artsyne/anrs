# RFC-NNNN: Title

- **RFC Number**: NNNN
- **Title**: Short descriptive title
- **Author**: Your Name (@github_handle)
- **Status**: Draft | Proposed | Accepted | Rejected | Implemented
- **Created**: YYYY-MM-DD
- **Updated**: YYYY-MM-DD

## Summary

One paragraph explanation of the proposal.

## Motivation

Why are we doing this? What problems does it solve? What use cases does it support?

### Problem Statement

Describe the current situation and its limitations.

### Goals

- Goal 1
- Goal 2

### Non-Goals

- What this RFC explicitly does NOT aim to solve

## Detailed Design

### Overview

High-level description of the proposed solution.

### Specification Changes

If this RFC modifies spec files, list them:

| File | Change Type | Description |
|------|-------------|-------------|
| `spec/state/state.schema.json` | Modify | Add new field `x` |

### New Concepts

If introducing new concepts, define them clearly:

**Concept Name**: Definition and purpose.

### API Changes

If CLI or API changes are involved:

```bash
# Before
anrs command --old-option

# After
anrs command --new-option
```

### Migration Path

How do existing users upgrade?

1. Step 1
2. Step 2

## Alternatives Considered

### Alternative 1

Description and why it was rejected.

### Alternative 2

Description and why it was rejected.

## Compatibility

### Backward Compatibility

- Is this change backward compatible?
- What breaks if not?

### Forward Compatibility

- Can older tools work with new spec versions?

## Security Considerations

Any security implications of this change.

## Implementation Plan

### Phase 1: Preparation

- [ ] Task 1
- [ ] Task 2

### Phase 2: Implementation

- [ ] Task 3
- [ ] Task 4

### Phase 3: Documentation

- [ ] Update docs
- [ ] Update examples

## Open Questions

1. Question that needs discussion?
2. Another unresolved issue?

## References

- Link to related issues
- Link to prior art
- Link to relevant documentation

---

## Appendix

### A. Full Schema Example

```json
{
  "example": "schema"
}
```

### B. Migration Script (if applicable)

```python
# Migration code example
```
