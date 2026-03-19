"""FastAPI app factory."""

from fastapi import FastAPI

from palio.api.middleware import (
    create_request_context_middleware,
    create_request_logging_middleware,
)
from palio.api.routes import (
    admin_router,
    meta_router,
    public_router,
    realtime_router,
)
from palio.bootstrap.logging import configure_logging
from palio.bootstrap.runtime import ApplicationRuntime
from palio.bootstrap.wiring import build_runtime
from palio.shared.errors.handlers import register_error_handlers


def create_app(runtime: ApplicationRuntime | None = None) -> FastAPI:
    """Create the API FastAPI application with explicit runtime wiring."""
    runtime = runtime or build_runtime()
    settings = runtime.settings
    configure_logging(settings.logging)
    app = FastAPI(
        title=settings.api_title,
        version=settings.build.version,
    )
    app.state.runtime = runtime
    register_error_handlers(app)
    app.middleware("http")(create_request_logging_middleware())
    app.middleware("http")(create_request_context_middleware(settings.request_context))
    app.include_router(meta_router)
    app.include_router(admin_router)
    app.include_router(public_router)
    app.include_router(realtime_router)

    return app
