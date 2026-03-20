from __future__ import annotations

from palio.api.errors.spec import ApiProblemSpec

MISSING_CAPABILITY_API_PROBLEM = ApiProblemSpec(
    code="MISSING_CAPABILITY",
    type_uri="https://api.palioboard.local/problems/missing-capability",
    title="Missing capability",
    http_status=403,
)

__all__ = [
    "MISSING_CAPABILITY_API_PROBLEM",
]
