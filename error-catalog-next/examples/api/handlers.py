from fastapi.responses import JSONResponse

from palio.shared.errors import DomainError

from .problem_details import build_problem_payload
from .registry import ERROR_TO_PROBLEM


def domain_error_to_response(exc: DomainError) -> JSONResponse:
    problem_spec = ERROR_TO_PROBLEM[type(exc)]
    return JSONResponse(
        status_code=problem_spec.http_status,
        content=build_problem_payload(problem_spec, exc),
        media_type="application/problem+json",
    )
