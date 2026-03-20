from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ApiProblemSpec:
    code: str
    type_uri: str
    title: str
    http_status: int
    translation_key: str | None = None


JOLLY_ALREADY_USED_API_PROBLEM = ApiProblemSpec(
    code="JOLLY_ALREADY_USED",
    type_uri="https://api.palioboard.local/problems/jolly-already-used",
    title="Jolly already used",
    http_status=409,
    translation_key="errors.jollyAlreadyUsed",
)

GAME_NOT_IN_PROGRESS_API_PROBLEM = ApiProblemSpec(
    code="GAME_NOT_IN_PROGRESS",
    type_uri="https://api.palioboard.local/problems/game-not-in-progress",
    title="Game not in progress",
    http_status=409,
    translation_key="errors.gameNotInProgress",
)
