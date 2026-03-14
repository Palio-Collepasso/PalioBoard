# Backend

This directory is the canonical home for the FastAPI backend and backend test harness.

Current TASK-2 scaffold:
- `pyproject.toml` with the minimal FastAPI and pytest setup used by the repo `Makefile`
- `src/palio/app/` as the explicit composition root with placeholder admin, public, and realtime surfaces
- `src/palio/db/` and `src/palio/shared/` for cross-cutting technical primitives needed by the scaffold
- `src/palio/modules/` with the documented modular-monolith package layout and one public `facade.py` per module
- `tests/` with narrow smoke coverage for app boot and boundary enforcement

Current local commands from this directory:
- `uv run fastapi dev src/palio/app/main.py`
- `uv run pytest`
- `uv run python -m palio.app.export_openapi ../../docs/api/openapi.yaml`
- `uv run python -m palio.shared.module_boundaries`

Contract workflow baseline from TASK-7:
- FastAPI owns the committed OpenAPI artifact at `docs/api/openapi.yaml`
- the export command runs from application code and does not require a running backend
- frontend TypeScript types are generated from that committed spec and are not committed

Still deferred to later tasks:
- Alembic configuration and migrations
- SQLAlchemy persistence wiring
- real business workflows and API contracts
- Postgres-backed integration coverage beyond the scaffold smoke tests
