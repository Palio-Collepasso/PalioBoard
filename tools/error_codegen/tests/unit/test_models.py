"""Enforce model-contract rules for catalog parsing and field validation.

This file should cover:
- invalid code shape rejected at the model boundary
- invalid `type_slug` rejected at the model boundary
- invalid `http_status` rejected at the model boundary
- unknown fields rejected
- minimal split-catalog root shape accepted
- transport metadata exposed on validated entries

It should not enforce semantic cross-file rules, generator output, CLI behavior,
or API runtime behavior.
"""

import dataclasses
from pathlib import Path

import pytest
from pydantic import ValidationError

from error_codegen.models import (
    CatalogValidationIssue,
    ErrorCatalogEntry,
    ErrorEntryDocument,
    RootCatalogDocument,
)


def _valid_entry_payload(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "code": "JOLLY_ALREADY_USED",
        "module_name": "event_operations",
        "source_path": Path("docs/api/errors/event_operations.yaml"),
        "type_slug": "jolly-already-used",
        "type_uri": "https://api.palioboard.local/problems/jolly-already-used",
        "http_status": 409,
        "title": "Jolly already used",
        "description": "The selected team has already consumed its Jolly.",
        "category": "business_rule",
        "retry_policy": "never",
        "safe_to_expose": True,
        "translation_key": "errors.jollyAlreadyUsed",
        "raw_context_schema": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "team_id": {"type": "string"},
            },
            "required": ["team_id"],
        },
        "normalized_context_schema": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "team_id": {"type": "string"},
            },
            "required": ["team_id"],
        },
        "resolved_context_schema": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "team_id": {"type": "string"},
            },
            "required": ["team_id"],
        },
        "type_uri_override": None,
        "translation_key_override": None,
        "log_level": None,
        "severity": None,
        "example": {"context": {"team_id": "team-001"}},
        "notes_for_operators": None,
    }
    payload.update(overrides)
    return payload


def test_catalog_validation_issue_is_a_frozen_dataclass() -> None:
    """Validation issues should remain immutable and carry location/message."""
    issue = CatalogValidationIssue(location="catalog.index", message="duplicate")

    assert issue.location == "catalog.index"
    assert issue.message == "duplicate"

    with pytest.raises(dataclasses.FrozenInstanceError):
        issue.location = "other"  # type: ignore[misc]


def test_error_catalog_entry_rejects_invalid_code_shape() -> None:
    """Validated catalog entries should reject invalid symbolic codes."""
    with pytest.raises(ValidationError, match="UPPER_SNAKE_CASE"):
        ErrorCatalogEntry(**_valid_entry_payload(code="bad-code"))


def test_error_entry_document_rejects_invalid_type_slug() -> None:
    """Authored error-entry models should reject invalid `type_slug` values."""
    with pytest.raises(ValidationError, match="kebab-case"):
        ErrorEntryDocument(
            type_slug="Bad-Slug",
            http_status=409,
            title="Jolly already used",
            description=None,
            category="business_rule",
            retry_policy="never",
            safe_to_expose=True,
            translation_key_override=None,
            context_schema={
                "type": "object",
                "additionalProperties": False,
                "properties": {},
            },
            log_level=None,
            severity=None,
            example=None,
            notes_for_operators=None,
        )


def test_error_entry_document_rejects_invalid_http_status() -> None:
    """Authored error-entry models should reject non-error HTTP status values."""
    with pytest.raises(ValidationError, match="between 400 and 599"):
        ErrorEntryDocument(
            type_slug="jolly-already-used",
            http_status=399,
            title="Jolly already used",
            description=None,
            category="business_rule",
            retry_policy="never",
            safe_to_expose=True,
            translation_key_override=None,
            context_schema={
                "type": "object",
                "additionalProperties": False,
                "properties": {},
            },
            log_level=None,
            severity=None,
            example=None,
            notes_for_operators=None,
        )


def test_error_entry_document_rejects_unknown_fields() -> None:
    """Authored error-entry models should reject stray keys."""
    with pytest.raises(ValidationError):
        ErrorEntryDocument(
            type_slug="jolly-already-used",
            http_status=409,
            title="Jolly already used",
            description=None,
            category="business_rule",
            retry_policy="never",
            safe_to_expose=True,
            translation_key_override=None,
            context_schema={
                "type": "object",
                "additionalProperties": False,
                "properties": {},
            },
            log_level=None,
            severity=None,
            example=None,
            notes_for_operators=None,
            unexpected="boom",  # type: ignore[arg-type]
        )


def test_error_entry_document_rejects_translation_override_for_hidden_error() -> None:
    """Non-exposed authored errors should not carry a translation override."""
    with pytest.raises(ValidationError, match="must not declare"):
        ErrorEntryDocument(
            type_slug="jolly-already-used",
            http_status=409,
            title="Jolly already used",
            description=None,
            category="business_rule",
            retry_policy="never",
            safe_to_expose=False,
            translation_key_override="errors.jollyAlreadyUsed",
            context_schema={
                "type": "object",
                "additionalProperties": False,
                "properties": {},
            },
            log_level=None,
            severity=None,
            example=None,
            notes_for_operators=None,
        )


def test_root_catalog_document_accepts_minimal_split_catalog_payload() -> None:
    """The root index model should accept the minimal split-catalog shape."""
    document = RootCatalogDocument(
        catalog_version=1,
        namespace="palioboard",
        base_type_uri="https://api.palioboard.local/problems/",
        schema_dialect="https://json-schema.org/draft/2020-12/schema",
        default_media_type="application/problem+json",
        imports=["event_operations.yaml"],
        shared_context_schemas={},
        errors={},
    )

    assert document.namespace == "palioboard"
    assert str(document.base_type_uri).endswith("/problems/")


def test_error_catalog_entry_exposes_transport_metadata() -> None:
    """Validated entries should expose core transport metadata for later use."""
    entry = ErrorCatalogEntry(**_valid_entry_payload())

    assert entry.code == "JOLLY_ALREADY_USED"
    assert entry.type_slug == "jolly-already-used"
    assert entry.http_status == 409
    assert entry.type_uri == "https://api.palioboard.local/problems/jolly-already-used"
    assert entry.translation_key == "errors.jollyAlreadyUsed"
