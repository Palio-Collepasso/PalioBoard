"""API-local runtime test support for error handling.

Keep this module focused on the target runtime seams only. It should resolve
the intended future modules and fail clearly if they are not present yet.
It must not adapt to the current bootstrap/export-openapi implementation.
"""

from collections.abc import Mapping
from dataclasses import dataclass
from importlib import import_module
from types import ModuleType

from fastapi import FastAPI
from fastapi.testclient import TestClient

PROBLEM_JSON_MEDIA_TYPE = "application/problem+json"
KNOWN_ERROR_ROUTE = "/_tests/errors/generated-domain"
UNMAPPED_ERROR_ROUTE = "/_tests/errors/unmapped-domain"
UNKNOWN_ERROR_ROUTE = "/_tests/errors/unknown"

DOMAIN_ERROR_BASE_MODULE = "palio.shared.errors"
API_ERROR_HANDLERS_MODULE = "palio.api.errors.handlers"
API_ERROR_SPEC_MODULE = "palio.api.errors.spec"
DOMAIN_ERROR_MODULE = "palio.modules.event_operations.errors_gen"
API_PROBLEM_SPEC_MODULE = "palio.api.modules.event_operations.errors.specs_gen"
API_MAPPING_MODULE = "palio.api.modules.event_operations.errors.mapping_gen"

KNOWN_DOMAIN_ERROR_NAME = "JollyAlreadyUsedError"
KNOWN_PROBLEM_SPEC_NAME = "JOLLY_ALREADY_USED_API_PROBLEM"
KNOWN_MAPPING_NAME = "ERROR_TO_PROBLEM"


@dataclass(frozen=True, slots=True)
class RuntimeResponse:
    """Expected response details for one synthetic runtime error."""

    status_code: int
    content_type: str
    body: object
    text: str


def _require_module(module_name: str, purpose: str) -> ModuleType:
    """Import one intended target module or fail with a clear assertion."""
    try:
        return import_module(module_name)
    except ModuleNotFoundError as error:
        raise AssertionError(
            f"Expected `{purpose}` module `{module_name}` to exist in the target API "
            "runtime layout."
        ) from error


def _resolve_attr(module: ModuleType, attribute_name: str, purpose: str) -> object:
    """Resolve one intended target attribute or fail with a clear assertion."""
    if hasattr(module, attribute_name):
        return getattr(module, attribute_name)
    raise AssertionError(
        f"Expected `{purpose}` attribute `{attribute_name}` in module "
        f"`{module.__name__}`."
    )


def resolve_generated_domain_error_type() -> type[Exception]:
    """Resolve the generated domain error type used by the known-error test."""
    module = _require_module(DOMAIN_ERROR_MODULE, "generated domain error")
    error_type = _resolve_attr(
        module,
        KNOWN_DOMAIN_ERROR_NAME,
        "generated domain error",
    )
    if not isinstance(error_type, type) or not issubclass(error_type, Exception):
        raise AssertionError(
            f"`{DOMAIN_ERROR_MODULE}.{KNOWN_DOMAIN_ERROR_NAME}` must be an "
            "Exception subclass."
        )
    return error_type


def resolve_api_problem_spec_type() -> type[object]:
    """Resolve the shared API problem-spec type used by generated constants."""
    module = _require_module(API_ERROR_SPEC_MODULE, "shared API problem spec")
    problem_spec_type = _resolve_attr(
        module,
        "ApiProblemSpec",
        "shared API problem spec",
    )
    if not isinstance(problem_spec_type, type):
        raise AssertionError(
            f"`{API_ERROR_SPEC_MODULE}.ApiProblemSpec` must be a type."
        )
    return problem_spec_type


def resolve_generated_api_problem_spec() -> object:
    """Resolve the generated API problem spec used by the known-error test."""
    problem_spec_type = resolve_api_problem_spec_type()
    module = _require_module(API_PROBLEM_SPEC_MODULE, "generated API problem spec")
    problem_spec = _resolve_attr(
        module,
        KNOWN_PROBLEM_SPEC_NAME,
        "generated API problem spec",
    )
    if not isinstance(problem_spec, problem_spec_type):
        raise AssertionError(
            f"`{API_PROBLEM_SPEC_MODULE}.{KNOWN_PROBLEM_SPEC_NAME}` must be an "
            "instance of the shared `ApiProblemSpec` type."
        )
    return problem_spec


