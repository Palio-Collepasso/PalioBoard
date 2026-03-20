from __future__ import annotations

from palio.modules.event_operations.errors_gen import JollyAlreadyUsedError
from .specs_gen import JOLLY_ALREADY_USED_API_PROBLEM

ERROR_TO_PROBLEM = {
    JollyAlreadyUsedError: JOLLY_ALREADY_USED_API_PROBLEM,
}

__all__ = ["ERROR_TO_PROBLEM"]
