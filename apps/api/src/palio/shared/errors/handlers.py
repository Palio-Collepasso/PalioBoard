"""FastAPI wiring for catalog-backed application errors."""

from collections.abc import Mapping
from typing import Any, cast

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.types import ExceptionHandler

from palio.shared.errors.base import ApplicationError


async def handle_application_error(
    _request: Request,
    error: ApplicationError,
) -> JSONResponse:
    """Serialize one catalog-backed exception as RFC 9457-style problem details."""
    problem_details = _build_problem_details(error)
    return JSONResponse(
        status_code=error.error_definition.http_status,
        content=jsonable_encoder(problem_details),
        media_type="application/problem+json",
    )


def register_error_handlers(app: FastAPI) -> None:
    """Register shared exception handlers on the application."""
    app.add_exception_handler(
        ApplicationError,
        cast(ExceptionHandler, handle_application_error),
    )


def _build_problem_details(error: ApplicationError) -> Mapping[str, Any]:
    """Build the stable problem-details payload for one application error."""
    problem_details: dict[str, Any] = {
        "type": error.error_definition.type_uri,
        "code": error.error_definition.code,
        "title": error.error_definition.title,
        "status": error.error_definition.http_status,
        "context": dict(error.context),
    }
    if error.detail is not None:
        problem_details["detail"] = error.detail
    return problem_details
