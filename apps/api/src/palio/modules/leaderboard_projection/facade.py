"""Public facade for the leaderboard projection module."""

from palio.shared.module_facade import ModuleFacade

LeaderboardProjectionFacade = ModuleFacade


def build_leaderboard_projection_facade() -> LeaderboardProjectionFacade:
    """Build the public facade for the leaderboard projection module."""
    return ModuleFacade(
        module_name="leaderboard_projection",
        purpose="Synchronous standings recomputation and projection tables.",
    )
