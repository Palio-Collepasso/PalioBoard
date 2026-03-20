"""Enforce docs-generation invariants across valid scenarios.

This file should verify generated Error Catalog content and section-level
expectations through the real generator path. It complements unit tests for
preservation, idempotence, and missing-heading behavior.
"""

from pathlib import Path

import pytest

from support.adapters import load_catalog, render_docs_artifact
from support.expectations import collect_raw_error_entries
from support.scenarios import Scenario, success_scenarios


SUCCESS_SCENARIOS = [
    pytest.param(scenario, id=scenario.id)
    for scenario in success_scenarios(
        Path(__file__).resolve().parents[1] / "fixtures" / "scenarios"
    )
]


@pytest.mark.parametrize("scenario", SUCCESS_SCENARIOS)
def test_docs_generation_contains_expected_sections_and_error_details(
    scenario: Scenario,
) -> None:
    """Generated docs should include core catalog details for every error."""
    catalog = load_catalog(scenario.index_path)
    rendered = render_docs_artifact(
        catalog,
        title=f"{scenario.level.capitalize()} {scenario.outcome} — {scenario.name}",
    )
    entries = collect_raw_error_entries(scenario.index_path)

    assert rendered
    for entry in entries:
        assert entry.code in rendered
        assert entry.title in rendered
        assert entry.type_slug in rendered
        assert str(entry.http_status) in rendered
        if entry.translation_key:
            assert entry.translation_key in rendered

        required_fields = (entry.context_schema or {}).get("required", [])
        for field_name in required_fields:
            assert str(field_name) in rendered
