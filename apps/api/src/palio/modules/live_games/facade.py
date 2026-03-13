"""Public facade for the live games module."""

from palio.shared.module_facade import ModuleFacade

LiveGamesFacade = ModuleFacade


def build_live_games_facade() -> LiveGamesFacade:
    return ModuleFacade(
        module_name="live_games",
        purpose="In-memory live drafts, field leases, and provisional snapshots.",
    )
