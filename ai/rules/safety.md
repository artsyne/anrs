# Safety Rules

<!--
  🛡️ SAFETY CONSTRAINTS
  
  Rules to prevent dangerous or irreversible actions.
  These rules protect the system and users.
-->

---

## 🔴 Prohibited Actions

### 1. Destructive Operations

```bash
# ❌ NEVER execute these commands
rm -rf /
rm -rf *
DROP DATABASE
DELETE FROM users;  # Without WHERE clause
```

### 2. Secret Exposure

```bash
# ❌ NEVER output secrets
echo $API_KEY
cat .env
git add .env
```

### 3. Production Access

```bash
# ❌ NEVER directly access production
ssh production-server
kubectl exec -it prod-pod
psql production_database
```

### 4. Force Operations

```bash
# ❌ NEVER use force flags without explicit approval
git push --force
git reset --hard
kubectl delete --force
```

---

## 🟡 Restricted Actions

### 1. Database Operations

```sql
-- ⚠️ REQUIRES review before execution
ALTER TABLE ...
DROP INDEX ...
TRUNCATE TABLE ...
UPDATE ... WHERE ...  # Must have specific WHERE clause
```

### 2. System Configuration

```bash
# ⚠️ REQUIRES explicit approval
chmod 777 ...
chown ...
systemctl restart ...
```

### 3. Network Operations

```bash
# ⚠️ REQUIRES security review
curl external-url
wget ...
npm install (from public registry)
```

---

## ✅ Safe Operations

### 1. Read-Only

```bash
# ✅ Always safe
ls, cat, grep, find
git status, git log, git diff
kubectl get, kubectl describe
```

### 2. Local Development

```bash
# ✅ Safe in development
go run, go test
npm run dev
docker-compose up (local)
```

### 3. Harness Operations

```bash
# ✅ Safe - designed for this purpose
./scripts/run_harness.sh
./scripts/run_task.sh
```

---

## 🔒 Data Protection

### 1. PII (Personal Identifiable Information)

- **NEVER** log PII
- **NEVER** expose PII in error messages
- **ALWAYS** mask PII in outputs

### 2. Credentials

- **NEVER** commit credentials
- **NEVER** print credentials
- **ALWAYS** use environment variables

### 3. Backups

- **ALWAYS** backup before destructive operations
- **ALWAYS** verify backup integrity
- **ALWAYS** document recovery procedure

---

## 🚨 Incident Response

If a safety rule is violated:

```
1. STOP all operations immediately
2. ASSESS the impact
3. NOTIFY appropriate parties
4. CONTAIN the damage
5. DOCUMENT the incident
6. IMPLEMENT preventive measures
```

---

## 📋 Safety Checklist

Before any potentially risky operation:

- [ ] Is this operation reversible?
- [ ] Is there a backup?
- [ ] Has this been tested in non-production?
- [ ] Is explicit approval documented?
- [ ] Are rollback procedures ready?

---

## 🔗 Related

- `harness/evaluators/security_scan.py` — Automated security checks
- `ai/skills/core/rollback/` — Rollback procedures
