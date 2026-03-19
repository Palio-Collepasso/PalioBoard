"""SQLAlchemy-backed Unit of Work implementations."""

from dataclasses import dataclass

from palio.infrastructure.db.runtime import (
    DatabaseRuntime,
    SessionFactory,
)
from palio.infrastructure.db.transaction import SqlAlchemyTransaction
from palio.shared.db.unit_of_work import UnitOfWork, UnitOfWorkFactory


class SqlAlchemyUnitOfWork(UnitOfWork):
    """Create SQLAlchemy-backed transactions for one workflow."""

    def __init__(self, session_factory: SessionFactory) -> None:
        """Store the session factory for later transaction creation."""
        self._session_factory = session_factory

    def begin(self) -> SqlAlchemyTransaction:
        """Create one active SQLAlchemy transaction."""
        return SqlAlchemyTransaction(self._session_factory())


@dataclass(frozen=True, slots=True)
class SqlAlchemyUnitOfWorkFactory(UnitOfWorkFactory):
    """Create SQLAlchemy-backed Unit of Work instances."""

    session_factory: SessionFactory

    def __call__(self) -> SqlAlchemyUnitOfWork:
        """Create one SQLAlchemy-backed Unit of Work instance."""
        return SqlAlchemyUnitOfWork(self.session_factory)


def build_sqlalchemy_unit_of_work_factory(
    *,
    database: DatabaseRuntime,
) -> SqlAlchemyUnitOfWorkFactory:
    """Build the SQLAlchemy-backed Unit of Work factory from the DB runtime."""
    return SqlAlchemyUnitOfWorkFactory(session_factory=database.session_factory)
