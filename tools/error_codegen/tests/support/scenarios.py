"""Scenario discovery helpers for the error_codegen tool test suite.

This module stays tool-owned. It should not grow API runtime helpers or any
logic that depends on FastAPI or application wiring.
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Scenario:
    """Describe one scenario folder."""

    outcome: str
    level: str
    name: str
    root: Path

    @property
    def id(self) -> str:
        """Return a stable pytest id."""
        return f"{self.outcome}/{self.level}/{self.name}"

    @property
    def contracts_root(self) -> Path:
        """Return the contracts/errors directory."""
        return self.root / "inputs" / "contracts" / "errors"

    @property
    def index_path(self) -> Path:
        """Return the catalog index file."""
        return self.contracts_root / "index.yaml"



def _discover(base_root: Path, outcome: str) -> list[Scenario]:
    """Discover scenarios below one outcome root."""
    base = base_root / outcome
    discovered: list[Scenario] = []
    for level_dir in sorted(path for path in base.iterdir() if path.is_dir()):
        for scenario_dir in sorted(path for path in level_dir.iterdir() if path.is_dir()):
            discovered.append(
                Scenario(
                    outcome=outcome,
                    level=level_dir.name,
                    name=scenario_dir.name,
                    root=scenario_dir,
                )
            )
    return discovered



def success_scenarios(base_root: Path) -> list[Scenario]:
    """Return all success scenarios."""
    return _discover(base_root, "success")



def failure_scenarios(base_root: Path) -> list[Scenario]:
    """Return all failure scenarios."""
    return _discover(base_root, "failure")
