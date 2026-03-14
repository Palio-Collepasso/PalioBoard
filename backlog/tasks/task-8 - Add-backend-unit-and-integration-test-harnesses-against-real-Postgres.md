---
id: TASK-8
title: Add backend unit and integration test harnesses against real Postgres
status: Done
assignee:
  - '@codex'
created_date: '2026-03-12 01:37'
updated_date: '2026-03-14 18:49'
labels: []
milestone: m-0
dependencies:
  - TASK-2
  - TASK-4
  - TASK-5
documentation:
  - docs/testing/test-strategy.md
  - docs/qna/architecture/deployment and operations.md
parent_task_id: M-0
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create the backend testing baseline with fast unit-test entrypoints and Postgres-backed integration-test wiring that applies real migrations and exercises the application skeleton honestly.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Backend tests are split into unit and Postgres-backed integration layers in line with the documented strategy.
- [x] #2 Integration tests run against a real local PostgreSQL database and apply real migrations rather than using SQLite substitutes.
- [x] #3 The test harness includes at least one smoke path for app startup or health endpoints and one smoke path for migration/application bootstrapping.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Restructure the backend pytest layout into explicit `unit` and `integration` layers under `apps/api/tests/`, moving the current smoke/config/boundary tests into the appropriate bucket and updating `apps/api/pyproject.toml` plus the top-level `Makefile` so the backend test entrypoint runs the split deliberately instead of one undifferentiated suite.
2. Add shared backend test support under `apps/api/tests/` for environment overrides, app/runtime construction, and reusable assertions so unit tests stay DB-free while integration tests opt into real Postgres wiring through a single documented harness.
3. Introduce a real-Postgres integration harness that targets a local PostgreSQL server, creates isolated test databases for the suite, applies the real Alembic migrations into those databases, and then feeds the resulting runtime/migration URLs into the backend without any SQLite fallback or fake DB layer.
4. Add the first Postgres-backed smoke coverage required by this task: one integration path that proves migration/bootstrap against a real database (for example asserting the migrated `palio_board` schema exists) and one integration path that proves the application/readiness surface works when pointed at the migrated Postgres runtime. Keep app-boot/config smoke coverage that does not need a live DB in the unit layer.
5. Update the affected documentation and repo guidance so the new backend harness is the documented truth: at minimum `apps/api/README.md`, `README.md`, `docs/ops/local-dev.md`, `docs/testing/test-strategy.md`, and `REDLINING.md` should explain the unit/integration split, the local Postgres prerequisite/configuration, and the intended validation commands (`pytest` layer commands plus `make test-backend`).
6. Validate the finished harness with the narrowest honest checks for this task: run the unit suite, run the Postgres-backed integration suite against a real local database with real migrations, and confirm the stable repo entrypoint (`make test-backend`) exercises the split successfully.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Research completed before planning: reviewed Backlog workflow overview/task-execution guidance, TASK-8 plus dependency task records (TASK-2, TASK-4, TASK-5), `apps/api/AGENTS.md`, `apps/api/README.md`, `docs/testing/test-strategy.md`, `docs/ops/local-dev.md`, `docs/qna/architecture/deployment and operations.md`, `docs/qna/data/schema and migrations.md`, `docs/architecture/architecture.md`, `docs/architecture/adr/ADR-0009-testing-and-quality-gates.md`, the top-level `README.md`, and the current backend runtime/migration/test files.

Current codebase findings: `apps/api/tests/` is still a single unsplit smoke suite (`test_app.py`, `test_db_runtime.py`, `test_settings.py`, `test_module_boundaries.py`, `test_openapi_export.py`); `make test-backend` still runs `cd apps/api && uv run pytest`; Alembic and runtime DB wiring already exist, and the baseline migration creates only the `palio_board` schema.

Local prerequisite check completed during planning: `uv` and `docker` are available in this worktree environment, so a real-local-Postgres integration harness is viable. No code changes started; waiting for explicit user approval before implementation.

Implemented the split backend harness under `apps/api/tests/unit/` and `apps/api/tests/integration/`, plus shared Postgres helpers under `apps/api/tests/support/postgres.py`. `make test-backend` now runs the two layers sequentially, and app-local `uv run pytest` also succeeds against the packaged split layout.

Integration tests now use a real local PostgreSQL database only: by default they start a disposable Docker `postgres:16-alpine` container, create isolated test databases, and apply the real Alembic migrations with `python -m alembic -x db_url=... upgrade head`. `PALIO_TEST_POSTGRES_URL` can point the suite at an existing local admin database instead.

Added the required smoke coverage: one integration test proves the migrated `palio_board` schema and Alembic revision exist in a real database, and one integration test proves FastAPI `/readyz`, `/healthz`, and `/version` behave correctly when the app runs against that migrated Postgres runtime.

Updated `apps/api/README.md`, `README.md`, `docs/ops/local-dev.md`, `docs/testing/test-strategy.md`, and `REDLINING.md` so the split harness, local Postgres behavior, and test env vars are documented.

During validation, the existing `palio.db` package export mismatch surfaced because `palio.db.__init__` already expected `APPLICATION_SCHEMA` and `RUNTIME_DATABASE_URL_ENV_VAR` from `palio.db.config`. Fixed that inconsistency in `apps/api/src/palio/db/config.py` so the test/runtime imports work consistently.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented TASK-8 by splitting the backend suite into `apps/api/tests/unit/` and `apps/api/tests/integration/`, updating `apps/api/pyproject.toml` and the top-level `Makefile` so the backend test entrypoint now runs fast unit checks separately from the real-Postgres integration layer.

Added a reusable Postgres integration harness in `apps/api/tests/support/postgres.py`. The integration suite either reuses an existing local Postgres admin database via `PALIO_TEST_POSTGRES_URL` or starts a disposable Docker `postgres:16-alpine` container, then creates isolated test databases and applies the real Alembic migrations before exercising the app.

Added the first honest smoke coverage at the correct layer: a migration/bootstrap test that asserts the real migrated `palio_board` schema and Alembic revision exist, and an app/readiness smoke test that verifies `/readyz`, `/healthz`, and `/version` against a migrated Postgres runtime. Updated the backend/local-dev/testing docs and `REDLINING.md` to match the new harness.

Validation run:
- `cd apps/api && uv run pytest tests/unit`
- `cd apps/api && uv run pytest tests/integration`
- `cd apps/api && uv run pytest`
- `env -u VIRTUAL_ENV make test-backend`
<!-- SECTION:FINAL_SUMMARY:END -->
