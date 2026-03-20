from __future__ import annotations

from palio.modules.event_operations.errors_gen import JollyAlreadyUsedError, GameNotInProgressError, InvalidPlacementError
from .specs_gen import JOLLY_ALREADY_USED_API_PROBLEM, GAME_NOT_IN_PROGRESS_API_PROBLEM, INVALID_PLACEMENT_API_PROBLEM

ERROR_TO_PROBLEM = {
    JollyAlreadyUsedError: JOLLY_ALREADY_USED_API_PROBLEM,
    GameNotInProgressError: GAME_NOT_IN_PROGRESS_API_PROBLEM,
    InvalidPlacementError: INVALID_PLACEMENT_API_PROBLEM,
}

__all__ = ["ERROR_TO_PROBLEM"]
