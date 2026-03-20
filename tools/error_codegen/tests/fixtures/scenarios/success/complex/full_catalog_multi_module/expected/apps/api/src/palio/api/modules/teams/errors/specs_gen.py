from __future__ import annotations

from palio.api.errors.spec import ApiProblemSpec

TEAM_NOT_FOUND_API_PROBLEM = ApiProblemSpec(
    code="TEAM_NOT_FOUND",
    type_uri="https://api.palioboard.local/problems/team-not-found",
    title="Team not found",
    http_status=404,
)

__all__ = [
    "TEAM_NOT_FOUND_API_PROBLEM",
]
