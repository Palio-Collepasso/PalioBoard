# Runbook

## Purpose
Keep executable operator playbooks for issues that can actually happen with the current deployment and local support model.

## Document boundary
This file owns **actionable troubleshooting and recovery steps**.
It does not own architecture rationale, release sequence, or future candidate ideas.
- Deploy procedure lives in `docs/ops/deploy.md`.
- Architecture rationale lives in ADR-0008 and `docs/architecture/architecture.md`.

## Quick links
- health: `GET /healthz`
- readiness: `GET /readyz`
- version: `GET /version`
- public health: `GET /api/public/health`
- realtime health: `GET /realtime/health`
- host-side logs: `docker compose -f "$COMPOSE_FILE" logs --tail=200 backend nginx`

## Ownership
- first operator: deployment owner on duty
- escalation owner: maintainer responsible for the affected area
- docs to cross-check: `docs/ops/deploy.md`, `docs/api/error-contract.md`, `docs/testing/critical-e2e-flows.md`

## Incident index
| ID | Scenario | Use when |
|---|---|---|
| `RB-001` | readiness or health checks fail after a stack change | app boots partially, proxy routing breaks, or health endpoints fail |
| `RB-002` | migration step fails or was skipped | schema and runtime are out of sync or startup blocks on migration issues |

## `RB-001` — Readiness or health checks fail after a stack change
- **Last reviewed:** 2026-03-18
- **Use when:** `/healthz`, `/readyz`, same-origin shell routing, or health proxy paths fail right after a deploy or stack change.

### Immediate checks
```bash
curl -fsS http://127.0.0.1/healthz
curl -fsS http://127.0.0.1/readyz
curl -fsS http://127.0.0.1/version
docker compose -f "$COMPOSE_FILE" ps
docker compose -f "$COMPOSE_FILE" logs --tail=200 backend nginx
```

### Likely causes
- app failed to start after a code/config change
- proxy route split is broken
- env vars or secrets are missing
- migrations were not applied or the DB is unreachable

### Recovery steps
1. confirm whether the issue is app startup, proxy routing, or DB readiness
2. if the app build is bad and migrations are backward-compatible, follow the rollback path in `docs/ops/deploy.md`
3. if the issue is configuration or environment-only, correct the env/config and restart the affected services
4. re-run the health checks and public/realtime health endpoints

### Verification after recovery
```bash
curl -fsS http://127.0.0.1/healthz
curl -fsS http://127.0.0.1/readyz
curl -fsS http://127.0.0.1/api/public/health
curl -fsS http://127.0.0.1/realtime/health
```

### Escalate when
- readiness stays unhealthy after configuration correction
- rollback is unsafe because of migration risk
- logs show a data or schema mismatch rather than a simple startup failure

## `RB-002` — Explicit migration step fails or was skipped
- **Last reviewed:** 2026-03-18
- **Use when:** the explicit migration step errors, the backend expects a newer schema than the database has, or startup fails because migrations were skipped.

### Immediate checks
```bash
docker compose -f "$COMPOSE_FILE" run --rm backend alembic current
docker compose -f "$COMPOSE_FILE" run --rm backend alembic heads
docker compose -f "$COMPOSE_FILE" logs --tail=200 backend
```

### Likely causes
- migration script error
- deployment skipped the explicit migration step
- runtime code expects a schema not yet applied
- DB connection/config values are wrong on the target host

### Recovery steps
1. stop treating the deploy as successful until schema and app agree
2. identify whether the migration can be re-run safely
3. if the migration was skipped, run it explicitly and then restart the app services
4. if the migration itself is broken, switch to rollback/incident decision-making rather than forcing forward blindly
5. after recovery, re-run readiness and key health checks

### Verification after recovery
```bash
docker compose -f "$COMPOSE_FILE" run --rm backend alembic current
curl -fsS http://127.0.0.1/readyz
curl -fsS http://127.0.0.1/api/public/health
```

### Escalate when
- current/head cannot be reconciled safely
- the migration is destructive or not backward-compatible
- app startup still fails after schema state is corrected

## Incident notes template
When an issue required operator action, record:
- date/time
- operator
- scenario ID
- observed symptoms
- commands run
- recovery result
- follow-up docs or code changes needed
