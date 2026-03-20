"""API runtime handler tests for unknown and unmapped exceptions.

This file enforces the handler-level guarantees that are not specific to a
known catalog error: unknown exceptions remain generic 500 behavior, and
unmapped generated errors are not silently claimed as catalog problems.
It should not depend on generator tests or the tool scenario tree.
"""

from fastapi import status

from .runtime_support import (
    build_unknown_exception_response,
    build_unmapped_problem_response,
)


def test_unknown_exception_remains_generic_500_behavior() -> None:
    """Unhandled exceptions should stay on the generic 500 path."""
    response = build_unknown_exception_response()

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.text == "Internal Server Error"


def test_unmapped_exception_is_not_claimed_as_catalog_problem() -> None:
    """An unmapped runtime exception should not be serialized as a catalog error."""
    response = build_unmapped_problem_response()

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert not response.content_type.startswith("application/problem+json")
    assert response.text == "Internal Server Error"
