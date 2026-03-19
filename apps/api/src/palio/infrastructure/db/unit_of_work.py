"""SQLAlchemy implementation of the application Unit of Work contract."""

from collections.abc import Callable
from typing import Self

from sqlalchemy.orm import Session

from palio.app.unit_of_work import UnitOfWork

type SessionFactory = Callable[[], Session]


class SqlAlchemyUnitOfWork(UnitOfWork):
    """Wrap one SQLAlchemy session in a Unit of Work boundary.

    Args:
        session_factory: Factory used to open one ORM session per workflow.
    """

    def __init__(self, session_factory: SessionFactory) -> None:
        """Store the session factory for later workflow-scoped sessions."""
        self._session_factory = session_factory
        self._session: Session | None = None

    def __enter__(self) -> Self:
        """Open a session at the start of the workflow."""
        self._session = self._session_factory()
        return self

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        """Rollback on errors and always close the session."""
        if self._session is None:
            return

        if exc_type is not None:
            self._session.rollback()

        self._session.close()
        self._session = None

    def commit(self) -> None:
        """Commit the current transaction."""
        self.session().commit()

    def rollback(self) -> None:
        """Rollback the current transaction."""
        self.session().rollback()

    @property
    def session(self) -> Session:
        """Return the active session or fail fast when misused.

        Returns:
            The active SQLAlchemy session.

        Raises:
            RuntimeError: When the Unit of Work is used outside its context.
        """
        if self._session is None:
            raise RuntimeError(
                "UnitOfWork has no active session. Use it within a with block."
            )

        return self._session
