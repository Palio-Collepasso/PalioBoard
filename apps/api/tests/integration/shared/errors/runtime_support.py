"""API-local runtime test support for error handling.

Prototype-only skeleton. The final implementation should live here, not in the
tool test support package.
"""

from typing import Any


def problem_runtime_primitives() -> tuple[type[Any], type[Exception], Any]:
    """Return runtime primitives needed by API error mapping tests."""
    raise NotImplementedError


def build_problem_response(
    expected_payload: dict[str, Any],
) -> tuple[int, str, dict[str, Any]]:
    """Build a Problem Details response for a synthetic runtime error."""
    raise NotImplementedError
