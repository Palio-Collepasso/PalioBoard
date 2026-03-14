"""Database-specific configuration helpers."""

from palio.settings import MIGRATION_DATABASE_URL_ENV_VAR


class DatabaseConfigurationError(RuntimeError):
    """Raised when required database configuration is missing."""


def require_migration_database_url(
    configured_url: str | None,
    *,
    explicit_url: str | None = None,
) -> str:
    """Resolve the Alembic migration DB URL.

    Args:
        configured_url: Migration DB URL resolved by the caller.
        explicit_url: Optional explicit migration DB URL override.

    Returns:
        The migration DB URL.

    Raises:
        DatabaseConfigurationError: When no migration DB URL is configured.
    """

    if explicit_url is not None:
        return explicit_url

    if configured_url is None:
        raise DatabaseConfigurationError(
            "Alembic requires a database URL. Set "
            f"{MIGRATION_DATABASE_URL_ENV_VAR} or pass -x db_url=..."
        )

    return configured_url
