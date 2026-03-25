---
name: test-driven-dev
description: |
  Implement features using Test-Driven Development. Use when:
  (1) Building new features from scratch
  (2) Need to ensure test coverage from the start
  (3) Following RED-GREEN-REFACTOR cycle
---

# Test-Driven Development

Build features by writing tests first, then implementing code to pass them.

## Input

```yaml
feature: string        # Feature description
requirements: list     # Feature requirements
```

## Output

```yaml
tests_added: list
implementation_files: list
all_tests_pass: boolean
```

## Checklist

- [ ] Requirements understood
- [ ] Test cases identified
- [ ] Tests written (RED)
- [ ] Implementation done (GREEN)
- [ ] Code refactored (REFACTOR)
- [ ] All tests pass

## Execution

### Phase 1: RED (Write Failing Tests)

1. Identify test cases from requirements
2. Write test for first requirement
3. Run test — verify it FAILS
4. Repeat for each requirement

### Phase 2: GREEN (Make Tests Pass)

1. Write MINIMAL code to pass first test
2. Run tests — verify it PASSES
3. Repeat for each test
4. Do NOT over-engineer

### Phase 3: REFACTOR (Clean Up)

1. Review code for improvements
2. Remove duplication
3. Improve naming
4. Run tests after each change
5. All tests must still pass

## Test Structure

```go
func TestFeature_Scenario_ExpectedBehavior(t *testing.T) {
    // Arrange
    input := setup()
    
    // Act
    result := feature(input)
    
    // Assert
    assert.Equal(t, expected, result)
}
```

## Constraints

- ALWAYS write test first
- NEVER write more code than needed to pass
- ALWAYS refactor after green
- Tests must be independent

## Related

- `spec/rules/coding.md` — Coding standards
- `harness/evaluators/l2_dynamic_tests.py` — Test evaluator
