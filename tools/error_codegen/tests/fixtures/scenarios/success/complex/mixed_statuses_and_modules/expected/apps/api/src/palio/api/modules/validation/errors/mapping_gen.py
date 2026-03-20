from __future__ import annotations

from palio.modules.validation.errors_gen import InvalidEntryPayloadError
from .specs_gen import INVALID_ENTRY_PAYLOAD_API_PROBLEM

ERROR_TO_PROBLEM = {
    InvalidEntryPayloadError: INVALID_ENTRY_PAYLOAD_API_PROBLEM,
}

__all__ = ["ERROR_TO_PROBLEM"]
