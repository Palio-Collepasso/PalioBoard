"""Authorization module public surface."""

from palio.modules.authorization.facade import (
    AuthorizationFacade,
    build_authorization_facade,
)

__all__ = ["AuthorizationFacade", "build_authorization_facade"]
