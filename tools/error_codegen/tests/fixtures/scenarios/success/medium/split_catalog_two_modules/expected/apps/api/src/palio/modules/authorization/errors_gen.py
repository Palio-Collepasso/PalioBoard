from __future__ import annotations

from dataclasses import dataclass
from palio.shared.errors import DomainError


@dataclass(slots=True)
class MissingCapabilityError(DomainError):
    capability: str

__all__ = [
    "MissingCapabilityError",
]
