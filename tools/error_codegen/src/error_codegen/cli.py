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
    help="Validate and generate API error-catalog artifacts.",
)

CATALOG_ARGUMENT = typer.Argument(
    help="Path to the root error catalog index.yaml file.",
    dir_okay=False,
    resolve_path=True,
)
SCHEMA_OPTION = typer.Option(
    "--schema",
    dir_okay=False,
    resolve_path=True,
    help="Path to the JSON Schema that validates the catalog format.",
)

CatalogArgumentPath = Annotated[Path, CATALOG_ARGUMENT]
SchemaOptionPath = Annotated[Path, SCHEMA_OPTION]


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


@app.command("validate")
def validate_command(
    catalog: CatalogArgumentPath = DEFAULT_CATALOG_INDEX_PATH,
    schema: SchemaOptionPath = DEFAULT_SCHEMA_PATH,
) -> None:
    """Validate the catalog and print a concise summary.

    It performs:
    - catalog schema validation
    - semantic validation
    - duplicate checks
    - example/context validation
    """
    typer.echo(
        run_cli(
            lambda: validate_error_catalog(catalog_path=catalog, schema_path=schema),
            handled_errors=(CatalogValidationError,),
        )
    )


@app.command("generate")
def generate_command(
    catalog: CatalogArgumentPath = DEFAULT_CATALOG_INDEX_PATH,
    schema: SchemaOptionPath = DEFAULT_SCHEMA_PATH,
    output_root: Annotated[
        Path,
        typer.Option(
            "--output-root",
            file_okay=False,
            resolve_path=True,
            help="Directory that receives generated backend module files.",
        ),
    ] = DEFAULT_OUTPUT_ROOT,
    ts_output: Annotated[
        Path,
        typer.Option(
            "--ts-output",
            dir_okay=False,
            resolve_path=True,
            help="Output path for the generated TypeScript file.",
        ),
    ] = DEFAULT_TS_OUTPUT_PATH,
    docs_output: Annotated[
        Path,
        typer.Option(
            "--docs-output",
            dir_okay=False,
            resolve_path=True,
            help="Output path for the generated error-contract markdown file.",
        ),
    ] = DEFAULT_DOCS_OUTPUT_PATH,
) -> None:
    """Generate artifacts.

    - Python per-module files
    - TypeScript artifact
    - docs
    """
    written_paths = run_cli(
        lambda: generate_error_artifacts(
            catalog_path=catalog,
            schema_path=schema,
            python_output_root=output_root,
            typescript_output_path=ts_output,
            docs_output_path=docs_output,
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
