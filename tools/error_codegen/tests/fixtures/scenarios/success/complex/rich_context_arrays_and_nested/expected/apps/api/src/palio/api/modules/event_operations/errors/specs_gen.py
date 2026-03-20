from __future__ import annotations

from palio.api.errors.spec import ApiProblemSpec

LIVE_CYCLE_MISMATCH_API_PROBLEM = ApiProblemSpec(
    code="LIVE_CYCLE_MISMATCH",
    type_uri="https://api.palioboard.local/problems/live-cycle-mismatch",
    title="Live cycle mismatch",
    http_status=409,
)

__all__ = [
    "LIVE_CYCLE_MISMATCH_API_PROBLEM",
]
