"""Pytest fixtures for the error_codegen tool test suite."""

# ruff: noqa: E402

import os
import sys
from pathlib import Path

import pytest

TESTS_ROOT = Path(__file__).resolve().parent
API_SRC_ROOT = TESTS_ROOT.parents[2] / "apps" / "api" / "src"
for path in (API_SRC_ROOT, TESTS_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from support.scenarios import Scenario, failure_scenarios, success_scenarios


@pytest.fixture(scope="session")
def scenarios_root() -> Path:
    """Return the root directory containing success/failure scenario folders."""
    explicit = os.environ.get("ERROR_CATALOG_SCENARIOS_ROOT")
    if explicit:
        return Path(explicit)
    return TESTS_ROOT / "fixtures" / "scenarios"


@pytest.fixture(scope="session")
def all_success_scenarios(scenarios_root: Path) -> list[Scenario]:
    """Return all discovered valid scenarios."""
    return success_scenarios(scenarios_root)


@pytest.fixture(scope="session")
def all_failure_scenarios(scenarios_root: Path) -> list[Scenario]:
    """Return all discovered invalid scenarios."""
    return failure_scenarios(scenarios_root)
