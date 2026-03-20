"""API runtime mapping tests for catalog-backed domain errors.

This file enforces the known-error contract only:
resolve the generated API problem spec, serialize `application/problem+json`,
and preserve the payload fields and runtime context values.
It should not depend on the tool support package or the broader tool scenario
tree.
"""

from fastapi import status

from .runtime_support import (
    KNOWN_ERROR_ROUTE,
    build_known_problem_response,
    resolve_generated_api_problem_spec,
    resolve_generated_domain_error_type,
    resolve_generated_domain_to_problem_mapping,
)


def test_generated_domain_error_resolves_generated_api_problem_spec() -> None:
    """A known generated domain error should resolve the generated API problem spec."""
    error_type = resolve_generated_domain_error_type()
    spec = resolve_generated_api_problem_spec()
    mapping = resolve_generated_domain_to_problem_mapping()

    assert spec.code == "JOLLY_ALREADY_USED"
    assert spec.type_uri == "https://api.palioboard.local/problems/jolly-already-used"
    assert spec.title == "Jolly already used"
    assert spec.http_status == status.HTTP_409_CONFLICT
    assert mapping[error_type] is spec


def test_known_domain_error_response_uses_application_problem_json() -> None:
    """Known domain errors should serialize as `application/problem+json`."""
    response = build_known_problem_response()

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.content_type.startswith("application/problem+json")


def test_known_domain_error_response_includes_type_code_title_status_and_context() -> (
    None
):
    """Mapped responses should expose the core Problem Details payload fields."""
    response = build_known_problem_response()

    assert response.body == {
        "type": "https://api.palioboard.local/problems/jolly-already-used",
        "code": "JOLLY_ALREADY_USED",
        "title": "Jolly already used",
        "status": status.HTTP_409_CONFLICT,
        "context": {
            "team_id": "team-001",
            "game_id": "game-002",
            "previous_game_id": "game-003",
        },
    }


def test_known_domain_error_response_preserves_context_values() -> None:
    """Context values from the domain error should be preserved in the response."""
    response = build_known_problem_response()

    assert response.body["context"] == {
        "team_id": "team-001",
        "game_id": "game-002",
        "previous_game_id": "game-003",
    }
    assert KNOWN_ERROR_ROUTE == "/_tests/errors/generated-domain"
