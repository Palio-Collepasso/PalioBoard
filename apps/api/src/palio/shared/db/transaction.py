"""Application-facing transaction and Unit of Work contracts."""

from typing import Protocol, Self, runtime_checkable


@runtime_checkable
class Transaction(Protocol):
    """Application-level active transaction."""

    def __enter__(self) -> Self:
        """Enter and return the active transaction."""
        ...

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: object | None,
    ) -> None:
        """Rollback on errors and always close the transaction."""
        ...

    def commit(self) -> None:
        """Commit the current transaction."""
        ...

    def rollback(self) -> None:
        """Rollback the current transaction."""
        ...
