"""Typer CLI for the error-code generation toolchain."""

from collections.abc import Callable
from pathlib import Path
from typing import Annotated

import typer

from error_codegen import (
    DEFAULT_CATALOG_INDEX_PATH,
    DEFAULT_DOCS_OUTPUT_PATH,
    DEFAULT_OUTPUT_ROOT,
    DEFAULT_SCHEMA_PATH,
    DEFAULT_TS_OUTPUT_PATH,
    CatalogValidationError,
    generate_error_artifacts,
    validate_error_catalog,
)

app = typer.Typer(
    add_completion=False,
    no_args_is_help=True,
    help=(
        "Validate the error catalog and generate shared error artifacts.\n\n"
        "The catalog is the single source of truth for:\n"
        "- error identifiers\n"
        "- HTTP transport metadata\n"
        "- safe-to-expose context schema\n\n"
        "Generated artifacts include:\n"
        "- Python module-local error definitions\n"
        "- frontend TypeScript error metadata\n"
        "- Markdown error contract documentation"
    ),
)

CATALOG_OPTION = typer.Option(
    "--catalog-index",
    metavar="PATH",
    show_default="contracts/errors/index.yaml",
    help="Path to the root catalog index.yaml.",
)


def run_cli[T](
    operation: Callable[[], T],
    *,
    handled_errors: tuple[type[Exception], ...],
) -> T:
    """Run a CLI operation and convert handled errors into exit code 1."""
    try:
        return operation()
    except handled_errors as error:
        typer.echo(str(error), err=True)
        raise typer.Exit(code=1) from error


@app.command(
    "validate",
    help=(
        "Validate the error catalog.\n\n"
        "This command checks:\n"
        "- YAML/schema structure\n"
        "- per-entry semantic rules\n"
        "- cross-catalog invariants\n"
        "- context schema consistency"
    ),
    short_help="Validate the error catalog.",
)
def validate_command(
    catalog_index: Annotated[str, CATALOG_OPTION] = str(DEFAULT_CATALOG_INDEX_PATH),
    _json: Annotated[
        bool,
        typer.Option(
            "--json",
            help="Output validation results as JSON.",
        ),
    ] = False,
    _fail_fast: Annotated[
        bool,
        typer.Option(
            "--fail-fast/--no-fail-fast",
            help="Stop at the first validation error.",
        ),
    ] = False,
) -> None:
    """Validate the error catalog.

    This command checks:
    - YAML/schema structure
    - per-entry semantic rules
    - cross-catalog invariants
    - context schema consistency
    """
    typer.echo(
        run_cli(
            lambda: validate_error_catalog(
                catalog_path=Path(catalog_index),
                schema_path=DEFAULT_SCHEMA_PATH,
            ),
            handled_errors=(CatalogValidationError,),
        )
    )


@app.command(
    "generate",
    help=(
        "Generate all shared error artifacts from the catalog.\n\n"
        "Generated outputs:\n"
        "- Python module-local error definitions\n"
        "- TypeScript frontend error metadata\n"
        "- Markdown error contract documentation"
    ),
    short_help="Generate Python, TypeScript, and Markdown artifacts.",
)
def generate_command(
    catalog_index: Annotated[str, CATALOG_OPTION] = str(DEFAULT_CATALOG_INDEX_PATH),
    output_root: Annotated[
        str,
        typer.Option(
            "--python-out",
            metavar="PATH",
            show_default="apps/api/app/modules",
            help="Output directory for generated Python module files.",
        ),
    ] = str(DEFAULT_OUTPUT_ROOT),
    ts_output: Annotated[
        str,
        typer.Option(
            "--typescript-out",
            metavar="PATH",
            show_default="apps/web/src/shared/api/error-codes.gen.ts",
            help="Output file for generated TypeScript artifact.",
        ),
    ] = str(DEFAULT_TS_OUTPUT_PATH),
    docs_output: Annotated[
        str,
        typer.Option(
            "--docs-out",
            metavar="PATH",
            show_default="docs/api/error-contract.md",
            help="Output file for generated Markdown documentation.",
        ),
    ] = str(DEFAULT_DOCS_OUTPUT_PATH),
    _check: Annotated[
        bool,
        typer.Option(
            "--check/--no-check",
            help="Validate the catalog before generating artifacts.",
        ),
    ] = True,
) -> None:
    """Generate all shared error artifacts from the catalog.

    Generated outputs:
    - Python module-local error definitions
    - TypeScript frontend error metadata
    - Markdown error contract documentation
    """
    written_paths = run_cli(
        lambda: generate_error_artifacts(
            catalog_path=Path(catalog_index),
            schema_path=DEFAULT_SCHEMA_PATH,
            python_output_root=Path(output_root),
            typescript_output_path=Path(ts_output),
            docs_output_path=Path(docs_output),
        ),
        handled_errors=(CatalogValidationError,),
    )
    for written_path in written_paths:
        typer.echo(written_path)


def main() -> None:
    """Run the error-codegen CLI."""
    app()


if __name__ == "__main__":
    main()
