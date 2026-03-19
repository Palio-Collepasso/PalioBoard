from pathlib import Path

from error_codegen.generators.python import (
    GENERATED_FILENAME,
    build_python_error_module_artifacts,
)
from support.sample_catalog import MODULE_NAMES, build_sample_catalog


def test_build_python_error_module_artifacts_preserves_module_order() -> None:
    artifacts = build_python_error_module_artifacts(
        build_sample_catalog(),
        output_root=Path("/tmp/generated-modules"),
    )

    assert tuple(artifact.module_name for artifact in artifacts) == MODULE_NAMES
    assert (
        artifacts[2].output_path
        == Path("/tmp/generated-modules/event_operations") / GENERATED_FILENAME
    )


def test_build_python_error_module_artifact_renders_metadata_only_source() -> None:
    artifact = build_python_error_module_artifacts(
        build_sample_catalog(),
        output_root=Path("/tmp/generated-modules"),
    )[2]

    assert "from palio.shared.errors.base import ErrorDefinition" in artifact.content
    assert "JOLLY_ALREADY_USED = ErrorDefinition(" in artifact.content
    assert "ERROR_DEFINITIONS_BY_CODE" in artifact.content
    assert "class " not in artifact.content
