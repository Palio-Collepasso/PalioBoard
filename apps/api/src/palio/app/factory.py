"""FastAPI app factory."""

from fastapi import FastAPI

from palio import __version__
from palio.app.bootstrap import ApplicationRuntime, build_runtime
from palio.app.routes import (
    create_admin_router,
    create_public_router,
    create_realtime_router,
)


def create_app(runtime: ApplicationRuntime | None = None) -> FastAPI:
    """Create the backend FastAPI application with explicit runtime wiring."""

    app = FastAPI(
        title="PalioBoard API",
        version=__version__,
    )
    runtime = runtime or build_runtime()
    app.state.runtime = runtime
    app.include_router(create_admin_router(runtime))
    app.include_router(create_public_router(runtime))
    app.include_router(create_realtime_router(runtime))

    @app.get("/healthz", tags=["meta"])
    def healthcheck() -> dict[str, object]:
        return {
            "status": "ok",
            "app": "palio-api",
            "modules": runtime.modules.names(),
        }

    return app
