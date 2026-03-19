"""HTTP and realtime routing surfaces."""

from palio.api.routes.admin import router as admin_router
from palio.api.routes.meta import router as meta_router
from palio.api.routes.public import router as public_router
from palio.api.routes.realtime import router as realtime_router

__all__ = [
    "admin_router",
    "meta_router",
    "public_router",
    "realtime_router",
]
