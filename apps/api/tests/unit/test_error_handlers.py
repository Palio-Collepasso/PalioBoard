from typing import cast
from uuid import UUID

from fastapi import APIRouter, status
from fastapi.testclient import TestClient

from palio.bootstrap import create_app
from palio.bootstrap.export_openapi import build_placeholder_runtime
from palio.shared.errors import (
    ApplicationError,
    ErrorDefinition,
    InvalidErrorContextError,
)

USER_MISSING_DEFINITION = ErrorDefinition(
    code="USER_MISSING",
    module_name="users",
    type_slug="user-missing",
    type_uri="https://api.palioboard.local/problems/user-missing",
    http_status=status.HTTP_404_NOT_FOUND,
    title="User missing",
    description="The requested user does not exist.",
    category="not_found",
    retry_policy="never",
    safe_to_expose=True,
    translation_key="errors.userMissing",
    log_level="INFO",
    severity="low",
    context_schema={
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "user_id": {
                "type": "string",
                "format": "uuid",
            }
        },
        "required": ["user_id"],
    },
    notes_for_operators=None,
)


class UserMissingError(ApplicationError):
    error_definition = USER_MISSING_DEFINITION

    def __init__(self, user_id: UUID) -> None:
        super().__init__(context={"user_id": user_id})


def test_application_error_is_serialized_as_problem_details() -> None:
    app = create_app(runtime=build_placeholder_runtime())
    router = APIRouter()

    def raise_user_missing() -> None:
        raise UserMissingError(UUID("01956c9f-6f7e-7b42-a4b0-2d21d920c001"))

    router.add_api_route(
        "/_tests/errors/application", raise_user_missing, methods=["GET"]
    )
    app.include_router(router)

    with TestClient(app) as client:
        response = client.get("/_tests/errors/application")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.headers["content-type"].startswith("application/problem+json")
    assert response.json() == {
        "type": "https://api.palioboard.local/problems/user-missing",
        "code": "USER_MISSING",
        "title": "User missing",
        "status": status.HTTP_404_NOT_FOUND,
        "context": {
            "user_id": "01956c9f-6f7e-7b42-a4b0-2d21d920c001",
        },
    }


def test_application_error_rejects_invalid_runtime_context() -> None:
    try:
        UserMissingError(cast(UUID, "not-a-uuid"))
    except InvalidErrorContextError as error:
        assert "Invalid context for `USER_MISSING`" in str(error)
    else:  # pragma: no cover - defensive assertion branch
        raise AssertionError("Expected invalid runtime context to be rejected.")


def test_unknown_exceptions_keep_default_fastapi_500_behavior() -> None:
    app = create_app(runtime=build_placeholder_runtime())
    router = APIRouter()

    def raise_runtime_error() -> None:
        raise RuntimeError("boom")

    router.add_api_route(
        "/_tests/errors/unhandled", raise_runtime_error, methods=["GET"]
    )
    app.include_router(router)

    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.get("/_tests/errors/unhandled")

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.text == "Internal Server Error"
