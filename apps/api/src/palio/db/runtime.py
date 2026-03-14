"""Database runtime assembly for SQLAlchemy-backed persistence."""

from dataclasses import dataclass

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from palio.db.config import APPLICATION_SCHEMA
from palio.db.unit_of_work import SqlAlchemyUnitOfWork


class DatabaseNotConfiguredError(RuntimeError):
    """Raised when DB helpers are used without a configured runtime URL."""


type SessionFactory = sessionmaker[Session]


@dataclass(frozen=True, slots=True)
class ReadinessCheck:
    """Represent the current backend readiness status."""

    is_ready: bool
    reason: str


@dataclass(frozen=True, slots=True)
class DatabaseRuntime:
    """Store shared SQLAlchemy runtime objects for the application.

    Attributes:
        dsn: Runtime SQLAlchemy URL for normal app access.
        schema: Fixed Postgres schema owned by the application.
        engine: Lazily-connecting SQLAlchemy engine when the runtime is configured.
        session_factory: Factory for request or use-case scoped ORM sessions.
    """

    dsn: str | None = None
    schema: str = APPLICATION_SCHEMA
    engine: Engine | None = None
    session_factory: SessionFactory | None = None

    @property
    def is_configured(self) -> bool:
        """Report whether the runtime can open DB sessions."""

        return self.engine is not None and self.session_factory is not None

    def create_session(self) -> Session:
        """Create one ORM session from the configured factory.

        Returns:
            A SQLAlchemy ORM session.

        Raises:
            DatabaseNotConfiguredError: When no runtime DB URL is configured.
        """

        if self.session_factory is None:
            raise DatabaseNotConfiguredError(
                "Database runtime is not configured. Set PALIO_DB_RUNTIME_URL "
                "before opening ORM sessions."
            )

        return self.session_factory()

    def create_unit_of_work(self) -> SqlAlchemyUnitOfWork:
        """Create one session-bound Unit of Work.

        Returns:
            A SQLAlchemy-backed Unit of Work.
        """

        return SqlAlchemyUnitOfWork(self.create_session)

    def check_readiness(self) -> ReadinessCheck:
        """Check whether the database runtime is ready for traffic.

        Returns:
            The current readiness result.
        """

        if not self.is_configured or self.engine is None:
            return ReadinessCheck(
                is_ready=False,
                reason="database_not_configured",
            )

        try:
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
        except Exception as exc:
            return ReadinessCheck(
                is_ready=False,
                reason=f"database_unavailable:{exc.__class__.__name__}",
            )

        return ReadinessCheck(is_ready=True, reason="ok")


def build_database_runtime(*, dsn: str | None = None) -> DatabaseRuntime:
    """Build the DB runtime without forcing a startup connection.

    Args:
        dsn: Optional explicit runtime DB URL override.

    Returns:
        A configured runtime when a runtime DB URL is available, otherwise an
        inert runtime descriptor that preserves the scaffold boot path.
    """

    if dsn is None:
        return DatabaseRuntime()

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
