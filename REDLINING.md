# Redlining

This file tracks material implementation-baseline changes that affect how the repository should be read or used.

Add new entries in reverse chronological order.

## 2026-03-14

### TASK-8 - Backend unit and real-Postgres integration harness

- Split the backend pytest suite into `apps/api/tests/unit/` and `apps/api/tests/integration/`, and changed `make test-backend` to run the two layers sequentially.
- Added a Postgres-backed integration harness under `apps/api/tests/support/postgres.py` that applies the real Alembic migrations into isolated test databases.
- Backend integration smoke tests now verify both the migrated `palio_board` schema bootstrap and FastAPI readiness against a real local Postgres database.
- The integration suite can reuse an existing local Postgres server through `PALIO_TEST_POSTGRES_URL` or start a disposable Docker `postgres:16-alpine` container automatically.

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
