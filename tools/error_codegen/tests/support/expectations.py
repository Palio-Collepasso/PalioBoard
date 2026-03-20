"""Expectation helpers for tool-side catalog and generator tests.

Keep this module focused on catalog loading, scenario-derived expectations, and
generator assertions. API runtime helpers belong in API test support.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True, slots=True)
class RawErrorEntry:
    """One raw error entry parsed directly from a scenario catalog."""

    module: str
    code: str
    type_slug: str
    http_status: int
    title: str
    translation_key: str | None
    context_schema: dict[str, object] | None
    example_context: dict[str, object] | None


@dataclass(frozen=True, slots=True)
class RawContextExpectation:
    """Expected context fields for one error code."""

    required: tuple[str, ...]
    optional: tuple[str, ...]


def read_yaml(path: Path) -> dict[str, Any]:
    """Read one YAML document from disk."""
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise AssertionError(
            f"Expected mapping at {path}, got {type(payload).__name__}."
        )
    return payload


def collect_raw_error_entries(index_path: Path) -> list[RawErrorEntry]:
    """Collect raw error metadata from a split catalog rooted at ``index.yaml``."""
    index_document = read_yaml(index_path)
    base_dir = index_path.parent
    include_key = "includes" if "includes" in index_document else "imports"

    entries: list[RawErrorEntry] = []
    for include_path in index_document.get(include_key, []):
        module_document = read_yaml(base_dir / include_path)
        module_name = str(module_document.get("module") or Path(include_path).stem)
        for key, payload in module_document.get("errors", {}).items():
            if not isinstance(payload, dict):
                raise AssertionError(
                    f"Expected mapping for error {key!r} in {include_path}."
                )
            entries.append(
                RawErrorEntry(
                    module=module_name,
                    code=str(payload.get("code", key)),
                    type_slug=str(payload["type_slug"]),
                    http_status=int(payload["http_status"]),
                    title=str(payload["title"]),
                    translation_key=(
                        str(payload["translation_key"])
                        if payload.get("translation_key") is not None
                        else None
                    ),
                    context_schema=(
                        payload["context_schema"]
                        if isinstance(payload.get("context_schema"), dict)
                        else None
                    ),
                    example_context=(
                        payload["example_context"]
                        if isinstance(payload.get("example_context"), dict)
                        else None
                    ),
                )
            )
    return entries


def expected_failure_markers(scenario_name: str) -> list[str]:
    """Return stable message fragments expected for a known failure scenario."""
    markers_by_scenario = {
        "invalid_code_format": ["code", "UPPER_SNAKE_CASE"],
        "invalid_http_status": ["http_status", "400", "599"],
        "invalid_type_slug": ["type_slug", "kebab"],
        "example_missing_required_context": ["example_context", "required"],
        "example_has_extra_context": ["example_context", "additional"],
        "duplicate_code_across_modules": ["duplicate", "code"],
        "duplicate_type_slug_across_modules": ["duplicate", "type_slug"],
        "invalid_nested_context_example": ["example_context", "context_schema"],
        "key_mismatch_and_missing_translation_key": ["translation_key", "code"],
        "combined_catalog_conflicts": ["duplicate", "translation_key", "type_slug"],
        "split_catalog_multiple_cross_file_collisions": [
            "duplicate",
            "code",
            "type_slug",
        ],
        "doc_injection_missing_heading": ["heading", "documentation"],
    }
    return markers_by_scenario.get(scenario_name, ["catalog"])


def expected_runtime_payloads(index_path: Path) -> list[dict[str, Any]]:
    """Build expected runtime Problem Details payloads from raw catalog entries.

    Temporary compatibility helper. The final runtime assertions should move to
    API test support and stop depending on tool-owned expectations.
    """
    try:
        index_document = read_yaml(index_path)
        base_type_uri = str(index_document["base_type_uri"]).rstrip("/") + "/"

        payloads: list[dict[str, Any]] = []
        for entry in collect_raw_error_entries(index_path):
            payloads.append(
                {
                    "type": f"{base_type_uri}{entry.type_slug}",
                    "code": entry.code,
                    "title": entry.title,
                    "status": entry.http_status,
                    "context": entry.example_context or {},
                }
            )
        return payloads
    except Exception:
        from support.adapters import load_catalog

        try:
            catalog = load_catalog(index_path)
        except Exception:
            return []
        payloads: list[dict[str, Any]] = []
        for entry in catalog.errors.values():
            example = entry.example if isinstance(entry.example, dict) else {}
            context = example.get("context", {}) if isinstance(example, dict) else {}
            payloads.append(
                {
                    "type": entry.type_uri,
                    "code": entry.code,
                    "title": entry.title,
                    "status": entry.http_status,
                    "context": context if isinstance(context, dict) else {},
                }
            )
        return payloads


def expected_codes_by_module(index_path: Path) -> dict[str, tuple[str, ...]]:
    """Return expected symbolic codes grouped by owning module."""
    grouped: dict[str, list[str]] = {}
    for entry in collect_raw_error_entries(index_path):
        grouped.setdefault(entry.module, []).append(entry.code)
    return {module: tuple(sorted(codes)) for module, codes in sorted(grouped.items())}


def expected_translation_keys(index_path: Path) -> dict[str, str]:
    """Return translation keys for all raw errors that expose one."""
    pairs = {
        entry.code: entry.translation_key
        for entry in collect_raw_error_entries(index_path)
        if entry.translation_key is not None
    }
    return dict(sorted(pairs.items()))


def expected_context_fields_by_code(
    index_path: Path,
) -> dict[str, RawContextExpectation]:
    """Return required and optional context fields per code."""
    expectations: dict[str, RawContextExpectation] = {}
    for entry in collect_raw_error_entries(index_path):
        schema = entry.context_schema or {}
        properties = schema.get("properties", {}) if isinstance(schema, dict) else {}
        required = schema.get("required", []) if isinstance(schema, dict) else []
        required_names = tuple(
            sorted(name for name in required if isinstance(name, str))
        )
        optional_names = tuple(
            sorted(
                name
                for name in properties
                if isinstance(name, str) and name not in required_names
            )
        )
        expectations[entry.code] = RawContextExpectation(
            required=required_names,
            optional=optional_names,
        )
    return dict(sorted(expectations.items()))


def generated_python_expectations(index_path: Path) -> dict[str, list[RawErrorEntry]]:
    """Group raw error entries by module for Python generation assertions."""
    grouped: dict[str, list[RawErrorEntry]] = {}
    for entry in collect_raw_error_entries(index_path):
        grouped.setdefault(entry.module, []).append(entry)
    return grouped
