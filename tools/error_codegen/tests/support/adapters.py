"""Import and rendering adapters for tool-side tests.

Keep this module focused on the generator tool. Runtime HTTP helpers must live
under API test support.
"""

from __future__ import annotations

import importlib
import inspect
from collections.abc import Callable
from pathlib import Path
from types import ModuleType

from typer.testing import CliRunner


def import_module_from_candidates(candidates: list[str]) -> ModuleType:
    """Import the first available module from a list of candidates.

    Args:
        candidates: Fully qualified module names to try in order.

    Returns:
        The imported module.

    Raises:
        AssertionError: If none of the candidate modules can be imported.
    """
    last_error: Exception | None = None
    for module_name in candidates:
        try:
            return importlib.import_module(module_name)
        except Exception as error:  # pragma: no cover - actionable mismatch path
            last_error = error
    raise AssertionError(
        "Unable to import any of the expected tool modules: "
        f"{candidates!r}. Update the tool-side test adapters to match "
        "the final repo paths. "
        f"Last error: {last_error}"
    )


def resolve_attr(module: ModuleType, candidates: list[str]) -> object:
    """Resolve the first available attribute from a module.

    Args:
        module: Imported module object.
        candidates: Attribute names to try in order.

    Returns:
        The resolved attribute.

    Raises:
        AssertionError: If no candidate attribute exists on the module.
    """
    for attribute_name in candidates:
        if hasattr(module, attribute_name):
            return getattr(module, attribute_name)
    raise AssertionError(
        f"Expected one of {candidates!r} in `{module.__name__}`, but none was found."
    )


def call_with_known_params(
    function: Callable[..., object], /, *args: object, **kwargs: object
) -> object:
    """Call a function using only supported keyword arguments.

    This keeps tests resilient to small signature changes during refactors.

    Args:
        function: Callable under test.
        *args: Positional arguments.
        **kwargs: Candidate keyword arguments.

    Returns:
        The result of calling the function.
    """
    signature = inspect.signature(function)
    accepted_kwargs = {
        name: value for name, value in kwargs.items() if name in signature.parameters
    }
    return function(*args, **accepted_kwargs)


def load_catalog(index_path: Path) -> object:
    """Load a catalog from its ``index.yaml`` path.

    Args:
        index_path: Path to the catalog root index file.

    Returns:
        The loaded catalog model.
    """
    module = import_module_from_candidates(
        [
            "tools.error_codegen.loader",
            "error_codegen.loader",
        ]
    )
    function = resolve_attr(module, ["load_error_catalog"])
    signature = inspect.signature(function)

    if "catalog_index_path" in signature.parameters:
        return function(catalog_index_path=index_path)
    if "index_path" in signature.parameters:
        return function(index_path=index_path)
    return function(index_path)


def catalog_validation_error_type() -> type[Exception]:
    """Return the catalog validation exception type used by the tool.

    Returns:
        The concrete validation exception class.
    """
    module = import_module_from_candidates(
        [
            "tools.error_codegen.validators",
            "error_codegen.validators",
        ]
    )
    error_type = resolve_attr(module, ["CatalogValidationError"])
    if not isinstance(error_type, type) or not issubclass(error_type, Exception):
        raise AssertionError("CatalogValidationError must be an Exception subclass.")
    return error_type


def build_python_artifacts(catalog: object) -> dict[str, str]:
    """Build generated Python definition artifacts keyed by relative path.

    Args:
        catalog: Loaded catalog model.

    Returns:
        Mapping from relative output path to rendered Python source.
    """
    module = import_module_from_candidates(
        [
            "tools.error_codegen.generators.python",
            "error_codegen.generators.python",
        ]
    )
    function = resolve_attr(
        module,
        [
            "build_python_error_definition_artifacts",
            "build_python_error_module_artifacts",
        ],
    )
    result = function(catalog)

    if isinstance(result, dict):
        return {str(path): str(source) for path, source in result.items()}

    normalized: dict[str, str] = {}
    for artifact in result:
        if hasattr(artifact, "relative_path") and hasattr(artifact, "source"):
            normalized[str(artifact.relative_path)] = str(artifact.source)
            continue
        if hasattr(artifact, "output_path") and hasattr(artifact, "content"):
            normalized[str(artifact.output_path)] = str(artifact.content)
            continue
        if hasattr(artifact, "output_path") and hasattr(artifact, "source"):
            normalized[str(artifact.output_path)] = str(artifact.source)
            continue
        if hasattr(artifact, "module_name") and hasattr(artifact, "source"):
            normalized[f"{artifact.module_name}/error_defs_gen.py"] = str(
                artifact.source
            )
            continue
        raise AssertionError(
            "Unrecognized Python artifact shape. Update the tool-side test adapters to "
            "match the final generator return type."
        )
    return normalized


def render_typescript_artifact(catalog: object) -> str:
    """Render the merged TypeScript error artifact.

    Args:
        catalog: Loaded catalog model.

    Returns:
        Rendered TypeScript source.
    """
    module = import_module_from_candidates(
        [
            "tools.error_codegen.generators.typescript",
            "error_codegen.generators.typescript",
        ]
    )
    function = resolve_attr(
        module,
        [
            "generate_typescript_error_artifact",
            "render_typescript_error_artifact",
        ],
    )
    return str(function(catalog)).strip()


def render_docs_artifact(catalog: object, *, title: str) -> str:
    """Render the Markdown error-contract document.

    Args:
        catalog: Loaded catalog model.
        title: Document title to inject.

    Returns:
        Rendered Markdown content.
    """
    module = import_module_from_candidates(
        [
            "tools.error_codegen.generators.docs",
            "error_codegen.generators.docs",
        ]
    )
    function = resolve_attr(module, ["render_error_contract"])
    rendered = call_with_known_params(
        function,
        catalog,
        title=title,
        document_title=title,
    )
    return str(rendered).strip()


def cli_runner() -> tuple[CliRunner, object]:
    """Return a ``CliRunner`` and the Typer application object.

    Returns:
        Tuple of test CLI runner and app object.
    """
    module = import_module_from_candidates(
        [
            "tools.error_codegen.cli",
            "error_codegen.cli",
        ]
    )
    app = resolve_attr(module, ["app", "cli"])
    return CliRunner(), app
