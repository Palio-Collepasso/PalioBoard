from __future__ import annotations

from palio.modules.live_games.errors_gen import GameAlreadyClosedError
from .specs_gen import GAME_ALREADY_CLOSED_API_PROBLEM

ERROR_TO_PROBLEM = {
    GameAlreadyClosedError: GAME_ALREADY_CLOSED_API_PROBLEM,
}

__all__ = ["ERROR_TO_PROBLEM"]
