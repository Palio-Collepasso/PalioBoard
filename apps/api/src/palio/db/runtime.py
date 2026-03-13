"""Database runtime placeholders for later SQLAlchemy wiring."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DatabaseRuntime:
    """Minimal database runtime descriptor for the scaffold."""

    dsn: str | None = None


def build_database_runtime() -> DatabaseRuntime:
    return DatabaseRuntime()
