"""API endpoint-flow integration test for catalog-backed problem details.

This file enforces the HTTP-facing end-to-end contract through a fake test-only
endpoint backed by a self-contained fake generated error contract.
"""

from pathlib import Path

from fastapi import status

from .error_endpoint_support import (
    PROBLEM_JSON_MEDIA_TYPE,
    build_fake_generated_contract,
    invoke_fake_problem_endpoint,
)


def test_fake_endpoint_exists_for_the_problem_details_flow(tmp_path: Path) -> None:
    """A test-only endpoint should exist and be callable through HTTP."""
    response = invoke_fake_problem_endpoint(tmp_path)

    assert response.status_code == status.HTTP_409_CONFLICT


def test_fake_endpoint_raises_a_fake_mapped_domain_error(tmp_path: Path) -> None:
    """The fake generated domain error should resolve to the fake generated spec."""
    contract = build_fake_generated_contract(tmp_path)

    assert contract.mapping[contract.domain_error_type] is contract.problem_spec


def test_fake_endpoint_returns_application_problem_json_response(
    tmp_path: Path,
) -> None:
    """The end-to-end response should use `application/problem+json`."""
    response = invoke_fake_problem_endpoint(tmp_path)

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.content_type.startswith(PROBLEM_JSON_MEDIA_TYPE)


def test_fake_endpoint_problem_response_includes_expected_fields(
    tmp_path: Path,
) -> None:
    """The response should include `type`, `code`, `title`, `status`, and `context`."""
    response = invoke_fake_problem_endpoint(tmp_path)

    assert response.body == response.contract.expected_body


def test_fake_endpoint_problem_response_preserves_context_values(
    tmp_path: Path,
) -> None:
    """The response context should match the fake domain error values."""
    response = invoke_fake_problem_endpoint(tmp_path)

    assert response.body["context"] == response.contract.expected_body["context"]
