"""SQLAlchemy-backed transaction implementation."""

from typing import Self

from sqlalchemy.orm import Session

from palio.shared.db.transaction import Transaction


class SqlAlchemyTransaction(Transaction):
    """Wrap one SQLAlchemy session in an active transaction scope."""

    def __init__(self, session: Session) -> None:
        """Store the active SQLAlchemy session for this transaction."""
        self._session = session

    def __enter__(self) -> Self:
        """Enter and return the active transaction."""
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: object | None,
    ) -> None:
        """Rollback on errors and always close the transaction session."""
        if exc_type is not None:
            self._session.rollback()

        self._session.close()

    def commit(self) -> None:
        """Commit the active transaction."""
        self.session.commit()

    def rollback(self) -> None:
        """Rollback the active transaction."""
        self.session.rollback()

    @property
    def session(self) -> Session:
        """Expose the SQLAlchemy session to infrastructure wiring only."""
        return self._session
