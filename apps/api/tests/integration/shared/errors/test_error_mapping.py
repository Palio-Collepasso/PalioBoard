"""Enforce API runtime mapping behavior for known catalog-backed errors.

This file should verify known domain or application errors serialize to
`application/problem+json` with `type`, `code`, `title`, `status`, and `context`.
It should not test generator behavior and should not depend on the full tool
scenario tree in the final shape.
"""

from typing import Any

import pytest

from tests.integration.shared.errors.runtime_support import build_problem_response


RUNTIME_SCENARIOS: tuple[tuple[str, dict[str, Any]], ...] = ()


@pytest.mark.parametrize(("scenario", "expected_payload"), RUNTIME_SCENARIOS)
def test_domain_errors_map_to_problem_responses_with_expected_fields(
    scenario: str,
    expected_payload: dict[str, Any],
) -> None:
    """Runtime mapping should preserve the core Problem Details fields and context."""
    del scenario
    status_code, content_type, actual_payload = build_problem_response(
        expected_payload
    )

    assert status_code == expected_payload["status"]
    assert content_type.startswith("application/problem+json")
    assert actual_payload["type"] == expected_payload["type"]
    assert actual_payload["code"] == expected_payload["code"]
    assert actual_payload["title"] == expected_payload["title"]
    assert actual_payload["status"] == expected_payload["status"]
    assert actual_payload.get("context", {}) == expected_payload.get("context", {})
