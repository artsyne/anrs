---
name: api-contracts
description: |
  API endpoint definitions and contracts. Read when:
  (1) Implementing REST API endpoints
  (2) Designing request/response formats
  (3) Understanding error code conventions
---

# API Contracts

Reference for API endpoint definitions. See `api-contracts.json` for machine-readable format.

## Endpoints

### Health Check
```
GET /health
Response: { status, version, uptime_seconds }
```

### Tasks API
```
GET    /api/tasks      → List all tasks
POST   /api/tasks      → Create task (body: description, priority)
GET    /api/tasks/{id} → Get single task
```

### Harness API
```
POST /api/harness/run
Request:  { level: "L1|L2|L3" }
Response: { result: "PASS|FAIL", report_url }
```

## Response Format

**Success:**
```json
{
  "data": { ... },
  "meta": { "request_id": "abc-123" }
}
```

**Error:**
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message"
  }
}
```

## Error Codes

| Code | Meaning |
|------|---------|
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 422 | Validation Error |
| 500 | Internal Server Error |
