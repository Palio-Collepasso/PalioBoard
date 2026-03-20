from __future__ import annotations

from dataclasses import dataclass
from palio.shared.errors import DomainError


@dataclass(slots=True)
class TeamNotFoundError(DomainError):
    team_id: str

__all__ = [
    "TeamNotFoundError",
]
