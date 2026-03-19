"""HTTP and realtime routing surfaces."""

from palio.api.routes.admin import create_admin_router
from palio.api.routes.meta import create_meta_router
from palio.api.routes.public import create_public_router
from palio.api.routes.realtime import create_realtime_router

__all__ = [
    "create_admin_router",
    "create_meta_router",
    "create_public_router",
    "create_realtime_router",
]
