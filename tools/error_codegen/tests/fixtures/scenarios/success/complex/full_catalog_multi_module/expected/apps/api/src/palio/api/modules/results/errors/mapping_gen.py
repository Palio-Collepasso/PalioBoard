from __future__ import annotations

from palio.modules.results.errors_gen import PlacementConflictError
from .specs_gen import PLACEMENT_CONFLICT_API_PROBLEM

ERROR_TO_PROBLEM = {
    PlacementConflictError: PLACEMENT_CONFLICT_API_PROBLEM,
}

__all__ = ["ERROR_TO_PROBLEM"]
