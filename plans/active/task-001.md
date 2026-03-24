# Task: task-001 (Example)

<!--
  📋 EXAMPLE TASK
  
  This is a sample task to demonstrate the plan format.
-->

---

## Objective

Implement a basic "Hello World" endpoint for the demo.

---

## Requirements

- Add GET /hello endpoint
- Return JSON response with message
- Include request timestamp
- Add unit test

---

## Steps

1. [ ] Create handler function in `src/handler/hello.go`
2. [ ] Register route in `src/router.go`
3. [ ] Write unit test in `src/handler/hello_test.go`
4. [ ] Run harness to verify

---

## Acceptance Criteria

- [ ] GET /hello returns 200 status
- [ ] Response includes "message" field
- [ ] Response includes "timestamp" field
- [ ] Unit test passes
- [ ] Harness L1 and L2 pass

---

## Estimated Effort

30 minutes

---

## Notes

This is a demo task to verify the AHES framework is working correctly.
