"""Prototype-only helpers for future generated module contract tests.

This module should stay tiny and pure. It exists to share import and source
path checks for future generated API-spec and mapping modules.
"""

from importlib import import_module
from pathlib import Path
from types import ModuleType


def require_module(module_name: str) -> ModuleType:
    """Import one future generated module or fail with a clear assertion."""
    try:
        return import_module(module_name)
    except ModuleNotFoundError as error:
        raise AssertionError(
            f"Expected future generated module `{module_name}` to exist."
        ) from error


def require_attr(module: ModuleType, attr_name: str) -> object:
    """Resolve one attribute from a generated module or fail clearly."""
    if hasattr(module, attr_name):
        return getattr(module, attr_name)
    raise AssertionError(
        f"Expected `{attr_name}` in future generated module `{module.__name__}`."
    )


def module_source_path(module: ModuleType) -> Path:
    """Return the source file path for a generated module."""
    path = getattr(module, "__file__", None)
    if not isinstance(path, str):
        raise AssertionError(f"Module `{module.__name__}` has no source file path.")
    return Path(path)
