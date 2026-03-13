"""Public facade for the tournaments module."""

from palio.shared.module_facade import ModuleFacade

TournamentsFacade = ModuleFacade


def build_tournaments_facade() -> TournamentsFacade:
    return ModuleFacade(
        module_name="tournaments",
        purpose="Bracket progression and tournament result materialization.",
    )
