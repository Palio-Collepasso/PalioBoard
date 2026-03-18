"""Shared Unit of Work contract owned by application orchestration."""

from collections.abc import Callable
from typing import Protocol, Self

from sqlalchemy.orm import Session

type SessionFactory = Callable[[], Session]


class UnitOfWork(Protocol):
    """Session-bound transaction contract used by orchestrators."""

    session: Session | None

    def __enter__(self) -> Self:
        """Open and return the active unit of work."""
        ...

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        """Close the unit of work and handle rollback when needed."""
        ...

    def commit(self) -> None:
        """Persist the current transaction."""
        ...

    def rollback(self) -> None:
        """Discard the current transaction."""
        ...


class SqlAlchemyUnitOfWork(UnitOfWork):
    """Wrap one SQLAlchemy session in a Unit of Work boundary.

    Args:
        session_factory: Factory used to open one ORM session per workflow.
    """

    def __init__(self, session_factory: SessionFactory) -> None:
        """Store the session factory for later workflow-scoped sessions."""
        self._session_factory = session_factory
        self.session: Session | None = None

    def __enter__(self) -> Self:
        """Open a session at the start of the workflow."""
        self.session = self._session_factory()
        return self

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        """Rollback on errors and always close the session."""
        if self.session is None:
            return

        if exc_type is not None:
            self.session.rollback()

        self.session.close()
        self.session = None

    def commit(self) -> None:
        """Commit the current transaction."""
        self._require_session().commit()

    def rollback(self) -> None:
        """Rollback the current transaction."""
        self._require_session().rollback()

    def _require_session(self) -> Session:
        """Return the active session or fail fast when misused.

        Returns:
            The active SQLAlchemy session.

        Raises:
            RuntimeError: When the Unit of Work is used outside its context.
        """
        if self.session is None:
            raise RuntimeError(
                "UnitOfWork has no active session. Use it within a with block."
            )

        return self.session
