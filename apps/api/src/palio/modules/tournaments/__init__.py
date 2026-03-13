"""Tournaments module public surface."""

from palio.modules.tournaments.facade import (
    TournamentsFacade,
    build_tournaments_facade,
)

__all__ = ["TournamentsFacade", "build_tournaments_facade"]
