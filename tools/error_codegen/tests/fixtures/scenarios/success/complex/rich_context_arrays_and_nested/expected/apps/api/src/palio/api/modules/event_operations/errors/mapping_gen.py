from __future__ import annotations

from palio.modules.event_operations.errors_gen import LiveCycleMismatchError
from .specs_gen import LIVE_CYCLE_MISMATCH_API_PROBLEM

ERROR_TO_PROBLEM = {
    LiveCycleMismatchError: LIVE_CYCLE_MISMATCH_API_PROBLEM,
}

__all__ = ["ERROR_TO_PROBLEM"]
