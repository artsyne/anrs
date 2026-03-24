---
name: safety-rules
description: |
  Safety constraints to prevent dangerous actions. Read when:
  (1) About to execute potentially risky operations
  (2) Handling data or credentials
  (3) Accessing external systems
---

# Safety Rules

## Prohibited Actions (NEVER)

### Destructive Operations
```bash
rm -rf /
rm -rf *
DROP DATABASE
DELETE FROM users;  # Without WHERE
```

### Secret Exposure
```bash
echo $API_KEY
cat .env
git add .env
```

### Production Access
```bash
ssh production-server
kubectl exec -it prod-pod
psql production_database
```

### Force Operations
```bash
git push --force
git reset --hard
kubectl delete --force
```

## Restricted Actions (REQUIRES approval)

### Database
```sql
ALTER TABLE / DROP INDEX / TRUNCATE TABLE
UPDATE ... WHERE ...  # Must have specific WHERE
```

### System
```bash
chmod 777 / chown / systemctl restart
```

### Network
```bash
curl external-url / wget / npm install (public registry)
```

## Safe Operations (ALWAYS OK)

```bash
# Read-only
ls, cat, grep, find, git status/log/diff, kubectl get/describe

# Local development
go run/test, npm run dev, docker-compose up (local)

# Harness
./scripts/run_harness.sh, ./scripts/run_task.sh
```

## Data Protection

- NEVER log PII or credentials
- NEVER expose PII in error messages
- ALWAYS mask sensitive data
- ALWAYS use environment variables for secrets
- ALWAYS backup before destructive operations

## Incident Response

If safety rule violated: STOP → ASSESS → NOTIFY → CONTAIN → DOCUMENT

## Safety Checklist

Before risky operations:
- [ ] Is this reversible?
- [ ] Is there a backup?
- [ ] Tested in non-production?
- [ ] Approval documented?
- [ ] Rollback ready?
