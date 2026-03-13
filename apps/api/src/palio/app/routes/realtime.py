"""Placeholder realtime routes."""

from fastapi import APIRouter, WebSocket

from palio.app.bootstrap import ApplicationRuntime


def create_realtime_router(runtime: ApplicationRuntime) -> APIRouter:
    router = APIRouter(prefix="/realtime", tags=["realtime"])

    @router.get("/health")
    def realtime_health() -> dict[str, object]:
        return {
            "surface": "realtime",
            "status": "ok",
            "modules": [
                runtime.modules.live_games.module_name,
                runtime.modules.event_operations.module_name,
            ],
        }

    @router.websocket("/ws")
    async def realtime_websocket(websocket: WebSocket) -> None:
        await websocket.accept()
        await websocket.send_json({"surface": "realtime", "status": "ready"})
        await websocket.close()

    return router
