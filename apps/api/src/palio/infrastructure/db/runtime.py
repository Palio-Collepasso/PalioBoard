"""Database runtime primitives for SQLAlchemy-backed persistence."""

from dataclasses import dataclass

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from palio.settings import APPLICATION_SCHEMA

type SessionFactory = sessionmaker[Session]


@dataclass(frozen=True, slots=True)
class ReadinessCheck:
    """Represent the current API readiness status."""

    is_ready: bool
    reason: str


@dataclass(frozen=True, slots=True)
class DatabaseRuntime:
    """Store shared SQLAlchemy runtime objects for the application.

    Attributes:
        dsn: Runtime SQLAlchemy URL for normal app access.
        schema: Fixed Postgres schema owned by the application.
        engine: Lazily-connecting SQLAlchemy engine for the configured runtime.
        session_factory: Factory for request or use-case scoped ORM sessions.
    """

    dsn: str
    engine: Engine
    session_factory: SessionFactory
    schema: str = APPLICATION_SCHEMA

    def create_session(self) -> Session:
        """Create one ORM session from the configured factory.

        Returns:
            A SQLAlchemy ORM session.

        Raises:
            DatabaseNotConfiguredError: When no runtime DB URL is configured.
        """
        return self.session_factory()

    def check_readiness(self) -> ReadinessCheck:
        """Check whether the database runtime is ready for traffic.

        Returns:
            The current readiness result.
        """
        try:
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
        except Exception as exc:
            return ReadinessCheck(
                is_ready=False,
                reason=f"database_unavailable:{exc.__class__.__name__}",
            )

        return ReadinessCheck(is_ready=True, reason="ok")


def build_database_runtime(*, dsn: str) -> DatabaseRuntime:
    """Build the configured DB runtime without forcing a startup connection.

    Args:
        dsn: Runtime DB URL.

    Returns:
        A configured runtime descriptor.
    """
    engine = create_engine(
        dsn,
        pool_pre_ping=True,
    )
    session_factory = sessionmaker(
        bind=engine,
        class_=Session,
        autoflush=False,
        expire_on_commit=False,
    )
    return DatabaseRuntime(
        dsn=dsn,
        engine=engine,
        session_factory=session_factory,
    )
