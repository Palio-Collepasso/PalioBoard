
"""Enforce that failure scenarios fail for the expected reason family.

This file should cover broad scenario-driven validation failures only. It should
not replace precise unit coverage for individual validator rules.
"""


from pathlib import Path

import pytest

from support.adapters import catalog_validation_error_type, load_catalog
from support.expectations import expected_failure_markers
from support.scenarios import Scenario, failure_scenarios


FAILURE_SCENARIOS = [
    pytest.param(scenario, id=scenario.id)
    for scenario in failure_scenarios(Path(__file__).resolve().parents[1] / 'fixtures' / 'scenarios')
]


@pytest.mark.parametrize('scenario', FAILURE_SCENARIOS)
def test_failure_catalogs_raise_validation_errors_with_expected_markers(
    scenario: Scenario,
) -> None:
    """Every failure scenario should fail for the expected reason family."""
    error_type = catalog_validation_error_type()

    with pytest.raises(error_type) as exc_info:
        load_catalog(scenario.index_path)

    message = str(exc_info.value)
    for marker in expected_failure_markers(scenario.name):
        assert marker.lower() in message.lower()
