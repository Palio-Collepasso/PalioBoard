# Redlining

This file tracks material implementation-baseline changes that affect how the repository should be read or used.

Add new entries in reverse chronological order.

## 2026-03-14

### TASK-6 - Docker Compose and same-origin Nginx local stack

- Added the first local-stack baseline under `infra/` with Docker Compose, backend and Nginx image definitions, and same-origin reverse-proxy configuration.
- `make up` and `make down` now drive `infra/compose/docker-compose.yml`, exposing the stack at `http://127.0.0.1:8080`.
- Nginx now serves the built Angular SPA and proxies `/healthz`, `/readyz`, `/version`, `/api/...`, and `/realtime/...` to the backend through one origin.
- Migrations remain explicit by design; the stack adds a one-shot `migrate` service instead of running Alembic during backend startup.
- Corrected the stale API-surface docs so they now match the implemented `/api/admin/...`, `/api/public/...`, and `/realtime/...` contract.
- Follow-up hardening switched the Nginx runtime stage from `nginx:1.27-alpine` to `nginx:1.29.4-alpine3.23-slim` after the image was flagged for severe vulnerability findings, while preserving the same stack behavior.

### TASK-5 - Runtime settings, JSON logging, and operational endpoints

- Added a typed backend settings layer in `apps/api/src/palio/settings.py` so runtime behavior now comes from explicit env vars rather than scattered direct lookups.
- Added Loguru-backed structured JSON HTTP request logging with propagated UUIDv7 request ids and disabled the default unstructured Uvicorn access log stream.
- Added `/healthz`, `/readyz`, and `/version` to the backend operational surface; readiness now reports whether the runtime DB is actually usable.
- Updated the backend smoke tests and committed OpenAPI artifact to cover the new settings/logging/endpoints baseline.

### TASK-4 - Postgres, SQLAlchemy, Alembic baseline

- Added the backend persistence baseline under `apps/api/` with SQLAlchemy 2.x, Alembic, and psycopg dependencies.
- Added explicit DB URL separation: `PALIO_DB_RUNTIME_URL` for normal app access and `PALIO_DB_MIGRATION_URL` for schema changes.
- Added the first Alembic revision, which creates the empty application schema `palio_board`.
- Kept schema evolution separate from normal app startup; migrations run only through explicit Alembic commands.
- Corrected tracked documentation references so the canonical backend app path is `apps/api`, not `apps/backend`.
