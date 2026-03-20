from __future__ import annotations

from palio.modules.event_operations.errors_gen import GameNotInProgressError
from .specs_gen import GAME_NOT_IN_PROGRESS_API_PROBLEM

ERROR_TO_PROBLEM = {
    GameNotInProgressError: GAME_NOT_IN_PROGRESS_API_PROBLEM,
}

__all__ = ["ERROR_TO_PROBLEM"]
