"""Placeholder admin API routes."""

from fastapi import APIRouter

from palio.app.bootstrap import ApplicationRuntime


def create_admin_router(runtime: ApplicationRuntime) -> APIRouter:
    router = APIRouter(prefix="/api/admin", tags=["admin"])

    @router.get("/health")
    def admin_health() -> dict[str, object]:
        return {
            "surface": "admin",
            "status": "ok",
            "modules": runtime.modules.names(),
        }

    return router
