"""Placeholder public API routes."""

from fastapi import APIRouter, Depends

from palio.api.dependencies import get_runtime
from palio.bootstrap.runtime import ApplicationRuntime

router = APIRouter(prefix="/api/public", tags=["public"])


@router.get("/health")
async def public_health(
    runtime: ApplicationRuntime = Depends(get_runtime),  # noqa: B008
) -> dict[str, object]:
    """Return a placeholder health payload for the public surface."""
    return {
        "surface": "public",
        "status": "ok",
        "modules": (
            runtime.app.transaction_services_factory.public_surface_module_names()
        ),
    }
