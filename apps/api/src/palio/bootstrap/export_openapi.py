"""Export the FastAPI OpenAPI contract as a committed repository artifact."""

from pathlib import Path
from typing import Annotated

import typer
import yaml

from palio.bootstrap.app_services import build_app_services
from palio.bootstrap.factory import create_app
from palio.bootstrap.runtime import ApplicationRuntime
from palio.infrastructure.db import ReadinessCheck
from palio.settings import ApplicationSettings, load_settings
from palio.shared.db.unit_of_work import UnitOfWork, UnitOfWorkFactory

REPOSITORY_ROOT = Path(__file__).resolve().parents[5]
DEFAULT_OUTPUT_PATH = REPOSITORY_ROOT / "docs" / "api" / "openapi.yaml"


class PlaceholderUnitOfWorkFactory(UnitOfWorkFactory):
    """Sentinel factory used by export/test runtimes without DB access."""

    def __call__(self) -> UnitOfWork:
        """Fail fast when transaction-backed dependencies are requested."""
        raise RuntimeError(
            "Placeholder runtime does not support opening application transactions."
        )


class PlaceholderDatabaseRuntime:
    """Explicit non-configured database runtime for export-only runtimes."""

    def check_readiness(self) -> ReadinessCheck:
        """Report that the placeholder runtime is not ready for DB traffic."""
        return ReadinessCheck(
            is_ready=False,
            reason="database_not_configured",
        )


def build_placeholder_runtime(
    *,
    settings: ApplicationSettings | None = None,
) -> ApplicationRuntime:
    """Build an explicit non-request-capable runtime for export and smoke tests."""
    resolved_settings = settings or load_settings()
    return ApplicationRuntime(
        settings=resolved_settings,
        database=PlaceholderDatabaseRuntime(),
        app=build_app_services(uow_factory=PlaceholderUnitOfWorkFactory()),
    )


def export_openapi(output_path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    """Write the current FastAPI OpenAPI schema to the requested path."""
    resolved_output_path = output_path.resolve()
    resolved_output_path.parent.mkdir(parents=True, exist_ok=True)

    specification = create_app(runtime=build_placeholder_runtime()).openapi()
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
