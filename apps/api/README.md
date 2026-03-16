# Backend

This directory is the canonical home for the FastAPI backend and backend test harness.

Current TASK-8 baseline:
- `pyproject.toml` with runtime dependencies for the FastAPI app plus a dev dependency group for tests, typing, formatting, and hook tooling used by the repo `Makefile`
- `alembic.ini` plus `migrations/` with the baseline revision that creates the empty `palio_board` application schema
- `src/palio/app/` as the explicit composition root with Loguru JSON request logging, UUIDv7 request-id propagation, and the operational `/healthz`, `/readyz`, and `/version` endpoints
- `src/palio/settings.py` for the typed env-based runtime settings used by the app/bootstrap and DB helpers
- `src/palio/db/` for the runtime/migration DB configuration, SQLAlchemy runtime assembly, readiness probing, and the session-bound Unit of Work baseline
- `src/palio/shared/` and `src/palio/modules/` for cross-cutting technical primitives and the documented modular-monolith package layout
- `tests/unit/` for fast backend smoke/configuration checks and `tests/integration/` for real-Postgres migration/readiness coverage
- `tests/support/postgres.py` for the Postgres-backed integration harness, which can reuse an existing local server or start a disposable Docker Postgres container using the same image/bootstrap settings as `infra/compose/docker-compose.yml`

Current local commands from this directory:
- `uv run --group dev pre-commit install --hook-type pre-commit --hook-type pre-push`
- `uv run --group dev ruff format src tests`
- `uv run --group dev ruff format --check src tests`
- `uv run --group dev ruff check src tests`
- `uv run --group dev pyright`
- `uv run fastapi dev src/palio/app/main.py`
- `uv run --group dev pytest`
- `uv run --group dev pytest tests/unit`
- `uv run --group dev pytest tests/integration`
- `PALIO_DB_MIGRATION_URL=postgresql+psycopg://... uv run alembic upgrade head`
- `uv run --group dev python -m palio.app.export_openapi ../../docs/api/openapi.yaml`
- `uv run python -m palio.shared.module_boundaries`

Contract workflow baseline from TASK-7:
- FastAPI owns the committed OpenAPI artifact at `docs/api/openapi.yaml`
- the export command runs from application code and does not require a running backend
- frontend TypeScript types are generated from that committed spec and are not committed

Runtime environment variables currently supported:
- `PALIO_ENV` sets the typed runtime environment (`development`, `test`, or `production`)
- `PALIO_LOG_LEVEL` controls JSON log verbosity
- `PALIO_REQUEST_ID_HEADER` overrides the inbound/outbound request-id header name (defaults to `X-Request-ID`)
- `PALIO_BUILD_VERSION` overrides the `/version` payload version string
- `PALIO_BUILD_COMMIT_SHA` adds commit/build metadata to `/version`
- `PALIO_DB_RUNTIME_URL` configures normal runtime DB access and readiness checks
- `PALIO_DB_MIGRATION_URL` configures Alembic/schema-change access
- `PALIO_TEST_POSTGRES_URL` optionally points the integration suite at an existing local Postgres admin database instead of starting a disposable container
- `PALIO_TEST_POSTGRES_IMAGE` optionally overrides the Docker image used when the integration suite starts its disposable local Postgres instance instead of the compose-backed default

Still deferred to later tasks:
- real business workflows and API contracts
- domain tables beyond the empty-schema migration
- deeper Postgres-backed workflow coverage beyond the current migration/readiness smoke checks
