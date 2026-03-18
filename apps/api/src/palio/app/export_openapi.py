"""Export the FastAPI OpenAPI contract as a committed repository artifact."""

from pathlib import Path
from typing import Annotated

import typer
import yaml

from palio.app.factory import create_app

REPOSITORY_ROOT = Path(__file__).resolve().parents[5]
DEFAULT_OUTPUT_PATH = REPOSITORY_ROOT / "docs" / "api" / "openapi.yaml"


def export_openapi(output_path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    """Write the current FastAPI OpenAPI schema to the requested path."""
    resolved_output_path = output_path.resolve()
    resolved_output_path.parent.mkdir(parents=True, exist_ok=True)

    specification = create_app().openapi()
    resolved_output_path.write_text(
        yaml.safe_dump(specification, sort_keys=False),
        encoding="utf-8",
    )
    return resolved_output_path


def main(
    output: Annotated[
        Path,
        typer.Argument(
            help="Output path for the generated OpenAPI YAML file.",
            dir_okay=False,
            resolve_path=True,
        ),
    ] = DEFAULT_OUTPUT_PATH,
) -> None:
    """Run the OpenAPI export CLI."""
    typer.echo(export_openapi(output))


if __name__ == "__main__":
    typer.run(main)
