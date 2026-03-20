from __future__ import annotations

from palio.api.errors.spec import ApiProblemSpec

GAME_ALREADY_CLOSED_API_PROBLEM = ApiProblemSpec(
    code="GAME_ALREADY_CLOSED",
    type_uri="https://api.palioboard.local/problems/game-already-closed",
    title="Game already closed",
    http_status=409,
)

__all__ = [
    "GAME_ALREADY_CLOSED_API_PROBLEM",
]
