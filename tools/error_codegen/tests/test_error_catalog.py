from pathlib import Path

import pytest

from error_codegen import (
    CatalogValidationError,
    load_error_catalog,
    validate_error_catalog,
)
from support.error_catalog import fragment_with_error, write_catalog


def test_load_error_catalog_reads_module_aligned_fragments() -> None:
    catalog = load_error_catalog()

    assert catalog.module_names == (
        "audit",
        "authorization",
        "event_operations",
        "identity",
        "leaderboard_projection",
        "live_games",
        "public_read",
        "results",
        "season_setup",
        "tournaments",
        "users",
    )
    assert catalog.errors == {}
    assert catalog.fragments[2].module_name == "event_operations"
    assert catalog.fragments[2].source_path.name == "event_operations.yaml"
    assert "UuidRef" in catalog.shared_context_schemas


def test_validate_error_catalog_returns_summary_for_committed_catalog() -> None:
    summary = validate_error_catalog()

    assert summary == (
        "Validated 11 module fragments, 0 error entries, and 6 shared context schemas."
    )


def test_load_error_catalog_reports_missing_module_fragment(tmp_path: Path) -> None:
    catalog_path = write_catalog(
        tmp_path,
        imports=["users.yaml"],
        fragments={"users.yaml": "errors: {}\n"},
        include_all_modules=False,
    )

    with pytest.raises(CatalogValidationError) as error:
        load_error_catalog(catalog_path=catalog_path)

    assert "Missing catalog fragment import for backend module `audit`." in str(
        error.value
    )


def test_load_error_catalog_reports_duplicate_symbolic_code(tmp_path: Path) -> None:
    catalog_path = write_catalog(
        tmp_path,
        imports=["users.yaml", "identity.yaml"],
        fragments={
            "users.yaml": fragment_with_error(
                code="USER_MISSING",
                type_slug="user-missing",
            ),
            "identity.yaml": fragment_with_error(
                code="USER_MISSING",
                type_slug="identity-missing",
            ),
        },
        include_all_modules=False,
    )

    with pytest.raises(CatalogValidationError) as error:
        load_error_catalog(catalog_path=catalog_path)

    assert "Duplicate symbolic error code" in str(error.value)


def test_load_error_catalog_reports_duplicate_type_slug(tmp_path: Path) -> None:
    catalog_path = write_catalog(
        tmp_path,
        imports=["users.yaml", "identity.yaml"],
        fragments={
            "users.yaml": fragment_with_error(
                code="USER_MISSING",
                type_slug="shared-slug",
            ),
            "identity.yaml": fragment_with_error(
                code="IDENTITY_MISSING",
                type_slug="shared-slug",
            ),
        },
        include_all_modules=False,
    )

    with pytest.raises(CatalogValidationError) as error:
        load_error_catalog(catalog_path=catalog_path)

    assert "Duplicate `type_slug`" in str(error.value)


def test_load_error_catalog_reports_duplicate_problem_type_uri(tmp_path: Path) -> None:
    catalog_path = write_catalog(
        tmp_path,
        imports=["users.yaml", "identity.yaml"],
        fragments={
            "users.yaml": fragment_with_error(
                code="USER_MISSING",
                type_slug="users-missing",
                type_uri_override="https://example.test/problems/shared",
            ),
            "identity.yaml": fragment_with_error(
                code="IDENTITY_MISSING",
                type_slug="identity-missing",
                type_uri_override="https://example.test/problems/shared",
            ),
        },
        include_all_modules=False,
    )

    with pytest.raises(CatalogValidationError) as error:
        load_error_catalog(catalog_path=catalog_path)

    assert "Duplicate derived problem type URI" in str(error.value)


def test_load_error_catalog_reports_unknown_shared_context_reference(
    tmp_path: Path,
) -> None:
    catalog_path = write_catalog(
        tmp_path,
        imports=["users.yaml"],
        fragments={
            "users.yaml": """
errors:
  USER_MISSING:
    type_slug: user-missing
    http_status: 404
    title: User missing
    category: not_found
    retry_policy: never
    safe_to_expose: true
    context_schema:
      type: object
      properties:
        user_id:
          $ref: "#/shared_context_schemas/MissingRef"
          required: true
""".strip()
            + "\n"
        },
    )

    with pytest.raises(CatalogValidationError) as error:
        load_error_catalog(catalog_path=catalog_path)

    assert "Unknown shared context schema reference" in str(error.value)


