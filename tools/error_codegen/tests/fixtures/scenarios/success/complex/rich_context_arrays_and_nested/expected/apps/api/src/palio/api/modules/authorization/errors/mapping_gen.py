from __future__ import annotations

from palio.modules.authorization.errors_gen import MissingAnyCapabilityError
from .specs_gen import MISSING_ANY_CAPABILITY_API_PROBLEM

ERROR_TO_PROBLEM = {
    MissingAnyCapabilityError: MISSING_ANY_CAPABILITY_API_PROBLEM,
}

__all__ = ["ERROR_TO_PROBLEM"]
