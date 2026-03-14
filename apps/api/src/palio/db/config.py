"""Database-specific configuration helpers."""

import os

APPLICATION_SCHEMA = "palio_board"
RUNTIME_DATABASE_URL_ENV_VAR = "PALIO_DB_RUNTIME_URL"
MIGRATION_DATABASE_URL_ENV_VAR = "PALIO_DB_MIGRATION_URL"


class DatabaseConfigurationError(RuntimeError):
    """Raised when required database configuration is missing."""


def get_runtime_database_url(*, explicit_url: str | None = None) -> str | None:
    """Resolve the runtime DB URL.

    Args:
        explicit_url: Optional explicit runtime DB URL override.

    Returns:
        The runtime DB URL when configured.
    """

    if explicit_url is not None:
        return explicit_url

    return os.getenv(RUNTIME_DATABASE_URL_ENV_VAR)


def get_migration_database_url(*, explicit_url: str | None = None) -> str:
    """Resolve the Alembic migration DB URL.

    Args:
        explicit_url: Optional explicit migration DB URL override.

    Returns:
        The migration DB URL.

    Raises:
        DatabaseConfigurationError: When no migration DB URL is configured.
    """

    if explicit_url is not None:
        return explicit_url

    configured_url = os.getenv(MIGRATION_DATABASE_URL_ENV_VAR)
    if configured_url is None:
        raise DatabaseConfigurationError(
            "Alembic requires a database URL. Set "
            f"{MIGRATION_DATABASE_URL_ENV_VAR} or pass -x db_url=..."
        )

    return configured_url
