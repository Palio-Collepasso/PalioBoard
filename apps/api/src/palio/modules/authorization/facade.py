"""Public facade for the authorization module."""

from palio.shared.module_facade import ModuleFacade

AuthorizationFacade = ModuleFacade


def build_authorization_facade() -> AuthorizationFacade:
    """Build the public facade for the authorization module."""
    return ModuleFacade(
        module_name="authorization",
        purpose="Capability vocabulary, role resolution, and policy checks.",
    )
