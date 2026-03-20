from __future__ import annotations

from palio.api.errors.spec import ApiProblemSpec

MISSING_ANY_CAPABILITY_API_PROBLEM = ApiProblemSpec(
    code="MISSING_ANY_CAPABILITY",
    type_uri="https://api.palioboard.local/problems/missing-any-capability",
    title="Missing any capability",
    http_status=403,
)

__all__ = [
    "MISSING_ANY_CAPABILITY_API_PROBLEM",
]
