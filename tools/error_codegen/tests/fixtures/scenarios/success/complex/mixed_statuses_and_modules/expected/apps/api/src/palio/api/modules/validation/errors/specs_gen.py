from __future__ import annotations

from palio.api.errors.spec import ApiProblemSpec

INVALID_ENTRY_PAYLOAD_API_PROBLEM = ApiProblemSpec(
    code="INVALID_ENTRY_PAYLOAD",
    type_uri="https://api.palioboard.local/problems/invalid-entry-payload",
    title="Invalid entry payload",
    http_status=400,
)

__all__ = [
    "INVALID_ENTRY_PAYLOAD_API_PROBLEM",
]
