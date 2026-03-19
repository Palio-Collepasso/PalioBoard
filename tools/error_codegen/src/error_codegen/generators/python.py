"""Generate Python error-definition artifacts from the catalog."""

import shutil
import subprocess
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from error_codegen.common import REPOSITORY_ROOT, write_text_artifact
from error_codegen.generators.common import render_template
from error_codegen.models import ErrorCatalog, ErrorCatalogEntry

DEFAULT_OUTPUT_ROOT = REPOSITORY_ROOT / "apps" / "api" / "src" / "palio" / "modules"
GENERATED_FILENAME = "error_defs_gen.py"


@dataclass(frozen=True, slots=True)
class GeneratedPythonModuleArtifact:
    """One generated Python error-definition artifact for a backend module."""

    module_name: str
    output_path: Path
    content: str


def build_python_error_module_artifacts(
    catalog: ErrorCatalog,
    output_root: Path = DEFAULT_OUTPUT_ROOT,
) -> tuple[GeneratedPythonModuleArtifact, ...]:
    """Render one generated definition module per imported backend module."""
    artifacts: list[GeneratedPythonModuleArtifact] = []
    for fragment in catalog.fragments:
        artifacts.append(
            GeneratedPythonModuleArtifact(
                module_name=fragment.module_name,
                output_path=output_root / fragment.module_name / GENERATED_FILENAME,
                content=_render_module_source(fragment.module_name, fragment.errors),
            )
        )
    return tuple(artifacts)


def write_python_error_module_artifacts(
    catalog: ErrorCatalog,
    output_root: Path = DEFAULT_OUTPUT_ROOT,
) -> tuple[Path, ...]:
    """Write generated Python error-definition modules to disk."""
    written_paths = tuple(
        write_text_artifact(artifact.output_path, artifact.content)
        for artifact in build_python_error_module_artifacts(
            catalog,
            output_root=output_root,
        )
    )
    _format_python_artifacts(written_paths)
    return written_paths


def _render_module_source(
    module_name: str,
    entries: Sequence[ErrorCatalogEntry],
) -> str:
    uppercase_exports = sorted(
        [
            "ERROR_DEFINITIONS",
            "ERROR_DEFINITIONS_BY_CODE",
            "ERROR_CODES",
            "MODULE_NAME",
            *[entry.code for entry in entries],
        ]
    )
    export_names = [*uppercase_exports, "ErrorDefinition"]
    return render_template(
        "python_errors.py.j2",
        module_name=module_name,
        entries=entries,
        export_names=export_names,
    )


def _format_python_artifacts(paths: Sequence[Path]) -> None:
    """Run Ruff format on generated Python artifacts when available."""
    if not paths:
        return

    ruff_binary = shutil.which("ruff")
    if ruff_binary is None:
        return

    subprocess.run(
        [ruff_binary, "format", *[str(path) for path in paths]],
        check=True,
        cwd=REPOSITORY_ROOT / "apps" / "api",
    )
