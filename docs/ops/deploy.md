# Deploy

## Purpose
Describe the release procedure for the current v1 deployment model: one production host, Docker Compose, one backend instance, same-origin proxy, and explicit migration step.

## Document boundary
This file owns **release steps, verification, and rollback**.
It does not own architecture rationale or generic incident policy.
- Architecture rationale lives in ADR-0008 and `docs/architecture/architecture.md`.
- Incident recovery playbooks live in `docs/ops/runbook.md`.

## Deployment model summary
- target: one production VPS/VM
- stack: Nginx + backend + database-dependent services via Docker Compose
- release style: manual deploy in a planned maintenance window
- migrations: explicit step before app start

## Required operator variables
Set these once for the environment and reuse them in the commands below:

```bash
export DEPLOY_HOST="<ssh-host>"
export APP_DIR="<deploy-directory-on-host>"
export COMPOSE_FILE="<compose-file-path>"
```

## Artifact locations
Document or keep stable references for:
- backend image or build ref used by the release
- Nginx image or build ref used by the release
- committed API contract: `docs/api/openapi.yaml`
- migration head expected by the release

## Preconditions
- [ ] merged change set identified
- [ ] required checks passed
- [ ] release ref identified
- [ ] migration risk reviewed
- [ ] rollback decision owner identified
- [ ] maintenance window confirmed when needed

## Standard release commands
### 1. Connect and update release input
```bash
ssh "$DEPLOY_HOST"
cd "$APP_DIR"
git rev-parse HEAD
```

### 2. Pull or prepare the release artifacts
```bash
docker compose -f "$COMPOSE_FILE" pull
```

### 3. Apply migrations explicitly
```bash
docker compose -f "$COMPOSE_FILE" run --rm backend alembic upgrade head
```

### 4. Restart the app stack
```bash
docker compose -f "$COMPOSE_FILE" up -d --force-recreate nginx backend
```

### 5. Verify the release locally on the host
```bash
curl -fsS http://127.0.0.1/healthz
curl -fsS http://127.0.0.1/readyz
curl -fsS http://127.0.0.1/version
curl -fsS http://127.0.0.1/api/public/health
curl -fsS http://127.0.0.1/realtime/health
```

## Post-deploy verification checklist
- [ ] `/healthz` responds successfully
- [ ] `/readyz` reports ready after migrations
- [ ] `/version` reports the expected build/release metadata
- [ ] same-origin shell and proxy routing still work
- [ ] `/api/admin/health` and `/api/public/health` behave as expected
- [ ] backend and Nginx logs show no new startup or routing errors
- [ ] any release-specific manual smoke checks passed

## Rollback decision tree
### Use application rollback only when all are true
- the failure is in the new app/proxy build
- migrations were backward-compatible
- the previous images are still available

### Use incident handling instead of simple rollback when any are true
- the migration was risky or not backward-compatible
- data was already transformed in a way the old app cannot read safely
- the issue is operational/environmental rather than release-code specific
- verification cannot tell whether rollback is safe

## Standard rollback commands
### Roll back application or proxy build
```bash
cd "$APP_DIR"
docker compose -f "$COMPOSE_FILE" up -d --force-recreate nginx backend
```

Follow with the same verification commands used after deploy.

### Inspect logs during rollback decision
```bash
docker compose -f "$COMPOSE_FILE" logs --tail=200 backend nginx
```

## Release scenarios
### Standard application-only deploy
Use when no schema change is required.
- pull new artifacts
- restart backend and Nginx
- run the verification checklist

### Deploy with backward-compatible migration
Use when the migration can run before app restart without breaking the previous version.
- run migration first
- restart app services
- verify readiness and public/admin health endpoints

### Deploy with risky migration
Use when the migration is not clearly backward-compatible or not safely reversible.
- treat as a planned maintenance event
- require explicit operator sign-off before app restart
- keep the rollback decision point separate from the app restart step
- if verification fails, switch to `docs/ops/runbook.md` instead of improvising

## Release record
Capture at least:
- deployed ref or tag
- operator
- date/time
- migration head applied
- verification result
- rollback decision if one was needed
