"""Enforce that all success scenarios load cleanly through the real tool stack.

This file should cover broad scenario-driven validation success only. It should
not replace unit tests for field-level or semantic validator rules.
"""

from pathlib import Path

import pytest

from support.adapters import load_catalog
from support.scenarios import Scenario, success_scenarios


SUCCESS_SCENARIOS = [
    pytest.param(scenario, id=scenario.id)
    for scenario in success_scenarios(
        Path(__file__).resolve().parents[1] / "fixtures" / "scenarios"
    )
]


@pytest.mark.parametrize("scenario", SUCCESS_SCENARIOS)
def test_success_catalogs_load_without_validation_errors(scenario: Scenario) -> None:
    """Every success scenario should validate and load cleanly."""
    catalog = load_catalog(scenario.index_path)
    assert catalog is not None
