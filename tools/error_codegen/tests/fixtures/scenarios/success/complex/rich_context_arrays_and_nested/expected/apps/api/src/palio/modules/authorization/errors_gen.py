from __future__ import annotations

from dataclasses import dataclass
from palio.shared.errors import DomainError


@dataclass(slots=True)
class MissingAnyCapabilityError(DomainError):
    required_any: list[str]
    granted: list[str]

__all__ = [
    "MissingAnyCapabilityError",
]
