---
name: task-001
description: |
  Example task for demo. Read when:
  (1) Understanding plan format
  (2) Learning task structure
---

# Task: task-001 (Example)

## Objective

Implement a basic "Hello World" endpoint for the demo.

## Requirements

- GET /hello endpoint
- JSON response with message
- Include request timestamp
- Unit test

## Steps

1. [ ] Create handler: `src/handler/hello.go`
2. [ ] Register route: `src/router.go`
3. [ ] Write test: `src/handler/hello_test.go`
4. [ ] Run harness

## Acceptance Criteria

- [ ] GET /hello returns 200
- [ ] Response has "message" field
- [ ] Response has "timestamp" field
- [ ] Unit test passes
- [ ] Harness L1/L2 pass

**Effort**: 30 minutes
