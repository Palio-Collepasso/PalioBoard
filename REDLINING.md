# Redlining

This file tracks material implementation-baseline changes that affect how the repository should be read or used.

Add new entries in reverse chronological order.

## 2026-03-14

### TASK-4 - Postgres, SQLAlchemy, Alembic baseline

- Added the backend persistence baseline under `apps/api/` with SQLAlchemy 2.x, Alembic, and psycopg dependencies.
- Added explicit DB URL separation: `PALIO_DB_RUNTIME_URL` for normal app access and `PALIO_DB_MIGRATION_URL` for schema changes.
- Added the first Alembic revision, which creates the empty application schema `palio_board`.
- Kept schema evolution separate from normal app startup; migrations run only through explicit Alembic commands.
- Corrected tracked documentation references so the canonical backend app path is `apps/api`, not `apps/backend`.
