"""FastAPI app factory."""

from fastapi import FastAPI

from palio.app.bootstrap import ApplicationRuntime, build_runtime
from palio.app.observability import (
    configure_logging,
    create_request_context_middleware,
    create_request_logging_middleware,
)
from palio.app.routes import (
    create_admin_router,
    create_meta_router,
    create_public_router,
    create_realtime_router,
)


def create_app(runtime: ApplicationRuntime | None = None) -> FastAPI:
    """Create the backend FastAPI application with explicit runtime wiring."""

    runtime = runtime or build_runtime()
    configure_logging(runtime.settings.logging)
    app = FastAPI(
        title=runtime.settings.api_title,
        version=runtime.settings.build.version,
    )
    app.state.runtime = runtime
    app.middleware("http")(create_request_logging_middleware())
    app.middleware("http")(
        create_request_context_middleware(runtime.settings.request_context)
    )
    app.include_router(create_meta_router(runtime))
    app.include_router(create_admin_router(runtime))
    app.include_router(create_public_router(runtime))
    app.include_router(create_realtime_router(runtime))

    return app
