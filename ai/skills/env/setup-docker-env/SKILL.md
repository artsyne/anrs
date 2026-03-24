---
name: setup-docker-env
description: |
  Setup Docker development environment. Use when:
  (1) Need a consistent development environment
  (2) Project requires containerized services (db, cache, etc.)
  (3) Setting up local development infrastructure
---

# Setup Docker Environment

Create a consistent, reproducible development environment using Docker.

## Input

```yaml
services: list         # Required services
dev_tools: list        # Development tools needed
```

## Output

```yaml
dockerfile: file
docker_compose: file
env_ready: boolean
```

## Checklist

- [ ] Requirements gathered
- [ ] Dockerfile created
- [ ] docker-compose.yml created
- [ ] Environment tested

## Execution

### 1. Analyze Requirements

Typical services:
- Application runtime
- Database
- Cache (Redis)
- Message queue

### 2. Create Dockerfile

```dockerfile
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN go build -o main .

FROM alpine:3.18
COPY --from=builder /app/main /main
CMD ["/main"]
```

### 3. Create docker-compose.yml

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8080:8080"
    depends_on:
      - db
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: app
      POSTGRES_PASSWORD: dev
    volumes:
      - db_data:/var/lib/postgresql/data
volumes:
  db_data:
```

### 4. Test Environment

```bash
docker-compose up -d
docker-compose ps
docker-compose exec app go test ./...
```

## Best Practices

- Use specific versions, not `latest`
- Multi-stage builds for smaller images
- Volume for data persistence
- Health checks for service readiness

## Constraints

- Pin all image versions
- Do not expose unnecessary ports
- Use secrets for sensitive data

## Related

- `ai/rules/safety.md` — Security practices