def test_load_error_catalog_reports_invalid_example_context(tmp_path: Path) -> None:
    catalog_path = write_catalog(
        tmp_path,
        imports=["users.yaml"],
        fragments={
            "users.yaml": """
errors:
  USER_MISSING:
    type_slug: user-missing
    http_status: 404
    title: User missing
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
        user_id: "not-a-uuid"
""".strip()
            + "\n"
        },
    )

    with pytest.raises(CatalogValidationError) as error:
        load_error_catalog(catalog_path=catalog_path)

    assert "is not a 'uuid'" in str(error.value)


def test_load_error_catalog_reports_invalid_fragment_entry_without_crashing(
    tmp_path: Path,
) -> None:
    catalog_path = write_catalog(
        tmp_path,
        imports=["users.yaml"],
        fragments={
            "users.yaml": """
errors:
  USER_MISSING:
    type_slug: user-missing
    http_status: 404
    category: not_found
    retry_policy: never
    safe_to_expose: true
    context_schema:
      type: object
      properties: {}
""".strip()
            + "\n"
        },
    )

    with pytest.raises(CatalogValidationError) as error:
        load_error_catalog(catalog_path=catalog_path)

    assert "title" in str(error.value)


def test_load_error_catalog_normalizes_required_field_extension(tmp_path: Path) -> None:
    catalog_path = write_catalog(
        tmp_path,
        imports=["users.yaml"],
        fragments={
            "users.yaml": """
errors:
  USER_MISSING:
    type_slug: user-missing
    http_status: 404
    title: User missing
    category: not_found
    retry_policy: never
    safe_to_expose: true
    context_schema:
      type: object
      additionalProperties: false
      properties:
        user_id:
          type: string
          required: true
        reason:
          type: string
          required: false
""".strip()
            + "\n"
        },
    )

    catalog = load_error_catalog(catalog_path=catalog_path)
    entry = catalog.errors["USER_MISSING"]

    assert entry.module_name == "users"
    assert entry.normalized_context_schema == {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "user_id": {"type": "string"},
            "reason": {"type": "string"},
        },
        "required": ["user_id"],
    }


def test_load_error_catalog_defaults_context_objects_to_closed_shapes(
    tmp_path: Path,
) -> None:
    catalog_path = write_catalog(
        tmp_path,
        imports=["users.yaml"],
        fragments={
            "users.yaml": """
errors:
  USER_MISSING:
    type_slug: user-missing
    http_status: 404
    title: User missing
    category: not_found
    retry_policy: never
    safe_to_expose: true
    context_schema:
      type: object
      properties:
        user_id:
          type: string
          required: true
""".strip()
            + "\n"
        },
    )

    entry = load_error_catalog(catalog_path=catalog_path).errors["USER_MISSING"]

    assert entry.normalized_context_schema == {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "user_id": {"type": "string"},
        },
        "required": ["user_id"],
    }


def test_load_error_catalog_rejects_open_context_bags(tmp_path: Path) -> None:
    catalog_path = write_catalog(
        tmp_path,
        imports=["users.yaml"],
        fragments={
            "users.yaml": """
errors:
  USER_MISSING:
    type_slug: user-missing
    http_status: 404
    title: User missing
    category: not_found
    retry_policy: never
    safe_to_expose: true
    context_schema:
      type: object
      additionalProperties: true
      properties: {}
""".strip()
            + "\n"
        },
    )

    with pytest.raises(CatalogValidationError) as error:
        load_error_catalog(catalog_path=catalog_path)

    assert "must not use `additionalProperties: true`" in str(error.value)


def test_load_error_catalog_rejects_translation_override_for_hidden_errors(
    tmp_path: Path,
) -> None:
    catalog_path = write_catalog(
        tmp_path,
        imports=["users.yaml"],
        fragments={
            "users.yaml": """
errors:
  USER_MISSING:
    type_slug: user-missing
    http_status: 404
    title: User missing
    category: not_found
    retry_policy: never
    safe_to_expose: false
    translation_key_override: errors.userMissing
    context_schema:
      type: object
      properties: {}
""".strip()
            + "\n"
        },
    )

    with pytest.raises(CatalogValidationError) as error:
        load_error_catalog(catalog_path=catalog_path)

    assert "must not declare `translation_key_override`" in str(error.value)
