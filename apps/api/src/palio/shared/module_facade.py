"""Shared facade descriptor reused by the module scaffold."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ModuleFacade:
    """Minimal public contract exposed by a bounded module."""

    module_name: str
    purpose: str
