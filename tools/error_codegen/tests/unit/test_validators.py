"""Enforce validator-level semantics and cross-file catalog rules.

This file should cover:
- valid split-catalog semantics passing at the validator level when applicable
- duplicate code across modules fails
- duplicate `type_slug` across modules fails
- example context satisfies `context_schema`
- missing required context fields fail
- extra context fields fail
- unknown shared refs fail
- import alignment/path rules
- context-schema normalization and closed-object behavior

It should not enforce model parsing shape, generated output, CLI behavior, or
API runtime behavior.
"""

from pathlib import Path
from textwrap import dedent, indent

import pytest

from error_codegen.loader import load_error_catalog
from error_codegen.models import CatalogValidationIssue
from error_codegen.validators import (
    CatalogValidationError,
    normalize_context_schema,
    resolve_context_schema_references,
    validate_context_references,
    validate_example_context,
    validate_import_alignment,
)


def _write_catalog(
    tmp_path: Path,
    *,
    index_imports: list[str],
    fragments: dict[str, str],
) -> Path:
    root = tmp_path / "contracts" / "errors"
    root.mkdir(parents=True)
    imports_block = "\n".join(f"  - {name}" for name in index_imports)
    (root / "index.yaml").write_text(
        (
            "catalog_version: 1\n"
            "namespace: palioboard\n"
            "base_type_uri: https://api.palioboard.local/problems/\n"
            "schema_dialect: https://json-schema.org/draft/2020-12/schema\n"
            "default_media_type: application/problem+json\n"
            "imports:\n"
            f"{imports_block}\n"
            "shared_context_schemas: {}\n"
        ),
        encoding="utf-8",
    )
    for filename, content in fragments.items():
        (root / filename).write_text(dedent(content), encoding="utf-8")
    return root / "index.yaml"


def _valid_fragment(
    *,
    module: str,
    code: str,
    type_slug: str,
    context_schema: str,
    example_context: str,
) -> str:
    return (
        f"module: {module}\n"
        "errors:\n"
        f"  {code}:\n"
        f"    code: {code}\n"
        f"    type_slug: {type_slug}\n"
        "    http_status: 409\n"
        "    title: Jolly already used\n"
        "    category: business_rule\n"
        "    retry_policy: never\n"
        "    safe_to_expose: true\n"
        "    context_schema:\n"
        f"{indent(dedent(context_schema).strip(), '      ')}\n"
        "    example:\n"
        "      context:\n"
        f"{indent(dedent(example_context).strip(), '        ')}\n"
    )


def test_catalog_validation_error_stores_issues() -> None:
    """The catalog validation exception should preserve the collected issues."""
    issues = [CatalogValidationIssue(location="a", message="first")]

    error = CatalogValidationError(issues)

    assert error.issues == tuple(issues)
    assert "a: first" in str(error)


def test_validate_split_catalog_semantics_accepts_valid_layout(tmp_path: Path) -> None:
    """A valid split catalog should pass validator-level semantics."""
    index_path = _write_catalog(
        tmp_path,
        index_imports=["event_operations.yaml"],
        fragments={
            "event_operations.yaml": _valid_fragment(
                module="event_operations",
                code="JOLLY_ALREADY_USED",
                type_slug="jolly-already-used",
                context_schema="""\
type: object
additionalProperties: false
properties:
  team_id:
    type: string
required:
  - team_id
""",
                example_context="""\
team_id: team-001
""",
            ),
        },
    )

    catalog = load_error_catalog(index_path)

    assert catalog.module_names == ("event_operations",)
    assert tuple(catalog.errors) == ("JOLLY_ALREADY_USED",)


def test_validate_import_alignment_rejects_nested_fragment_paths(tmp_path: Path) -> None:
    """Imported fragments should stay on the supported flat path layout."""
    issues: list[CatalogValidationIssue] = []

    validate_import_alignment(
        ["nested/event_operations.yaml"],
        catalog_path=tmp_path / "contracts" / "errors" / "index.yaml",
        issues=issues,
    )

    assert issues
    assert "docs/api/errors/<module>.yaml" in issues[0].message


def test_normalize_context_schema_closes_objects_by_default() -> None:
    """Object-shaped context schemas should default to closed objects."""
    normalized = normalize_context_schema(
        {
            "type": "object",
            "properties": {
                "team_id": {
                    "type": "string",
                }
            },
        }
    )

    assert normalized["additionalProperties"] is False


