"""Database primitives owned by the composition root."""

from palio.bootstrap.db.runtime import DatabaseRuntime, build_database_runtime
from palio.settings import (
    APPLICATION_SCHEMA,
    MIGRATION_DATABASE_URL_ENV_VAR,
    RUNTIME_DATABASE_URL_ENV_VAR,
)

__all__ = [
    "APPLICATION_SCHEMA",
    "MIGRATION_DATABASE_URL_ENV_VAR",
    "RUNTIME_DATABASE_URL_ENV_VAR",
    "DatabaseRuntime",
    "build_database_runtime",
]
