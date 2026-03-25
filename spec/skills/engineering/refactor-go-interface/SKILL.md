---
name: refactor-go-interface
description: |
  Safely refactor Go interfaces following best practices. Use when:
  (1) Interface has too many methods (>3)
  (2) Need to apply Interface Segregation Principle
  (3) Refactoring Go code for better testability
---

# Refactor Go Interface

Refactor Go interfaces to be smaller, more focused, and easier to test.

## Input

```yaml
interface_name: string  # Interface to refactor
current_file: string    # Where interface is defined
```

## Output

```yaml
new_interfaces: list
updated_implementations: list
tests_updated: boolean
```

## Checklist

- [ ] Current interface analyzed
- [ ] New interfaces designed
- [ ] Implementations updated
- [ ] Tests updated
- [ ] No regressions

## Execution

### 1. Analyze Current Interface

```go
// Before: Large interface
type Repository interface {
    Create(item Item) error
    Read(id string) (Item, error)
    Update(item Item) error
    Delete(id string) error
    List() ([]Item, error)
}
```

### 2. Apply Interface Segregation

```go
// After: Small, focused interfaces
type Creator interface {
    Create(item Item) error
}

type Reader interface {
    Read(id string) (Item, error)
}

type Updater interface {
    Update(item Item) error
}

// Compose when needed
type ReadWriter interface {
    Reader
    Creator
    Updater
}
```

### 3. Update Consumers

```go
// Before: Required full interface
func Process(repo Repository) { ... }

// After: Require only what's needed
func Process(reader Reader) { ... }
```

## Go Interface Guidelines

- Accept interfaces, return structs
- Keep interfaces small (1-3 methods)
- Define interfaces where used, not implemented
- Use composition for larger interfaces

## Constraints

- Test BEFORE and AFTER
- Change ONE interface at a time
- Update ALL consumers
- Preserve backward compatibility if needed

## Related

- `spec/rules/coding.md` — Go coding standards
