from __future__ import annotations

from dataclasses import dataclass
from typing import Literal
from palio.shared.errors import DomainError


@dataclass(slots=True)
class TeamNotFoundError(DomainError):
    team_id: str
    source: Literal['route', 'body', 'query'] | None = None

__all__ = [
    "TeamNotFoundError",
]
