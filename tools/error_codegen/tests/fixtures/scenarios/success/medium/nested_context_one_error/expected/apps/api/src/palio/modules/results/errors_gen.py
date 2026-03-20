from __future__ import annotations

from dataclasses import dataclass
from palio.shared.errors import DomainError


@dataclass(slots=True)
class PlacementConflictError(DomainError):
    game_id: str
    existing_result: dict[str, object]
    incoming_result: dict[str, object]

__all__ = [
    "PlacementConflictError",
]
