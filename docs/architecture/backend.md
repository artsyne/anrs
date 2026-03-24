# Backend Architecture

<!--
  ⚙️ BACKEND ARCHITECTURE
  
  Guidelines for backend development within AHES.
-->

---

## 🎯 Overview

Backend services follow a layered architecture pattern optimized for AI-driven development.

---

## 📐 Standard Structure

```
src/
├── cmd/                 # Entry points
│   └── server/
│       └── main.go
├── internal/            # Private packages
│   ├── handler/         # HTTP handlers
│   ├── service/         # Business logic
│   ├── repository/      # Data access
│   └── model/           # Domain models
├── pkg/                 # Public packages
└── api/                 # API definitions
    └── openapi.yaml
```

---

## 🔧 Design Patterns

### 1. Clean Architecture

```
┌─────────────────────────────────┐
│         Handlers (HTTP)         │
├─────────────────────────────────┤
│         Services (Logic)        │
├─────────────────────────────────┤
│       Repositories (Data)       │
├─────────────────────────────────┤
│         Models (Domain)         │
└─────────────────────────────────┘
```

### 2. Dependency Injection

```go
// Good: Interface-based dependencies
type UserService struct {
    repo UserRepository
}

func NewUserService(repo UserRepository) *UserService {
    return &UserService{repo: repo}
}
```

### 3. Error Handling

```go
// Wrap errors with context
if err := repo.Save(user); err != nil {
    return fmt.Errorf("failed to save user: %w", err)
}
```

---

## 🔌 API Design

### RESTful Conventions

```
GET    /users        # List
POST   /users        # Create
GET    /users/{id}   # Read
PUT    /users/{id}   # Update
DELETE /users/{id}   # Delete
```

### Response Format

```json
{
  "data": {},
  "meta": {
    "request_id": "abc-123"
  }
}
```

### Error Format

```json
{
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "User with ID 123 not found"
  }
}
```

---

## 🔗 Related

- `ai/rules/coding.md` — Go coding standards
- `docs/references/api-contracts.json` — API definitions
