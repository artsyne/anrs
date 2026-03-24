---
name: coding-rules
description: |
  Language-specific coding standards. Read when:
  (1) Writing new code
  (2) Reviewing code quality
  (3) Need language-specific conventions
---

# Coding Rules

## General Principles

- Code should be self-documenting
- Use meaningful names (variables, functions)
- Keep functions small (< 50 lines)
- Follow existing project conventions
- Write testable code, avoid tight coupling

## Go

```go
// Good: Clear names, always check errors
func ValidateUserInput(input UserInput) error {
    result, err := doSomething()
    if err != nil {
        return fmt.Errorf("failed: %w", err)
    }
    return nil
}

// Good: Small, focused interfaces
type Reader interface {
    Read(p []byte) (n int, err error)
}
```

## Frontend (TypeScript/React)

```tsx
// Good: Single responsibility
const UserAvatar: React.FC<Props> = ({ user }) => (
    <img src={user.avatar} alt={user.name} />
);

// Good: Minimal state
const [isOpen, setIsOpen] = useState(false);
```

## SRE / Infrastructure

```yaml
# Good: Explicit, documented
database:
  host: localhost
  port: 5432
  max_connections: 100  # Based on load testing
```

## Dependencies

**Adding**: CHECK if needed → EVALUATE quality → DOCUMENT reason → PIN version
**Removing**: VERIFY no usage → RUN harness → REMOVE → COMMIT

## Testing

```go
// Good: Descriptive name, AAA pattern
func TestValidateUser_ReturnsError_WhenEmailInvalid(t *testing.T) {
    // Arrange
    input := createTestInput()
    // Act
    result := doSomething(input)
    // Assert
    assert.Equal(t, expected, result)
}
```

## Security

- NEVER hardcode secrets
- ALWAYS validate user input
- ALWAYS use parameterized queries
- NEVER log sensitive data
- ALWAYS use HTTPS in production
