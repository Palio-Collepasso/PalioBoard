"""Public facade for the users module."""

from palio.shared.module_facade import ModuleFacade

UsersFacade = ModuleFacade


def build_users_facade() -> UsersFacade:
    return ModuleFacade(
        module_name="users",
        purpose="Application users, IdP linkage, and superadmin provisioning.",
    )
