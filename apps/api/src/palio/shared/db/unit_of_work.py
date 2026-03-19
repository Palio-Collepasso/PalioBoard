from typing import Protocol, runtime_checkable

from palio.shared.db.transaction import Transaction


@runtime_checkable
class UnitOfWork(Protocol):
    """Factory-like boundary that starts application transactions."""

    def begin(self) -> Transaction:
        """Open and return a new active transaction."""
        ...


@runtime_checkable
class UnitOfWorkFactory(Protocol):
    """Callable factory that creates one Unit of Work instance."""

    def __call__(self) -> UnitOfWork:
        """Create one Unit of Work instance."""
        ...
