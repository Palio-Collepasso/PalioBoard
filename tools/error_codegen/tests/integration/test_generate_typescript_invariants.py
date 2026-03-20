"""Enforce TypeScript generation invariants across valid scenarios.

This file should cover exported metadata invariants, context typing or key
exposure expectations, and deterministic rendering. It should not enforce exact
formatting when invariant checks are sufficient.
"""

from pathlib import Path

import pytest

from support.adapters import load_catalog, render_typescript_artifact
from support.expectations import collect_raw_error_entries
from support.scenarios import Scenario, success_scenarios

SUCCESS_SCENARIOS = [
    pytest.param(scenario, id=scenario.id)
    for scenario in success_scenarios(
        Path(__file__).resolve().parents[1] / "fixtures" / "scenarios"
    )
]


@pytest.mark.parametrize("scenario", SUCCESS_SCENARIOS)
def test_typescript_generation_contains_expected_codes_and_keys(
    scenario: Scenario,
) -> None:
    """Generated TypeScript should contain the expected codes, slugs, and translation keys."""
    catalog = load_catalog(scenario.index_path)
    rendered = render_typescript_artifact(catalog)
    entries = collect_raw_error_entries(scenario.index_path)

    assert rendered
    for entry in entries:
        assert entry.code in rendered
        assert entry.type_slug in rendered
        assert entry.title in rendered
        if entry.translation_key:
            assert entry.translation_key in rendered


@pytest.mark.parametrize("scenario", SUCCESS_SCENARIOS)
def test_typescript_generation_is_deterministic_for_each_scenario(
    scenario: Scenario,
) -> None:
    """Rendering the same catalog twice should produce identical TypeScript."""
    catalog_one = load_catalog(scenario.index_path)
    catalog_two = load_catalog(scenario.index_path)

    first = render_typescript_artifact(catalog_one)
    second = render_typescript_artifact(catalog_two)
    assert first == second
