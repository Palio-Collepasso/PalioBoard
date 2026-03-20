from __future__ import annotations

from dataclasses import dataclass
from palio.shared.errors import DomainError


@dataclass(slots=True)
class LiveCycleMismatchError(DomainError):
    game_id: str
    expected: dict[str, object]
    actual: dict[str, object]

__all__ = [
    "LiveCycleMismatchError",
]
