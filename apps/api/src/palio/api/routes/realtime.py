"""Placeholder realtime routes."""

from fastapi import APIRouter, Depends, WebSocket

from palio.api.dependencies import get_runtime
from palio.bootstrap.runtime import ApplicationRuntime

router = APIRouter(prefix="/realtime", tags=["realtime"])


@router.get("/health")
async def realtime_health(
    runtime: ApplicationRuntime = Depends(get_runtime),  # noqa: B008
) -> dict[str, object]:
    """Return a placeholder health payload for the realtime surface."""
    return {
        "surface": "realtime",
        "status": "ok",
        "modules": (
            runtime.app.transaction_services_factory.realtime_surface_module_names()
        ),
    }


@router.websocket("/ws")
async def realtime_websocket(websocket: WebSocket) -> None:
    """Accept one websocket and return the placeholder ready payload."""
    await websocket.accept()
    await websocket.send_json({"surface": "realtime", "status": "ready"})
    await websocket.close()
