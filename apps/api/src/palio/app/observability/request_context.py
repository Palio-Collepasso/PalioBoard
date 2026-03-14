"""Request-context lifecycle helpers."""

from collections.abc import Awaitable, Callable
from contextvars import ContextVar, Token

from fastapi import Request
from starlette.responses import Response
from uuid6 import uuid7

from palio.settings import RequestContextSettings

type RequestHandler = Callable[[Request], Awaitable[Response]]

_request_id_context: ContextVar[str | None] = ContextVar(
    "palio_request_id",
    default=None,
)


def get_request_id() -> str | None:
    """Read the current request identifier from context."""

    return _request_id_context.get()


def bind_request_id(request_id: str) -> Token[str | None]:
    """Bind one request identifier to the current context."""

    return _request_id_context.set(request_id)


def reset_request_id(token: Token[str | None]) -> None:
    """Reset the request identifier context to the previous state."""

    _request_id_context.reset(token)


def generate_request_id() -> str:
    """Generate one UUIDv7 request identifier."""

    return str(uuid7())


def create_request_context_middleware(
    settings: RequestContextSettings,
) -> Callable[[Request, RequestHandler], Awaitable[Response]]:
    """Create middleware that manages request-id propagation and lifecycle."""

    async def request_context_middleware(
        request: Request,
        call_next: RequestHandler,
    ) -> Response:
        request_id = request.headers.get(settings.header_name) or generate_request_id()
        token = bind_request_id(request_id)
        request.state.request_id = request_id
        try:
            response = await call_next(request)
            response.headers[settings.header_name] = request_id
            return response
        finally:
            reset_request_id(token)

    return request_context_middleware
