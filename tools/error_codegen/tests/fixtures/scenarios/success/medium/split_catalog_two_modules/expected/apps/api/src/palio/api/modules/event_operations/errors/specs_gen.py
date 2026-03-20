from __future__ import annotations

from palio.api.errors.spec import ApiProblemSpec

GAME_NOT_IN_PROGRESS_API_PROBLEM = ApiProblemSpec(
    code="GAME_NOT_IN_PROGRESS",
    type_uri="https://api.palioboard.local/problems/game-not-in-progress",
    title="Game not in progress",
    http_status=409,
)

__all__ = [
    "GAME_NOT_IN_PROGRESS_API_PROBLEM",
]
