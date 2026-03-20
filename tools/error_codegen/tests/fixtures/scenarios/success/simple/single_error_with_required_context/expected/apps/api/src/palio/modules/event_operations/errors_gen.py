from __future__ import annotations

from dataclasses import dataclass
from palio.shared.errors import DomainError


@dataclass(slots=True)
class JollyAlreadyUsedError(DomainError):
    team_id: str
    game_id: str
    previous_game_id: str

__all__ = [
    "JollyAlreadyUsedError",
]
