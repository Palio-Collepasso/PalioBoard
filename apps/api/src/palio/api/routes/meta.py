"""Operational meta routes."""

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from palio.api.dependencies import get_runtime
from palio.bootstrap.runtime import ApplicationRuntime

router = APIRouter(tags=["meta"])


@router.get("/healthz")
async def healthcheck(
    runtime: ApplicationRuntime = Depends(get_runtime),  # noqa: B008
) -> dict[str, object]:
    """Return the basic process health payload."""
    return {
        "status": "ok",
        "app": runtime.settings.app_name,
        "modules": runtime.app.module_names(),
    }


@router.get(
    "/readyz",
    responses={
        status.HTTP_503_SERVICE_UNAVAILABLE: {"description": "Api runtime is not ready"}
    },
)
async def readiness(
    runtime: ApplicationRuntime = Depends(get_runtime),  # noqa: B008
) -> JSONResponse:
    """Return runtime readiness based on database availability."""
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
async def version(
    runtime: ApplicationRuntime = Depends(get_runtime),  # noqa: B008
) -> dict[str, object]:
    """Return build and environment metadata for the running API."""
    payload: dict[str, object] = {
        "app": runtime.settings.app_name,
        "environment": runtime.settings.environment.value,
        "version": runtime.settings.build.version,
    }
    if runtime.settings.build.commit_sha is not None:
        payload["commit_sha"] = runtime.settings.build.commit_sha
    return payload
