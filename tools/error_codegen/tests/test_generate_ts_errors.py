from pathlib import Path

from error_codegen import (
    ErrorCatalog,
    ErrorCatalogEntry,
    ErrorCatalogFragment,
    generate_ts_errors,
)
from error_codegen.generators.typescript import (
    GENERATED_FILENAME,
    generate_typescript_error_artifact,
)
from support.error_catalog import write_catalog


def test_generate_typescript_error_artifact_is_stable_for_the_same_catalog() -> None:
    catalog = _make_catalog()

    first_render = generate_typescript_error_artifact(catalog)
    second_render = generate_typescript_error_artifact(catalog)

    assert first_render == second_render


def test_generate_typescript_error_artifact_renders_typed_context_helpers() -> None:
    catalog = _make_catalog()

    rendered = generate_typescript_error_artifact(catalog)

    assert 'export const ERROR_CATALOG_MODULES = [\n  "users"\n] as const;' in rendered
    assert "export type SharedContextUuidRef = string;" in rendered
    assert "export type UserMissingContext = {" in rendered
    assert '  "reason"?: "missing" | "inactive";' in rendered
    assert '  "user_id": SharedContextUuidRef;' in rendered
    assert 'export const ERROR_CODES = [\n  "USER_MISSING"\n] as const;' in rendered
    assert "export type CatalogProblemByCode = {" in rendered
    assert "export function matchesCatalogErrorCode(" in rendered
    assert (
        "export function isCatalogProblem(value: unknown): value is CatalogProblem"
        in rendered
    )
    assert 'const code = record["code"];' in rendered
    assert 'typeof record["type"] === "string"' in rendered
    assert "isCatalogErrorCode(code)" in rendered
    assert 'typeof record["title"] === "string"' in rendered
    assert 'typeof record["status"] === "number"' in rendered


def test_generate_ts_errors_writes_the_committed_artifact_shape(tmp_path: Path) -> None:
    catalog_path = write_catalog(
        tmp_path,
        fragments={
            "users.yaml": """
errors:
  USER_MISSING:
    type_slug: user-missing
    http_status: 404
    title: User missing
    description: The selected user does not exist.
    category: not_found
    retry_policy: never
    safe_to_expose: true
    log_level: WARNING
    context_schema:
      type: object
      additionalProperties: false
      properties:
        user_id:
          $ref: "#/shared_context_schemas/UuidRef"
        reason:
          type: string
          enum:
            - missing
            - inactive
      required:
        - user_id
""".strip()
            + "\n"
        },
    )
    output_path = tmp_path / "error-codes.generated.ts"

    resolved_output = generate_ts_errors(
        catalog_path=catalog_path,
        output_path=output_path,
    )

    assert resolved_output == output_path.resolve()
    rendered = resolved_output.read_text(encoding="utf-8")
    assert "USER_MISSING" in rendered
    assert "SharedContextUuidRef" in rendered
    assert "ERROR_CODES_BY_MODULE" in rendered
    assert resolved_output.name == GENERATED_FILENAME


def _make_catalog() -> ErrorCatalog:
    entry = ErrorCatalogEntry(
        code="USER_MISSING",
        module_name="users",
        source_path=Path("docs/api/errors/users.yaml"),
        type_slug="user-missing",
        type_uri="https://api.palioboard.local/problems/user-missing",
        http_status=404,
        title="User missing",
        description="The selected user does not exist.",
        category="not_found",
        retry_policy="never",
        safe_to_expose=True,
        translation_key="errors.userMissing",
        raw_context_schema={
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "user_id": {"$ref": "#/shared_context_schemas/UuidRef"},
                "reason": {
                    "type": "string",
                    "enum": ["missing", "inactive"],
                },
            },
            "required": ["user_id"],
        },
        normalized_context_schema={
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "reason": {
                    "type": "string",
                    "enum": ["missing", "inactive"],
                },
                "user_id": {"$ref": "#/shared_context_schemas/UuidRef"},
            },
            "required": ["user_id"],
        },
        type_uri_override=None,
        translation_key_override=None,
        log_level="WARNING",
        severity=None,
        example=None,
        notes_for_operators=None,
    )

    fragment = ErrorCatalogFragment(
        module_name="users",
        source_path=Path("docs/api/errors/users.yaml"),
        errors=(entry,),
    )

    return ErrorCatalog(
        catalog_path=Path("docs/api/errors/index.yaml"),
        schema_path=Path("docs/api/errors/schema.json"),
        namespace="palioboard",
        base_type_uri="https://api.palioboard.local/problems/",
        schema_dialect="https://json-schema.org/draft/2020-12/schema",
        default_media_type="application/problem+json",
        shared_context_schemas=ErrorCatalog.freeze_mapping(
            {
                "UuidRef": {
                    "type": "string",
                    "format": "uuid",
                }
            }
        ),
        fragments=(fragment,),
        errors=ErrorCatalog.freeze_mapping({"USER_MISSING": entry}),
    )
