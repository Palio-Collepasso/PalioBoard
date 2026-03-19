"""Shared runtime primitives for catalog-backed API errors."""

from palio.shared.errors.base import (
    ApplicationError,
    ErrorDefinition,
    InvalidErrorContextError,
)

__all__ = [
    "ApplicationError",
    "ErrorDefinition",
    "InvalidErrorContextError",
]