def test_resolve_context_schema_references_inlines_shared_schemas() -> None:
    """Shared context-schema references should be resolved recursively."""
    resolved = resolve_context_schema_references(
        {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "team_id": {"$ref": "#/shared_context_schemas/UuidRef"}
            },
            "required": ["team_id"],
        },
        shared_context_schemas={
            "UuidRef": {
                "type": "string",
                "format": "uuid",
            }
        },
    )

    assert resolved["properties"]["team_id"] == {
        "type": "string",
        "format": "uuid",
    }


def test_validate_context_references_rejects_unknown_shared_refs() -> None:
    """Unknown shared-schema references should be reported as validation errors."""
    issues: list[CatalogValidationIssue] = []

    validate_context_references(
        {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "team_id": {"$ref": "#/shared_context_schemas/MissingRef"}
            },
        },
        shared_context_schemas={},
        fragment_path=Path("docs/api/errors/event_operations.yaml"),
        code="JOLLY_ALREADY_USED",
        issues=issues,
    )

    assert issues
    assert "Unknown shared context schema reference" in issues[0].message


def test_validate_duplicate_code_across_modules_fails(tmp_path: Path) -> None:
    """Duplicate symbolic codes across modules should fail validation."""
    index_path = _write_catalog(
        tmp_path,
        index_imports=["event_operations.yaml", "users.yaml"],
        fragments={
            "event_operations.yaml": _valid_fragment(
                module="event_operations",
                code="DUPLICATE_CODE",
                type_slug="event-duplicate",
                context_schema="""\
type: object
additionalProperties: false
properties:
  team_id:
    type: string
required:
  - team_id
""",
                example_context="""\
team_id: team-001
""",
            ),
            "users.yaml": _valid_fragment(
                module="users",
                code="DUPLICATE_CODE",
                type_slug="users-duplicate",
                context_schema="""\
type: object
additionalProperties: false
properties:
  user_id:
    type: string
required:
  - user_id
""",
                example_context="""\
user_id: user-001
""",
            ),
        },
    )

    with pytest.raises(CatalogValidationError, match="Duplicate symbolic error code"):
        load_error_catalog(index_path)


def test_validate_duplicate_type_slug_across_modules_fails(tmp_path: Path) -> None:
    """Duplicate `type_slug` values across modules should fail validation."""
    index_path = _write_catalog(
        tmp_path,
        index_imports=["event_operations.yaml", "users.yaml"],
        fragments={
            "event_operations.yaml": _valid_fragment(
                module="event_operations",
                code="EVENT_DUPLICATE",
                type_slug="shared-type",
                context_schema="""\
type: object
additionalProperties: false
properties:
  team_id:
    type: string
required:
  - team_id
""",
                example_context="""\
team_id: team-001
""",
            ),
            "users.yaml": _valid_fragment(
                module="users",
                code="USERS_DUPLICATE",
                type_slug="shared-type",
                context_schema="""\
type: object
additionalProperties: false
properties:
  user_id:
    type: string
required:
  - user_id
""",
                example_context="""\
user_id: user-001
""",
            ),
        },
    )

    with pytest.raises(CatalogValidationError, match="Duplicate `type_slug`"):
        load_error_catalog(index_path)


def test_validate_example_context_satisfies_context_schema() -> None:
    """A valid example context should satisfy the declared context schema."""
    issues: list[CatalogValidationIssue] = []

    validate_example_context(
        code="JOLLY_ALREADY_USED",
        fragment_path=Path("docs/api/errors/event_operations.yaml"),
        normalized_context_schema={
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "team_id": {"type": "string"},
            },
            "required": ["team_id"],
        },
        shared_context_schemas={},
        example={"context": {"team_id": "team-001"}},
        issues=issues,
    )

    assert issues == []


def test_validate_example_context_reports_missing_required_fields() -> None:
    """Examples should be checked against required context fields."""
    issues: list[CatalogValidationIssue] = []

    validate_example_context(
        code="JOLLY_ALREADY_USED",
        fragment_path=Path("docs/api/errors/event_operations.yaml"),
        normalized_context_schema={
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "team_id": {"type": "string"},
            },
            "required": ["team_id"],
        },
        shared_context_schemas={},
        example={"context": {}},
        issues=issues,
    )

    assert issues
    assert "team_id" in issues[0].message


def test_validate_example_context_reports_extra_context_fields() -> None:
    """Examples should reject context keys that are not exposed by the schema."""
    issues: list[CatalogValidationIssue] = []

    validate_example_context(
        code="JOLLY_ALREADY_USED",
        fragment_path=Path("docs/api/errors/event_operations.yaml"),
        normalized_context_schema={
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "team_id": {"type": "string"},
            },
            "required": ["team_id"],
        },
        shared_context_schemas={},
        example={"context": {"team_id": "team-001", "unexpected": "boom"}},
        issues=issues,
    )

    assert issues
    assert "unexpected" in issues[0].message
