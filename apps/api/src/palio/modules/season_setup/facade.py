"""Public facade for the season setup module."""

from palio.shared.module_facade import ModuleFacade

SeasonSetupFacade = ModuleFacade


def build_season_setup_facade() -> SeasonSetupFacade:
    return ModuleFacade(
        module_name="season_setup",
        purpose="Season, teams, competitions, games, points configuration, and field catalogs.",
    )
