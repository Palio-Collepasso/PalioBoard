from support.scenarios import failure_scenarios, success_scenarios


def test_scenario_pack_contains_success_scenarios(scenarios_root) -> None:
    """Ensure the success side of the scenario pack is discoverable."""
    scenarios = success_scenarios(scenarios_root)
    assert scenarios


def test_scenario_pack_contains_failure_scenarios(scenarios_root) -> None:
    """Ensure the failure side of the scenario pack is discoverable."""
    scenarios = failure_scenarios(scenarios_root)
    assert scenarios
