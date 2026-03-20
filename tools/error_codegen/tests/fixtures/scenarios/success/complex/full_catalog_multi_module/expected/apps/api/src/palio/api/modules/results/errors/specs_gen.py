from __future__ import annotations

from palio.api.errors.spec import ApiProblemSpec

PLACEMENT_CONFLICT_API_PROBLEM = ApiProblemSpec(
    code="PLACEMENT_CONFLICT",
    type_uri="https://api.palioboard.local/problems/placement-conflict",
    title="Placement conflict",
    http_status=409,
)

__all__ = [
    "PLACEMENT_CONFLICT_API_PROBLEM",
]
