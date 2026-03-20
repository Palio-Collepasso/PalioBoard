from __future__ import annotations

from palio.modules.teams.errors_gen import TeamNotFoundError
from .specs_gen import TEAM_NOT_FOUND_API_PROBLEM

ERROR_TO_PROBLEM = {
    TeamNotFoundError: TEAM_NOT_FOUND_API_PROBLEM,
}

__all__ = ["ERROR_TO_PROBLEM"]
