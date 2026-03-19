"""Shared tooling for the API error catalog workflow."""

from pathlib import Path

from error_codegen.common import (
    DEFAULT_CATALOG_INDEX_PATH,
    DEFAULT_MODULES_ROOT,
    DEFAULT_SCHEMA_PATH,
)
from error_codegen.generators.docs import (
    DEFAULT_OUTPUT_PATH as DEFAULT_DOCS_OUTPUT_PATH,
)
from error_codegen.generators.docs import (
    write_error_contract,
)
from error_codegen.generators.python import (
    DEFAULT_OUTPUT_ROOT,
    write_python_error_module_artifacts,
)
from error_codegen.generators.typescript import (
    DEFAULT_OUTPUT_PATH as DEFAULT_TS_OUTPUT_PATH,
)
from error_codegen.generators.typescript import (
    write_typescript_error_artifact,
)
from error_codegen.loader import load_error_catalog
from error_codegen.models import (
    CatalogValidationIssue,
    ErrorCatalog,
    ErrorCatalogEntry,
    ErrorCatalogFragment,
)
from error_codegen.validators import CatalogValidationError

__all__ = [
    "DEFAULT_CATALOG_INDEX_PATH",
    "DEFAULT_DOCS_OUTPUT_PATH",
    "DEFAULT_MODULES_ROOT",
    "DEFAULT_OUTPUT_ROOT",
    "DEFAULT_SCHEMA_PATH",
    "DEFAULT_TS_OUTPUT_PATH",
    "CatalogValidationError",
    "CatalogValidationIssue",
    "ErrorCatalog",
    "ErrorCatalogEntry",
    "ErrorCatalogFragment",
    "generate_error_artifacts",
    "generate_error_docs",
    "generate_python_errors",
    "generate_ts_errors",
    "load_error_catalog",
    "validate_error_catalog",
]


def validate_error_catalog(
    catalog_path: Path = DEFAULT_CATALOG_INDEX_PATH,
    schema_path: Path = DEFAULT_SCHEMA_PATH,
) -> str:
    """Validate the committed catalog and return a concise summary."""
    catalog = load_error_catalog(catalog_path=catalog_path, schema_path=schema_path)
    error_count = len(catalog.errors)
    return (
        "Validated "
        f"{len(catalog.fragments)} module fragments, "
        f"{error_count} error entries, and "
        f"{len(catalog.shared_context_schemas)} shared context schemas."
    )


def generate_python_errors(
    catalog_path: Path = DEFAULT_CATALOG_INDEX_PATH,
    schema_path: Path = DEFAULT_SCHEMA_PATH,
    output_root: Path = DEFAULT_OUTPUT_ROOT,
) -> tuple[Path, ...]:
    """Generate the per-module Python error-code artifacts."""
    catalog = load_error_catalog(catalog_path=catalog_path, schema_path=schema_path)
    return write_python_error_module_artifacts(catalog, output_root=output_root)


def generate_ts_errors(
    catalog_path: Path = DEFAULT_CATALOG_INDEX_PATH,
    schema_path: Path = DEFAULT_SCHEMA_PATH,
    output_path: Path = DEFAULT_TS_OUTPUT_PATH,
) -> Path:
    """Generate the frontend error-code artifact from the committed catalog."""
    catalog = load_error_catalog(catalog_path=catalog_path, schema_path=schema_path)
    return write_typescript_error_artifact(catalog, output_path=output_path)


def generate_error_docs(
    catalog_path: Path = DEFAULT_CATALOG_INDEX_PATH,
    schema_path: Path = DEFAULT_SCHEMA_PATH,
    output_path: Path = DEFAULT_DOCS_OUTPUT_PATH,
) -> Path:
    """Render and write the generated error contract document."""
    catalog = load_error_catalog(catalog_path=catalog_path, schema_path=schema_path)
    return write_error_contract(catalog, output_path=output_path)


def generate_error_artifacts(
    catalog_path: Path = DEFAULT_CATALOG_INDEX_PATH,
    schema_path: Path = DEFAULT_SCHEMA_PATH,
    *,
    python_output_root: Path = DEFAULT_OUTPUT_ROOT,
    typescript_output_path: Path = DEFAULT_TS_OUTPUT_PATH,
    docs_output_path: Path = DEFAULT_DOCS_OUTPUT_PATH,
) -> tuple[Path, ...]:
    """Generate the committed Python, TypeScript, and docs artifacts."""
    catalog = load_error_catalog(catalog_path=catalog_path, schema_path=schema_path)
    python_paths = write_python_error_module_artifacts(
        catalog,
        output_root=python_output_root,
    )
    typescript_path = write_typescript_error_artifact(
        catalog,
        output_path=typescript_output_path,
    )
    docs_path = write_error_contract(catalog, output_path=docs_output_path)
    return (*python_paths, typescript_path, docs_path)
