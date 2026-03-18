"""Public facade for the identity module."""

from palio.shared.module_facade import ModuleFacade

IdentityFacade = ModuleFacade


def build_identity_facade() -> IdentityFacade:
    """Build the public facade for the identity module."""
    return ModuleFacade(
        module_name="identity",
        purpose="JWT verification, current principal resolution, and IdP adapters.",
    )