def resolve_generated_domain_to_problem_mapping() -> dict[type[Exception], object]:
    """Resolve the generated domain-error to problem-spec mapping table."""
    module = _require_module(API_MAPPING_MODULE, "generated API mapping")
    mapping = _resolve_attr(module, KNOWN_MAPPING_NAME, "generated API mapping")
    if not isinstance(mapping, Mapping):
        raise AssertionError(
            f"`{API_MAPPING_MODULE}.{KNOWN_MAPPING_NAME}` must be a mapping."
        )
    return dict(mapping)


def resolve_api_error_handlers() -> object:
    """Resolve the generated API error registration entrypoint."""
    module = _require_module(API_ERROR_HANDLERS_MODULE, "API error handlers")
    return _resolve_attr(module, "register_error_handlers", "API error handlers")


def resolve_domain_error_base() -> type[Exception]:
    """Resolve the intended domain-error base class for unmapped-runtime tests."""
    module = _require_module(DOMAIN_ERROR_BASE_MODULE, "domain error base")
    error_base = _resolve_attr(module, "DomainError", "domain error base")
    if not isinstance(error_base, type) or not issubclass(error_base, Exception):
        raise AssertionError(
            f"`{DOMAIN_ERROR_BASE_MODULE}.DomainError` must be an Exception subclass."
        )
    return error_base


def build_known_problem_response() -> RuntimeResponse:
    """Exercise the target handler with one generated domain error."""
    error_type = resolve_generated_domain_error_type()
    problem_spec = resolve_generated_api_problem_spec()
    mapping = resolve_generated_domain_to_problem_mapping()
    if mapping.get(error_type) is not problem_spec:
        raise AssertionError(
            "The generated domain error must resolve to the generated API problem spec."
        )

    register_error_handlers = resolve_api_error_handlers()
    app = FastAPI()
    register_error_handlers(app)

    @app.get(KNOWN_ERROR_ROUTE)
    def raise_error() -> dict[str, str]:
        _raise_known_error(error_type)

    response = TestClient(app).get(KNOWN_ERROR_ROUTE)
    return RuntimeResponse(
        status_code=response.status_code,
        content_type=response.headers.get("content-type", ""),
        body=response.json(),
        text=response.text,
    )


def build_unmapped_problem_response() -> RuntimeResponse:
    """Exercise the target handler with one generated-but-unmapped domain error."""
    domain_error_base = resolve_domain_error_base()
    register_error_handlers = resolve_api_error_handlers()

    @dataclass(slots=True)
    class UnmappedGeneratedDomainError(domain_error_base):
        """Synthetic generated-style error that should not be claimed by the mapping."""

        game_id: str
        current_state: str

    app = FastAPI()
    register_error_handlers(app)

    @app.get(UNMAPPED_ERROR_ROUTE)
    def raise_error() -> dict[str, str]:
        raise UnmappedGeneratedDomainError(game_id="game-002", current_state="pending")

    response = TestClient(app, raise_server_exceptions=False).get(UNMAPPED_ERROR_ROUTE)
    return RuntimeResponse(
        status_code=response.status_code,
        content_type=response.headers.get("content-type", ""),
        body=response.text,
        text=response.text,
    )


def build_unknown_exception_response() -> RuntimeResponse:
    """Exercise the generic FastAPI 500 path with an unknown exception."""
    register_error_handlers = resolve_api_error_handlers()
    app = FastAPI()
    register_error_handlers(app)

    @app.get(UNKNOWN_ERROR_ROUTE)
    def raise_error() -> dict[str, str]:
        raise RuntimeError("boom")

    response = TestClient(app, raise_server_exceptions=False).get(UNKNOWN_ERROR_ROUTE)
    return RuntimeResponse(
        status_code=response.status_code,
        content_type=response.headers.get("content-type", ""),
        body=response.text,
        text=response.text,
    )


def _raise_known_error(error_type: type[Exception]) -> None:
    """Raise one target generated domain error with explicit context values."""
    raise error_type(
        team_id="team-001",
        game_id="game-002",
        previous_game_id="game-003",
    )
