from __future__ import annotations

from dataclasses import dataclass
from palio.shared.errors import DomainError


@dataclass(slots=True)
class InvalidEntryPayloadError(DomainError):
    field: str
    reason: str

__all__ = [
    "InvalidEntryPayloadError",
]
