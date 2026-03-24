---
name: backend-architecture
description: |
  Backend development guidelines. Read when:
  (1) Writing backend code
  (2) Designing APIs
  (3) Structuring Go services
---

# Backend Architecture

## Standard Structure

```
src/
├── cmd/server/main.go     # Entry point
├── internal/              # Private packages
│   ├── handler/           # HTTP handlers
│   ├── service/           # Business logic
│   ├── repository/        # Data access
│   └── model/             # Domain models
├── pkg/                   # Public packages
└── api/openapi.yaml       # API definitions
```

## Design Patterns

**Clean Architecture**:
```
Handlers (HTTP) → Services (Logic) → Repositories (Data) → Models (Domain)
```

**Dependency Injection**:
```go
type UserService struct { repo UserRepository }
func NewUserService(repo UserRepository) *UserService {
    return &UserService{repo: repo}
}
```

**Error Handling**:
```go
if err := repo.Save(user); err != nil {
    return fmt.Errorf("failed to save user: %w", err)
}
```

## API Design

**RESTful**:
```
GET    /users        # List
POST   /users        # Create
GET    /users/{id}   # Read
PUT    /users/{id}   # Update
DELETE /users/{id}   # Delete
```

**Response Format**:
```json
{"data": {}, "meta": {"request_id": "abc-123"}}
```

**Error Format**:
```json
{"error": {"code": "USER_NOT_FOUND", "message": "User with ID 123 not found"}}
```
