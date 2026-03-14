---
id: TASK-4
title: 'Add Postgres, SQLAlchemy, Alembic, and the baseline empty-schema migration'
status: Done
assignee:
  - '@codex'
created_date: '2026-03-12 01:37'
updated_date: '2026-03-14 14:39'
labels: []
milestone: m-0
dependencies:
  - TASK-2
documentation:
  - docs/architecture/architecture.md
  - docs/qna/data/schema and migrations.md
parent_task_id: M-0
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Establish the backend database baseline with SQLAlchemy wiring, Alembic configuration, and an initial empty-schema migration that can be applied repeatably in local and CI environments.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The backend can connect to PostgreSQL through the approved persistence baseline and migration configuration.
- [x] #2 An initial Alembic revision creates the empty application schema successfully and becomes the starting point for later domain tables.
- [x] #3 The migration workflow keeps schema evolution separate from normal application startup.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Update the backend persistence baseline in `apps/api/` by adding the required database dependencies and project assets for PostgreSQL + SQLAlchemy 2.x + Alembic, including `pyproject.toml`, `alembic.ini`, and the `migrations/` package structure expected by the architecture.
2. Replace the current placeholder database runtime in `apps/api/src/palio/db/` with minimal SQLAlchemy wiring that fits the approved modular-monolith boundary: a runtime engine/session factory for application use, a session-bound Unit of Work baseline, and composition-root integration through `apps/api/src/palio/app/bootstrap.py` without introducing automatic migrations on app startup.
3. Keep TASK-4 scoped to persistence infrastructure only by using narrow DB-specific configuration inputs for runtime and migration commands, while leaving the broader typed env-settings consolidation to TASK-5.
4. Add the initial Alembic revision as the migration baseline so `upgrade head` creates only the empty application schema and Alembic version tracking, establishing the starting point for all later domain-table revisions.
5. Validate the baseline with the narrowest honest checks for this task: keep the existing FastAPI smoke tests green, verify Alembic can run against a real PostgreSQL database without SQLite fallbacks, and leave the fuller Postgres-backed integration harness split/fixtures work to TASK-8.
6. Update every affected document in the same change so the persistence baseline, migration workflow, and local developer commands stay accurate. Expected touch points include `apps/api/README.md`, `README.md`, `docs/ops/local-dev.md`, and any architecture/Q&A text that would otherwise become stale.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Research completed before planning: reviewed Backlog workflow overview/task-execution guidance, TASK-4/TASK-2/TASK-5/TASK-8 context, `docs/architecture/architecture.md`, `docs/qna/data/schema and migrations.md`, `docs/qna/architecture/module boundaries.md`, `docs/qna/architecture/deployment and operations.md`, `docs/qna/architecture/consistency and projections.md`, `docs/testing/test-strategy.md`, `docs/ops/local-dev.md`, `docs/milestones.md`, backend README, `docs/domain/er-schema.md`, and the current `apps/api` scaffold.

Current scaffold findings: `apps/api/src/palio/db/runtime.py` and `unit_of_work.py` are placeholders only; `palio.app.bootstrap` already owns manual runtime assembly; `pyproject.toml` does not yet declare SQLAlchemy/Alembic/Postgres dependencies; no Alembic config or migrations directory exists yet.

Scope boundary confirmed from adjacent tasks: TASK-5 owns broad typed env-based settings/logging/ops endpoints, and TASK-8 owns the fuller real-Postgres test harness. TASK-4 should establish the persistence/migration baseline without absorbing those wider concerns.

`docs/domain/er-schema.md` confirms the future table inventory and implementation constraints (for example UUIDv7 generation stays in Python).

User clarification recorded on 2026-03-14: the dedicated Postgres application schema for the baseline migration should be named `palio_board`.

User clarification recorded on 2026-03-14: documentation and implementation should use the canonical backend app path `apps/api` rather than `apps/backend`.

Documentation inconsistency noted for later cleanup if TASK-4 changes docs: the root `README.md` still shows `apps/backend/` in the repository tree even though TASK-1/TASK-2 and the current repo use `apps/api`.

Implemented in the AGENTS-compliant worktree `../palio-trees/agent/task-4` on branch `tasks/task-4-postgres-sqlalchemy-alembic-baseline`.

Added the backend persistence baseline in `apps/api/`: SQLAlchemy 2.x runtime wiring, psycopg-backed Postgres URLs, Alembic config, and the first migration revision.

Recorded the user clarification that the fixed application schema is `palio_board` and updated shared docs/Q&A so later persistence tasks inherit the same schema name.

Created `REDLINING.md` because the repo instructions require tracked-change notes and the file was absent in this branch.

Validation completed: `uv run pytest`, `uv run python -m palio.shared.module_boundaries`, `uv run alembic upgrade head` against a disposable Docker `postgres:16` instance, a live runtime `SELECT 1` using `PALIO_DB_RUNTIME_URL`, and a second `alembic upgrade head` no-op rerun to confirm repeatability.

Did not add `.env.dev` or `.env.test` files. That would be inert in TASK-4 because the code reads plain environment variables only, while the broader env/settings workflow belongs to TASK-5 and TASK-8.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented the backend persistence baseline for `apps/api` by adding SQLAlchemy 2.x, Alembic, and psycopg to the Python project, then replacing the placeholder DB runtime with a minimal SQLAlchemy engine/session factory plus a session-bound `SqlAlchemyUnitOfWork`. The FastAPI composition root still boots without auto-connecting to Postgres, but runtime workflows can now open real ORM sessions when `PALIO_DB_RUNTIME_URL` is configured.

Added Alembic under `apps/api/alembic.ini` and `apps/api/migrations/`, with an initial revision that creates the dedicated application schema `palio_board`. Migration execution stays explicitly separate from normal backend startup and uses `PALIO_DB_MIGRATION_URL`, preserving the approved split between runtime and migration credentials.

Updated the affected docs and tracked-change notes so the repository now documents the fixed schema name, the `apps/api` backend path, the explicit migration command, and the current local DB configuration surface. This included `README.md`, `apps/api/README.md`, `docs/ops/local-dev.md`, `docs/domain/er-schema.md`, `docs/qna/data/schema and migrations.md`, and the new `REDLINING.md`.

Validation run from the worktree:
- `cd apps/api && uv run pytest`
- `cd apps/api && uv run python -m palio.shared.module_boundaries`
- `cd apps/api && PALIO_DB_MIGRATION_URL=postgresql+psycopg://... uv run alembic upgrade head` against a disposable Docker `postgres:16` container
- `cd apps/api && PALIO_DB_RUNTIME_URL=postgresql+psycopg://... uv run python -c "...SELECT 1..."`
- a second `alembic upgrade head` rerun against the same container to confirm the baseline is repeatable/no-op once applied

No `.env.dev` or `.env.test` files were added in this task; that remains intentionally deferred to the later env/settings and test-harness tasks.
<!-- SECTION:FINAL_SUMMARY:END -->
