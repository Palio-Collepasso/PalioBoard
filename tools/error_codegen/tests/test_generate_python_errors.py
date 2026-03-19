from pathlib import Path

from error_codegen import generate_python_errors, load_error_catalog
from error_codegen.generators.python import (
    GENERATED_FILENAME,
    build_python_error_module_artifacts,
)
from support.error_catalog import (
    MODULE_IMPORTS,
    load_module_from_path,
    write_catalog,
)


def test_generate_python_errors_writes_expected_module_artifacts(
    tmp_path: Path,
) -> None:
    catalog = load_error_catalog()
    output_root = tmp_path / "modules"

    written_paths = generate_python_errors(output_root=output_root)
    expected_artifacts = build_python_error_module_artifacts(
        catalog,
        output_root=output_root,
    )

    assert written_paths == tuple(
        artifact.output_path for artifact in expected_artifacts
    )

    first_pass = {
        artifact.output_path: artifact.output_path.read_text(encoding="utf-8")
        for artifact in expected_artifacts
    }

    regenerated_paths = generate_python_errors(output_root=output_root)

    assert regenerated_paths == written_paths
    for output_path, rendered_source in first_pass.items():
        assert output_path.read_text(encoding="utf-8") == rendered_source


def test_generate_python_errors_emits_module_constants_and_metadata(
    tmp_path: Path,
) -> None:
    catalog_path = write_catalog(
        tmp_path,
        imports=MODULE_IMPORTS,
        fragments={
            "users.yaml": """
errors:
  USER_MISSING:
    type_slug: user-missing
    recommended_http_status: 404
    title: User missing
    description: The requested user does not exist.
    category: not_found
    retry_policy: never
    safe_to_expose: true
    context_schema:
      type: object
      additionalProperties: false
      properties:
        user_id:
          $ref: "#/shared_context_schemas/UuidRef"
          required: true
    example:
      context:
        user_id: "01956c9f-6f7e-7b42-a4b0-2d21d920c001"
""".strip()
            + "\n"
        },
    )
    output_root = tmp_path / "generated"

    generate_python_errors(catalog_path=catalog_path, output_root=output_root)
    module = load_module_from_path(
        output_root / "users" / GENERATED_FILENAME,
        module_name="generated_users_error_codes",
    )

    assert module.MODULE_NAME == "users"
    assert module.ERROR_CODES == ("USER_MISSING",)
    assert module.USER_MISSING == "USER_MISSING"
    assert module.USER_MISSING_METADATA.code == "USER_MISSING"
    assert module.USER_MISSING_METADATA.title == "User missing"
    assert module.ERROR_BY_CODE["USER_MISSING"] is module.USER_MISSING_METADATA
    assert module.get_error("USER_MISSING") is module.USER_MISSING_METADATA
    assert module.ERROR_BY_TYPE_URI[module.USER_MISSING_METADATA.type_uri] is (
        module.USER_MISSING_METADATA
    )
