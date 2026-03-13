"""Placeholder public API routes."""

from fastapi import APIRouter

from palio.app.bootstrap import ApplicationRuntime


def create_public_router(runtime: ApplicationRuntime) -> APIRouter:
    router = APIRouter(prefix="/api/public", tags=["public"])

    @router.get("/health")
    def public_health() -> dict[str, object]:
        return {
            "surface": "public",
            "status": "ok",
            "modules": [
                runtime.modules.public_read.module_name,
                runtime.modules.leaderboard_projection.module_name,
            ],
        }

    return router
