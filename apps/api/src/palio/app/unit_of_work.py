"""Application-facing Unit of Work contract for use-case orchestration."""

from typing import Protocol, Self


class UnitOfWork(Protocol):
    """Transaction boundary contract used by application orchestrators."""

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
