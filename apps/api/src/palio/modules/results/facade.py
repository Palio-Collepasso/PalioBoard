"""Public facade for the results module."""

from palio.shared.module_facade import ModuleFacade

ResultsFacade = ModuleFacade


def build_results_facade() -> ResultsFacade:
    """Build the public facade for the results module."""
    return ModuleFacade(
        module_name="results",
        purpose="Canonical official result persistence via game entries and fields.",
    )
