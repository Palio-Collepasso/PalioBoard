"""Enforce Python domain-error generation invariants across valid scenarios.

These tests should only cover the domain-error generator layer:
- one generated file per owning module
- expected relative path shape under ``palio/modules/<module>/errors_gen.py``
- no unexpected extra module files
- syntactically valid Python for all outputs
- scenario-driven output shape without exact formatting checks

They should not cover generated API problem specs or API mappings here.
"""

import ast
import re
from pathlib import Path

import pytest

from support.adapters import build_python_artifacts, load_catalog
from support.scenarios import Scenario, success_scenarios

SUCCESS_SCENARIOS = [
    pytest.param(scenario, id=scenario.id)
    for scenario in success_scenarios(
        Path(__file__).resolve().parents[1] / "fixtures" / "scenarios"
    )
]


def _module_name_from_generated_path(path: str) -> str:
    """Extract the owning module name from a generated Python output path."""
    match = re.search(r"palio/modules/([^/]+)/errors_gen\.py$", Path(path).as_posix())
    if match is None:
        raise AssertionError(
            "Generated Python output path does not match "
            "palio/modules/<module>/errors_gen.py: "
            f"{path}"
        )
    return match.group(1)


@pytest.mark.parametrize("scenario", SUCCESS_SCENARIOS)
def test_python_generation_writes_one_domain_file_per_module(
    scenario: Scenario,
) -> None:
    """Each owning module should get exactly one generated domain-error file."""
    catalog = load_catalog(scenario.index_path)
    generated = build_python_artifacts(catalog)

    assert len(generated) == len(catalog.fragments)

    observed_modules = {_module_name_from_generated_path(path) for path in generated}
    assert observed_modules == set(catalog.module_names)

    for path in generated:
        module_name = _module_name_from_generated_path(path)
        assert Path(path).as_posix().endswith(
            f"palio/modules/{module_name}/errors_gen.py"
        )


@pytest.mark.parametrize("scenario", SUCCESS_SCENARIOS)
def test_python_generation_outputs_are_valid_python(scenario: Scenario) -> None:
    """Generated domain-error files should parse as valid Python source."""
    catalog = load_catalog(scenario.index_path)
    generated = build_python_artifacts(catalog)

    for fragment in catalog.fragments:
        expected_suffix = f"palio/modules/{fragment.module_name}/errors_gen.py"
        matching_paths = [
            path
            for path in generated
            if Path(path).as_posix().endswith(expected_suffix)
        ]
        assert len(matching_paths) == 1, expected_suffix

        path = matching_paths[0]
        source = generated[path]
        ast.parse(source, filename=path)

        class_defs = [
            node
            for node in ast.parse(source, filename=path).body
            if isinstance(node, ast.ClassDef)
        ]
        assert len(class_defs) == len(fragment.errors)
