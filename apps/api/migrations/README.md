# Alembic migrations

This directory owns database schema evolution for the api.

Runtime application startup must never apply migrations automatically.

Use `PALIO_DB_MIGRATION_URL` when running Alembic commands locally or in CI.
