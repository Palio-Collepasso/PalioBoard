"""HTTP and realtime routing surfaces."""

from palio.app.routes.admin import create_admin_router
from palio.app.routes.meta import create_meta_router
from palio.app.routes.public import create_public_router
from palio.app.routes.realtime import create_realtime_router

__all__ = [
    "create_admin_router",
    "create_meta_router",
    "create_public_router",
    "create_realtime_router",
]
