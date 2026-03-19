"""Placeholder admin API routes."""

from fastapi import APIRouter, Depends

from palio.api.dependencies import get_runtime
from palio.bootstrap.runtime import ApplicationRuntime

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/health")
async def admin_health(
    runtime: ApplicationRuntime = Depends(get_runtime),  # noqa: B008
) -> dict[str, object]:
    """Return a placeholder health payload for the admin surface."""
    return {
        "surface": "admin",
        "status": "ok",
        "modules": runtime.app.module_names(),
    }
