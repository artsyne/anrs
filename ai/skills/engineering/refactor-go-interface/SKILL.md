# Skill: Refactor Go Interface

<!--
  ♻️ SKILL: refactor-go-interface
  
  Safely refactor Go interfaces following best practices.
-->

---

## 🎯 Purpose

Refactor Go interfaces to be smaller, more focused, and easier to test.

---

## 📥 Input

```yaml
interface_name: string  # Interface to refactor
current_file: string    # Where interface is defined
```

---

## 📤 Output

```yaml
new_interfaces: list
updated_implementations: list
tests_updated: boolean
```

---

## 📋 Checklist

- [ ] Current interface analyzed
- [ ] New interfaces designed
- [ ] Implementations updated
- [ ] Tests updated
- [ ] No regressions

---

## 🔧 Execution

### Step 1: Analyze Current Interface

```go
// Before: Large interface
type Repository interface {
    Create(item Item) error
    Read(id string) (Item, error)
    Update(item Item) error
    Delete(id string) error
    List() ([]Item, error)
    Search(query string) ([]Item, error)
}
```

### Step 2: Apply Interface Segregation

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

type Deleter interface {
    Delete(id string) error
}

// Compose when needed
type ReadWriter interface {
    Reader
    Creator
    Updater
}
```

### Step 3: Update Implementations

```go
// Implementation satisfies all small interfaces
type itemRepository struct { ... }

func (r *itemRepository) Create(item Item) error { ... }
func (r *itemRepository) Read(id string) (Item, error) { ... }
// ... etc
```

### Step 4: Update Consumers

```go
// Before: Required full interface
func Process(repo Repository) { ... }

// After: Require only what's needed
func Process(reader Reader) { ... }
```

---

## 🔑 Go Interface Guidelines

1. **Accept interfaces, return structs**
2. **Keep interfaces small** (1-3 methods)
3. **Define interfaces where used**, not implemented
4. **Use composition** for larger interfaces

---

## ⚠️ Constraints

- Test BEFORE and AFTER
- Change ONE interface at a time
- Update ALL consumers
- Preserve backward compatibility if needed

---

## 🔗 Related

- `ai/rules/coding.md` — Go coding standards
- `ai/orchestrator/strategies/refactor.md` — Refactor strategy
