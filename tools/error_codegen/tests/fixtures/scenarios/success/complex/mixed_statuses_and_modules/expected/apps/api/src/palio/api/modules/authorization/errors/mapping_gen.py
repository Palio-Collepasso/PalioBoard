from __future__ import annotations

from palio.modules.authorization.errors_gen import MissingCapabilityError
from .specs_gen import MISSING_CAPABILITY_API_PROBLEM

ERROR_TO_PROBLEM = {
    MissingCapabilityError: MISSING_CAPABILITY_API_PROBLEM,
}

__all__ = ["ERROR_TO_PROBLEM"]
