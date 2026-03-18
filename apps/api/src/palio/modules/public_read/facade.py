"""Public facade for the public read module."""

from palio.shared.module_facade import ModuleFacade

PublicReadFacade = ModuleFacade


def build_public_read_facade() -> PublicReadFacade:
    """Build the public facade for the public read module."""
    return ModuleFacade(
        module_name="public_read",
        purpose="Read-only screen-shaped queries for public and maxi views.",
    )
