# Backend

This directory is the canonical home for the FastAPI backend and backend test harness.

Current TASK-4 baseline:
- `pyproject.toml` with the FastAPI, SQLAlchemy, Alembic, psycopg, and pytest dependencies used by the repo `Makefile`
- `alembic.ini` plus `migrations/` with the baseline revision that creates the empty `palio_board` application schema
- `src/palio/app/` as the explicit composition root with placeholder admin, public, and realtime surfaces
- `src/palio/db/` for narrow runtime/migration DB configuration, SQLAlchemy runtime assembly, and the session-bound Unit of Work baseline
- `src/palio/shared/` and `src/palio/modules/` for cross-cutting technical primitives and the documented modular-monolith package layout
- `tests/` with narrow smoke coverage for app boot, boundary enforcement, and the DB runtime baseline

Current local commands from this directory:
- `uv run fastapi dev src/palio/app/main.py`
- `uv run pytest`
- `PALIO_DB_MIGRATION_URL=postgresql+psycopg://... uv run alembic upgrade head`
- `uv run python -m palio.shared.module_boundaries`

Still deferred to later tasks:
- real business workflows and API contracts
- domain tables beyond the empty-schema migration
- broader env-based settings, logging, and operational endpoints from TASK-5
- Postgres-backed integration coverage beyond the current smoke checks
