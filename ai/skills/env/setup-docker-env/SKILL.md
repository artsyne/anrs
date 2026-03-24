# Skill: Setup Docker Environment

<!--
  🐳 SKILL: setup-docker-env
  
  Setup Docker development environment.
-->

---

## 🎯 Purpose

Create a consistent, reproducible development environment using Docker.

---

## 📥 Input

```yaml
services: list         # Required services
dev_tools: list        # Development tools needed
```

---

## 📤 Output

```yaml
dockerfile: file
docker_compose: file
env_ready: boolean
```

---

## 📋 Checklist

- [ ] Requirements gathered
- [ ] Dockerfile created
- [ ] docker-compose.yml created
- [ ] Environment tested
- [ ] Documentation updated

---

## 🔧 Execution

### Step 1: Analyze Requirements

```
Typical services:
- Application runtime
- Database
- Cache (Redis)
- Message queue
- Mock services
```

### Step 2: Create Dockerfile

```dockerfile
# Use specific version for reproducibility
FROM golang:1.21-alpine AS builder

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN go build -o main .

# Multi-stage for smaller image
FROM alpine:3.18
COPY --from=builder /app/main /main
CMD ["/main"]
```

### Step 3: Create docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=postgres://db:5432/app
    depends_on:
      - db
      - redis

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: app
      POSTGRES_PASSWORD: dev
    volumes:
      - db_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine

volumes:
  db_data:
```

### Step 4: Test Environment

```bash
# Start all services
docker-compose up -d

# Verify health
docker-compose ps

# Run tests
docker-compose exec app go test ./...

# View logs
docker-compose logs -f app
```

---

## 📝 Best Practices

1. **Use specific versions** — Not `latest`
2. **Multi-stage builds** — Smaller images
3. **Volume for data** — Persist between restarts
4. **Health checks** — Verify service health
5. **.dockerignore** — Exclude unnecessary files

---

## ⚠️ Constraints

- Pin all image versions
- Do not expose unnecessary ports
- Use secrets for sensitive data
- Test before committing

---

## 🔗 Related

- `ai/rules/safety.md` — Security practices
