"""Shared Unit of Work contract owned by application orchestration."""

from typing import Protocol


class UnitOfWork(Protocol):
    """Placeholder Unit of Work protocol for session-bound workflows."""

    def commit(self) -> None: ...

    def rollback(self) -> None: ...
