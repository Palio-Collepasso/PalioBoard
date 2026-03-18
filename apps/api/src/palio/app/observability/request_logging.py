"""HTTP request logging middleware helpers."""

from collections.abc import Awaitable, Callable
from time import perf_counter

from fastapi import Request
from loguru import logger
from starlette.responses import Response

from palio.app.observability.request_context import get_request_id

type RequestHandler = Callable[[Request], Awaitable[Response]]


def _elapsed_ms(started_at: float) -> float:
    """Calculate elapsed time in milliseconds since the given start time."""
    return round((perf_counter() - started_at) * 1000, 3)


def create_request_logging_middleware() -> Callable[
    [Request, RequestHandler], Awaitable[Response]
]:
    """Create middleware that logs HTTP requests using the current request id."""

    async def request_logging_middleware(
        request: Request,
        call_next: RequestHandler,
    ) -> Response:
        started_at = perf_counter()

        with logger.contextualize(
            request_id=get_request_id(),
            method=request.method,
            path=request.url.path,
        ):
            try:
                response = await call_next(request)
            except Exception:
                logger.bind(duration_ms=_elapsed_ms(started_at)).exception(
                    "request.failed"
                )
                raise

            logger.bind(
                duration_ms=_elapsed_ms(started_at),
                status_code=response.status_code,
            ).info("request.completed")
        return response

    return request_logging_middleware
