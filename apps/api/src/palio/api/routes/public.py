# pyright: reportUnusedFunction=false
"""Placeholder public API routes."""

from fastapi import APIRouter

from palio.bootstrap.runtime import ApplicationRuntime


def create_public_router(runtime: ApplicationRuntime) -> APIRouter:
    """Create the public API router."""
    router = APIRouter(prefix="/api/public", tags=["public"])

    @router.get("/health")
    async def public_health() -> dict[str, object]:
        return {
            "surface": "public",
            "status": "ok",
            "modules": [
                runtime.modules.public_read.module_name,
                runtime.modules.leaderboard_projection.module_name,
            ],
        }

    return router
