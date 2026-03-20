from __future__ import annotations

from palio.api.errors.spec import ApiProblemSpec

JOLLY_ALREADY_USED_API_PROBLEM = ApiProblemSpec(
    code="JOLLY_ALREADY_USED",
    type_uri="https://api.palioboard.local/problems/jolly-already-used",
    title="Jolly already used",
    http_status=409,
)

GAME_NOT_IN_PROGRESS_API_PROBLEM = ApiProblemSpec(
    code="GAME_NOT_IN_PROGRESS",
    type_uri="https://api.palioboard.local/problems/game-not-in-progress",
    title="Game not in progress",
    http_status=409,
)

__all__ = [
    "JOLLY_ALREADY_USED_API_PROBLEM",
    "GAME_NOT_IN_PROGRESS_API_PROBLEM",
]
