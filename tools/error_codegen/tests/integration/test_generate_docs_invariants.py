"""Docs-generation integration invariants.

This file should exercise the real generator path against fixture-backed
scenarios. The required guarantees are:
preserve content before and after `# Error Catalog` byte-for-byte, replace only
that section, and remain idempotent across reruns.
It should not use exact full-document snapshots as the primary assertion.
"""

from pathlib import Path

import pytest

from error_codegen.generators.docs import ERROR_CATALOG_HEADING, render_error_contract
from support.adapters import load_catalog
from support.expectations import collect_raw_error_entries
from support.scenarios import Scenario, failure_scenarios, success_scenarios


SCENARIOS_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "scenarios"
SUCCESS_SCENARIOS = [
    pytest.param(scenario, id=scenario.id)
    for scenario in success_scenarios(SCENARIOS_ROOT)
]
MISSING_HEADING_SCENARIOS = [
    pytest.param(scenario, id=scenario.id)
    for scenario in failure_scenarios(SCENARIOS_ROOT)
    if scenario.name == "doc_injection_missing_heading"
]
BASE_CATALOG_SCENARIO = next(iter(success_scenarios(SCENARIOS_ROOT)))


def _split_document(document: str) -> tuple[str, str, str]:
    """Split a markdown document into prefix, catalog section, and suffix."""
    heading_start = document.index(ERROR_CATALOG_HEADING)
    next_heading_index = document.find("\n# ", heading_start + len(ERROR_CATALOG_HEADING))
    if next_heading_index == -1:
        next_heading_index = len(document)
    return (
        document[:heading_start],
        document[heading_start:next_heading_index],
        document[next_heading_index:],
    )


@pytest.mark.parametrize("scenario", SUCCESS_SCENARIOS)
def test_generate_docs_preserves_handwritten_content_before_and_after_section(
    scenario: Scenario,
) -> None:
    """Generated docs should preserve handwritten prefix and suffix text exactly."""
    catalog = load_catalog(scenario.index_path)
    rendered = render_error_contract(catalog)
    expected_document = (
        scenario.root / "expected" / "docs" / "api" / "error-contract.md"
    ).read_text(encoding="utf-8")

    actual_prefix, actual_section, actual_suffix = _split_document(rendered)
    expected_prefix, _, expected_suffix = _split_document(expected_document)

    assert actual_prefix == expected_prefix
    assert actual_suffix == expected_suffix
    assert actual_section.startswith(f"{ERROR_CATALOG_HEADING}\n")

    expected_entries = collect_raw_error_entries(scenario.index_path)
    for entry in expected_entries:
        assert entry.code in actual_section
        assert entry.title in actual_section
        assert entry.type_slug in actual_section
        assert str(entry.http_status) in actual_section
        if entry.translation_key:
            assert entry.translation_key in actual_section

    for entry in expected_entries:
        for field_name in (entry.context_schema or {}).get("required", []):
            assert str(field_name) in actual_section


@pytest.mark.parametrize("scenario", SUCCESS_SCENARIOS)
def test_generate_docs_is_idempotent_for_the_same_catalog(
    scenario: Scenario,
) -> None:
    """Running docs generation twice for the same catalog should not change output."""
    catalog = load_catalog(scenario.index_path)

    first_render = render_error_contract(catalog)
    second_render = render_error_contract(catalog)

    assert first_render == second_render


@pytest.mark.parametrize("scenario", SUCCESS_SCENARIOS)
def test_generate_docs_keeps_section_ownership_local_to_the_catalog(
    scenario: Scenario,
) -> None:
    """The generator should update only the catalog section, not surrounding prose."""
    catalog = load_catalog(scenario.index_path)
    rendered = render_error_contract(catalog)

    prefix, section, suffix = _split_document(rendered)

    assert "# Error Catalog" not in prefix
    assert "# Error Catalog" in section
    expected_document = (
        scenario.root / "expected" / "docs" / "api" / "error-contract.md"
    ).read_text(encoding="utf-8")
    _, _, expected_suffix = _split_document(expected_document)
    assert suffix == expected_suffix


@pytest.mark.parametrize("scenario", MISSING_HEADING_SCENARIOS)
def test_generate_docs_fails_when_heading_is_missing(scenario: Scenario) -> None:
    """Generation should fail clearly when the target document lacks `# Error Catalog`."""
    catalog = load_catalog(BASE_CATALOG_SCENARIO.index_path)
    target_document = (
        scenario.root / "inputs" / "docs" / "api" / "error-contract.md"
    ).read_text(encoding="utf-8")

    with pytest.raises(ValueError, match="`# Error Catalog` heading"):
        render_error_contract(catalog, base_document=target_document)
