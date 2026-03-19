import pytest

from error_codegen.models import ErrorCatalogEntry, ErrorEntryDocument
from error_codegen.validators import (
    normalize_context_schema,
    resolve_context_schema_references,
)
from support.sample_catalog import sample_entry_kwargs


def test_normalize_context_schema_promotes_required_extension_and_closes_objects() -> (
    None
):
    normalized = normalize_context_schema(
        {
            "type": "object",
            "properties": {
                "team_id": {
                    "type": "string",
                    "required": True,
                },
                "reason": {
                    "type": "string",
                    "required": False,
                },
            },
        }
    )

    assert normalized == {
        "type": "object",
        "properties": {
            "team_id": {"type": "string"},
            "reason": {"type": "string"},
        },
        "additionalProperties": False,
        "required": ["team_id"],
    }


def test_resolve_context_schema_references_inlines_shared_schemas() -> None:
    resolved = resolve_context_schema_references(
        {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "team_id": {"$ref": "#/shared_context_schemas/UuidRef"},
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

    assert resolved == {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "team_id": {
                "type": "string",
                "format": "uuid",
            }
        },
        "required": ["team_id"],
    }


def test_error_catalog_entry_rejects_invalid_symbolic_code() -> None:
    with pytest.raises(ValueError, match="UPPER_SNAKE_CASE"):
        ErrorCatalogEntry(**sample_entry_kwargs(code="bad-code"))


def test_error_entry_document_rejects_translation_override_for_hidden_errors() -> None:
    with pytest.raises(ValueError, match="must not declare `translation_key_override`"):
        ErrorEntryDocument(
            type_slug="user-missing",
            http_status=404,
            title="User missing",
            category="not_found",
            retry_policy="never",
            safe_to_expose=False,
            translation_key_override="errors.userMissing",
            context_schema={
                "type": "object",
                "properties": {},
            },
        )
