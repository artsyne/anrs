# Coding Rules

<!--
  📝 CODING STANDARDS
  
  Language-specific and general coding conventions.
  These rules ensure code quality and consistency.
-->

---

## 🎯 General Principles

### 1. Readability

- Code should be self-documenting
- Use meaningful names for variables and functions
- Keep functions small and focused (< 50 lines)

### 2. Consistency

- Follow existing project conventions
- Use consistent naming patterns
- Maintain consistent file structure

### 3. Testability

- Write testable code
- Avoid tight coupling
- Use dependency injection where appropriate

---

## 🐹 Go (Golang)

### Naming

```go
// ✅ Good: Clear, descriptive names
func ValidateUserInput(input UserInput) error { }

// ❌ Bad: Abbreviated, unclear
func ValUsrIn(i UI) error { }
```

### Error Handling

```go
// ✅ Good: Always check errors
result, err := doSomething()
if err != nil {
    return fmt.Errorf("failed to do something: %w", err)
}

// ❌ Bad: Ignoring errors
result, _ := doSomething()
```

### Interfaces

```go
// ✅ Good: Small, focused interfaces
type Reader interface {
    Read(p []byte) (n int, err error)
}

// ❌ Bad: Large, monolithic interfaces
type DoEverything interface {
    Read() / Write() / Delete() / Update() / ...
}
```

---

## 🌐 Frontend (TypeScript/React)

### Component Structure

```tsx
// ✅ Good: Single responsibility
const UserAvatar: React.FC<Props> = ({ user }) => {
  return <img src={user.avatar} alt={user.name} />;
};

// ❌ Bad: Too many responsibilities
const UserEverything: React.FC = () => {
  // Handles avatar, name, bio, settings, notifications...
};
```

### State Management

```tsx
// ✅ Good: Minimal state
const [isOpen, setIsOpen] = useState(false);

// ❌ Bad: Derived state stored as state
const [isOpen, setIsOpen] = useState(false);
const [isClosed, setIsClosed] = useState(true); // Redundant!
```

---

## 🛠 SRE / Infrastructure

### Configuration

```yaml
# ✅ Good: Explicit, documented
database:
  host: localhost
  port: 5432
  max_connections: 100  # Based on load testing results

# ❌ Bad: Magic numbers, no context
db:
  h: localhost
  p: 5432
  mc: 100
```

### Monitoring

```yaml
# ✅ Good: SLO-driven alerts
alerts:
  - name: high_error_rate
    condition: error_rate > 1%
    severity: critical
    slo_reference: "SLO-001"
```

---

## 📦 Dependencies

### Adding Dependencies

1. **CHECK** if functionality can be achieved without new dependency
2. **EVALUATE** dependency quality (stars, maintenance, security)
3. **DOCUMENT** why dependency is needed
4. **PIN** version for reproducibility

### Removing Dependencies

1. **VERIFY** no code depends on it
2. **RUN** harness to confirm
3. **REMOVE** from dependency file
4. **COMMIT** atomically

---

## 🧪 Testing

### Test Naming

```go
// ✅ Good: Describes behavior
func TestValidateUser_ReturnsError_WhenEmailInvalid(t *testing.T)

// ❌ Bad: Generic name
func TestValidate(t *testing.T)
```

### Test Structure

```go
// ✅ Good: Arrange-Act-Assert
func TestSomething(t *testing.T) {
    // Arrange
    input := createTestInput()
    
    // Act
    result := doSomething(input)
    
    // Assert
    assert.Equal(t, expected, result)
}
```

---

## 🔒 Security

1. **NEVER** hardcode secrets
2. **ALWAYS** validate user input
3. **ALWAYS** use parameterized queries
4. **NEVER** log sensitive data
5. **ALWAYS** use HTTPS in production
