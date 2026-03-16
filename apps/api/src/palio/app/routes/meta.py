"""Operational meta routes."""

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from palio.app.bootstrap import ApplicationRuntime


def create_meta_router(runtime: ApplicationRuntime) -> APIRouter:
    """Create the operational meta router."""

    router = APIRouter(tags=["meta"])

    @router.get("/healthz")
    async def healthcheck() -> dict[str, object]:
        return {
            "status": "ok",
            "app": runtime.settings.app_name,
            "modules": runtime.modules.names(),
        }

    @router.get(
        "/readyz",
        responses={
            status.HTTP_503_SERVICE_UNAVAILABLE: {
                "description": "Backend runtime is not ready"
            }
        },
    )
    async def readiness() -> JSONResponse:
        readiness_check = runtime.database.check_readiness()
        status_code = (
            status.HTTP_200_OK
            if readiness_check.is_ready
            else status.HTTP_503_SERVICE_UNAVAILABLE
        )
        return JSONResponse(
            status_code=status_code,
            content={
                "status": "ok" if readiness_check.is_ready else "not_ready",
                "checks": {
                    "database": readiness_check.reason,
                },
            },
        )

    @router.get("/version")
    async def version() -> dict[str, object]:
        payload: dict[str, object] = {
            "app": runtime.settings.app_name,
            "environment": runtime.settings.environment.value,
            "version": runtime.settings.build.version,
        }
        if runtime.settings.build.commit_sha is not None:
            payload["commit_sha"] = runtime.settings.build.commit_sha
        return payload

    return router
