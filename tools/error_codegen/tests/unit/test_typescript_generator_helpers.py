"""Enforce TypeScript generator helper behavior for the target architecture.

This file should only cover the frontend metadata contract:
- exported catalog entries contain `code`, `typeUri`, `title`, `httpStatus`,
  and `translationKey`
- context keys are exposed for interpolation in authored order
- nested fields are preserved without accidental flattening unless intentional

It should use the shared pure helpers from `support.text_helpers` instead of
duplicating token/block extraction locally. It should not enforce exact
full-file formatting, CLI behavior, or API runtime behavior.
"""

from types import SimpleNamespace

from error_codegen.generators.typescript import (
    _context_alias_name,
    _render_literal,
    _render_schema_type,
    _shared_context_alias_name,
    generate_typescript_error_artifact,
)
from support.sample_catalog import build_sample_catalog
from support.text_helpers import assert_tokens_in_order, extract_balanced_block


def test_render_literal_handles_scalar_values() -> None:
    """Literal rendering should preserve TypeScript-compatible scalars."""
    assert _render_literal("abc") == '"abc"'
    assert _render_literal(True) == "true"
    assert _render_literal(False) == "false"
    assert _render_literal(None) == "null"
    assert _render_literal(7) == "7"


def test_alias_name_helpers_generate_stable_context_type_names() -> None:
    """Alias helpers should derive stable exported type names."""
    assert _shared_context_alias_name("uuid_ref") == "SharedContextUuidRef"
    assert _context_alias_name("JOLLY_ALREADY_USED") == "JollyAlreadyUsedContext"


def test_render_schema_type_preserves_nested_object_fields() -> None:
    """Schema rendering should preserve nested object structure and field order."""
    schema = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "game_id": {"type": "string"},
            "existing_result": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "team_id": {"type": "string"},
                    "placement": {"type": "number"},
                },
                "required": ["team_id"],
            },
            "incoming_result": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "team_id": {"type": "string"},
                    "placement": {"type": "number"},
                },
                "required": ["team_id"],
            },
        },
        "required": ["game_id", "existing_result", "incoming_result"],
    }

    rendered = _render_schema_type(schema, {}, path=())

    assert_tokens_in_order(
        rendered,
        [
            '"game_id": string;',
            '"existing_result": {',
            '"team_id": string;',
            '"placement": number;',
            '"incoming_result": {',
        ],
    )
    assert "existing_result_team_id" not in rendered
    assert "incoming_result_team_id" not in rendered


def test_generate_typescript_artifact_exports_catalog_metadata_contract() -> None:
    """Generated TS should expose the frontend catalog contract and metadata keys."""
    rendered = generate_typescript_error_artifact(build_sample_catalog())

    assert "export type ApiErrorCatalogEntry = {" in rendered
    api_entry_block = extract_balanced_block(
        rendered, "export type ApiErrorCatalogEntry ="
    )
    assert_tokens_in_order(
        api_entry_block,
        [
            "code: string;",
            "typeUri: string;",
            "title: string;",
            "httpStatus: number;",
            "translationKey: string;",
        ],
    )
    assert "ERROR_METADATA_BY_CODE" not in rendered
    assert "ERROR_CODES_BY_MODULE" not in rendered
    assert "ERROR_CATALOG_MODULES" not in rendered
    assert "export const ERROR_CATALOG = {" in rendered
    assert "export type ErrorCode = keyof typeof ERROR_CATALOG;" in rendered


def test_generate_typescript_artifact_exposes_context_keys_for_interpolation() -> None:
    """Generated TS should keep context keys visible in authored order."""
    catalog = build_sample_catalog()
    rendered = generate_typescript_error_artifact(catalog)
    sample_entry = catalog.errors["JOLLY_ALREADY_USED"]
    context_block = extract_balanced_block(
        rendered, "export type JollyAlreadyUsedContext ="
    )

    assert_tokens_in_order(
        context_block,
        [
            '"team_id": SharedContextUuidRef;',
            '"game_id": SharedContextUuidRef;',
            '"previous_game_id"?: SharedContextUuidRef;',
        ],
    )
    assert "export interface ErrorContextByCode {" in rendered
    assert (
        "export type ErrorContext<TCode extends ErrorCode> = "
        "ErrorContextByCode[TCode];" in rendered
    )
    for field_name in sample_entry.resolved_context_schema["properties"]:
        assert field_name in context_block


def test_generate_typescript_artifact_does_not_flatten_nested_fields_incorrectly() -> (
    None
):
    """Generated TS should keep nested object structure intact in the artifact."""
    nested_schema = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "game_id": {"type": "string"},
            "existing_result": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "team_id": {"type": "string"},
                    "placement": {"type": "number"},
                },
                "required": ["team_id", "placement"],
            },
        },
        "required": ["game_id", "existing_result"],
    }
    entry = SimpleNamespace(
        module_name="event_operations",
        code="PLACEMENT_CONFLICT",
        type_uri="https://api.palioboard.local/problems/placement-conflict",
        http_status=409,
        title="Placement conflict",
        category="business_rule",
        retry_policy="never",
        safe_to_expose=True,
        translation_key="errors.placementConflict",
        normalized_context_schema=nested_schema,
        description=None,
        log_level=None,
        severity=None,
    )
    catalog = SimpleNamespace(
        module_names=("event_operations",),
        shared_context_schemas={},
        errors_for_module=lambda module_name: (
            (entry,) if module_name == "event_operations" else ()
        ),
    )

    rendered = generate_typescript_error_artifact(catalog)
    context_block = extract_balanced_block(
        rendered, "export type PlacementConflictContext ="
    )

    assert_tokens_in_order(
        context_block,
        [
            '"game_id": string;',
            '"existing_result": {',
            '"team_id": string;',
            '"placement": number;',
        ],
    )
    assert "existing_result_team_id" not in context_block
    assert "existing_result_placement" not in context_block
