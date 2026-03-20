"""Enforce TypeScript generation invariants across valid scenarios.

This file should eventually enforce the frontend contract only:
- exported catalog metadata includes `code`, `typeUri`, `title`, `httpStatus`,
  and `translationKey`
- context keys are listed for frontend interpolation in authored order
- nested fields are preserved instead of flattened unless intentionally designed
- rendering is deterministic

It should not enforce exact formatting, API runtime behavior, or backend
generation details that belong to the Python domain-error tests.
"""

from pathlib import Path

import pytest

from error_codegen.generators.typescript import _context_alias_name
from support.adapters import load_catalog, render_typescript_artifact
from support.expectations import collect_raw_error_entries
from support.scenarios import Scenario, success_scenarios

SCENARIOS_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "scenarios"
SUCCESS_SCENARIOS = [
    pytest.param(scenario, id=scenario.id)
    for scenario in success_scenarios(SCENARIOS_ROOT)
]


def _extract_balanced_block(source: str, start_marker: str) -> str:
    """Return the balanced block that starts at ``start_marker``."""
    start = source.index(start_marker)
    brace_start = source.index("{", start)

    depth = 0
    for index in range(brace_start, len(source)):
        character = source[index]
        if character == "{":
            depth += 1
        elif character == "}":
            depth -= 1
            if depth == 0:
                return source[start : index + 1]

    raise AssertionError(f"Unbalanced block starting at {start_marker!r}.")


def _assert_in_order(source: str, tokens: list[str]) -> None:
    """Assert that all tokens appear in the given order."""
    cursor = -1
    for token in tokens:
        position = source.index(token)
        assert position > cursor, token
        cursor = position


def _schema_paths(
    schema: object,
    *,
    prefix: tuple[str, ...] = (),
) -> list[tuple[str, ...]]:
    """Return ordered schema paths, including nested object fields."""
    if not isinstance(schema, dict):
        return []

    paths: list[tuple[str, ...]] = []
    properties = schema.get("properties")
    if not isinstance(properties, dict):
        return paths

    for name, child in properties.items():
        if not isinstance(name, str):
            continue
        path = (*prefix, name)
        paths.append(path)
        paths.extend(_schema_paths(child, prefix=path))
    return paths


@pytest.mark.parametrize("scenario", SUCCESS_SCENARIOS)
def test_typescript_generation_exports_catalog_metadata_contract(
    scenario: Scenario,
) -> None:
    """Generated TS should expose the target frontend catalog contract."""
    catalog = load_catalog(scenario.index_path)
    rendered = render_typescript_artifact(catalog)
    entries = collect_raw_error_entries(scenario.index_path)

    assert "export type ApiErrorCatalogEntry = {" in rendered
    assert "export const ERROR_CATALOG = {" in rendered
    assert "export type ErrorCode = keyof typeof ERROR_CATALOG;" in rendered
    assert "ERROR_METADATA_BY_CODE" not in rendered
    assert "ERROR_CODES_BY_MODULE" not in rendered
    assert "ERROR_CATALOG_MODULES" not in rendered

    api_entry_block = _extract_balanced_block(
        rendered, "export type ApiErrorCatalogEntry ="
    )
    _assert_in_order(
        api_entry_block,
        [
            "code: string;",
            "typeUri: string;",
            "title: string;",
            "httpStatus: number;",
            "translationKey: string;",
        ],
    )

    for entry in entries:
        entry_block = _extract_balanced_block(rendered, f"  {entry.code}: {{")
        _assert_in_order(
            entry_block,
            [
                f'code: "{entry.code}"',
                f'typeUri: "{entry.type_uri}"',
                f'title: "{entry.title}"',
                f"httpStatus: {entry.http_status}",
                f'translationKey: "{entry.translation_key}"',
            ],
        )
        assert "moduleName" not in entry_block
        assert "category" not in entry_block
        assert "retryPolicy" not in entry_block
        assert "safeToExpose" not in entry_block
        assert "contextSchema" not in entry_block


@pytest.mark.parametrize("scenario", SUCCESS_SCENARIOS)
def test_typescript_generation_exposes_context_keys_for_interpolation(
    scenario: Scenario,
) -> None:
    """Generated TS should keep context keys visible in authored order."""
    catalog = load_catalog(scenario.index_path)
    rendered = render_typescript_artifact(catalog)
    entries = collect_raw_error_entries(scenario.index_path)

    assert "export interface ErrorContextByCode {" in rendered
    assert (
        "export type ErrorContext<TCode extends ErrorCode> = "
        "ErrorContextByCode[TCode];"
        in rendered
    )

    for entry in entries:
        alias_name = _context_alias_name(entry.code)
        context_block = _extract_balanced_block(rendered, f"export type {alias_name} =")
        schema_paths = _schema_paths(entry.context_schema)
        flattened_paths = ["_".join(path) for path in schema_paths if len(path) > 1]

        for path in schema_paths:
            assert path[-1] in context_block

        for path in flattened_paths:
            assert path not in context_block

        top_level_paths = [path for path in schema_paths if len(path) == 1]
        _assert_in_order(context_block, [path[0] for path in top_level_paths])


@pytest.mark.parametrize("scenario", SUCCESS_SCENARIOS)
def test_typescript_generation_is_deterministic_across_runs(
    scenario: Scenario,
) -> None:
    """Rendering the same catalog twice should produce identical TypeScript."""
    catalog_one = load_catalog(scenario.index_path)
    catalog_two = load_catalog(scenario.index_path)

    first = render_typescript_artifact(catalog_one)
    second = render_typescript_artifact(catalog_two)
    assert first == second
