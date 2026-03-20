"""Enforce model-level parsing and field rules for catalog models.

This file should cover:
- required fields
- field validation
- model parsing shape

It should not enforce cross-file semantics, generator output, CLI behavior, or API runtime behavior.
"""

import dataclasses
import importlib
from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError


def _import_models_module() -> Any:
    """Import the tool models module using the repo-style path first."""
    candidates = ["tools.error_codegen.models", "error_codegen.models"]
    last_error: Exception | None = None
    for name in candidates:
        try:
            return importlib.import_module(name)
        except Exception as error:  # pragma: no cover - actionable failure path
            last_error = error
    raise AssertionError(
        f"Unable to import the models module. Last error: {last_error}"
    )


def _resolve_attr(module: Any, candidates: list[str]) -> Any:
    """Resolve the first available attribute from a module."""
    for name in candidates:
        if hasattr(module, name):
            return getattr(module, name)
    raise AssertionError(f"Expected one of {candidates!r} in {module.__name__}.")


def _minimal_model_payload(model_cls: Any) -> dict[str, object]:
    """Build a best-effort minimal payload for a pydantic document model."""
    payload: dict[str, object] = {}
    for field_name in model_cls.model_fields:
        if field_name in {"catalog_version"}:
            payload[field_name] = 1
        elif field_name in {"namespace"}:
            payload[field_name] = "palioboard"
        elif field_name in {"base_type_uri"}:
            payload[field_name] = "https://api.palioboard.local/problems/"
        elif field_name in {"schema_dialect"}:
            payload[field_name] = "https://json-schema.org/draft/2020-12/schema"
        elif field_name in {"default_media_type"}:
            payload[field_name] = "application/problem+json"
        elif field_name in {"includes", "imports"}:
            payload[field_name] = ["event_operations.yaml"]
        elif field_name in {"shared_context_schemas"}:
            payload[field_name] = {}
        elif field_name in {"errors"}:
            payload[field_name] = {}
        elif field_name in {"type_slug"}:
            payload[field_name] = "jolly-already-used"
        elif field_name in {"http_status", "recommended_http_status"}:
            payload[field_name] = 409
        elif field_name in {"title"}:
            payload[field_name] = "Jolly already used"
        elif field_name in {"description"}:
            payload[field_name] = None
        elif field_name in {"category"}:
            payload[field_name] = "business_rule"
        elif field_name in {"retry_policy"}:
            payload[field_name] = "never"
        elif field_name in {"safe_to_expose"}:
            payload[field_name] = True
        elif field_name in {"translation_key"}:
            payload[field_name] = "errors.jollyAlreadyUsed"
        elif field_name in {"translation_key_override"}:
            payload[field_name] = None
        elif field_name in {"type_uri_override"}:
            payload[field_name] = None
        elif field_name in {"context_schema"}:
            payload[field_name] = {
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            }
        elif field_name in {"log_level", "severity", "notes_for_operators"}:
            payload[field_name] = None
        elif field_name in {"example"}:
            payload[field_name] = {"context": {}}
        elif field_name in {"module_name"}:
            payload[field_name] = "event_operations"
        elif field_name in {"source_path", "catalog_path", "schema_path"}:
            payload[field_name] = Path("/tmp/catalog.yaml")
        elif field_name in {"code"}:
            payload[field_name] = "JOLLY_ALREADY_USED"
        elif field_name in {"type_uri"}:
            payload[field_name] = (
                "https://api.palioboard.local/problems/jolly-already-used"
            )
        elif field_name in {"raw_context_schema", "normalized_context_schema"}:
            payload[field_name] = {
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            }
        elif field_name in {"shared_context_schemas"}:
            payload[field_name] = {}
        elif field_name in {"fragments"}:
            payload[field_name] = ()
        elif field_name in {"errors"}:
            payload[field_name] = {}
        else:
            # Leave fields with defaults unset; for truly new required fields, fail loudly.
            pass
    return payload


def test_catalog_validation_issue_is_a_frozen_dataclass() -> None:
    """Validation issue objects should be immutable and preserve location/message."""
    models = _import_models_module()
    issue_cls = _resolve_attr(models, ["CatalogValidationIssue"])

    issue = issue_cls(location="catalog.index", message="duplicate code")

    assert dataclasses.is_dataclass(issue)
    assert issue.location == "catalog.index"
    assert issue.message == "duplicate code"

    with pytest.raises(dataclasses.FrozenInstanceError):
        issue.location = "other"  # type: ignore[misc]


def test_error_entry_document_forbids_unknown_fields() -> None:
    """The authored error-entry model should reject stray keys."""
    models = _import_models_module()
    document_cls = _resolve_attr(models, ["ErrorEntryDocument"])

    payload = _minimal_model_payload(document_cls)
    payload["unexpected"] = "boom"

    with pytest.raises(ValidationError):
        document_cls(**payload)


def test_root_catalog_document_accepts_minimal_split_catalog_payload() -> None:
    """The root index model should accept the minimal split-catalog shape."""
    models = _import_models_module()
    root_cls = _resolve_attr(models, ["RootCatalogDocument"])

    payload = _minimal_model_payload(root_cls)
    document = root_cls(**payload)

    assert getattr(document, "namespace") == "palioboard"
    assert str(getattr(document, "base_type_uri")).startswith(
        "https://api.palioboard.local/problems/"
    )


def test_error_catalog_entry_exposes_transport_metadata() -> None:
    """The validated entry model should keep the core transport metadata accessible."""
    models = _import_models_module()
    entry_cls = _resolve_attr(models, ["ErrorCatalogEntry"])

    payload = _minimal_model_payload(entry_cls)
    entry = entry_cls(**payload)

    assert getattr(entry, "code") == "JOLLY_ALREADY_USED"
    assert getattr(entry, "type_slug") == "jolly-already-used"
    status = getattr(
        entry, "http_status", getattr(entry, "recommended_http_status", None)
    )
    assert status == 409
