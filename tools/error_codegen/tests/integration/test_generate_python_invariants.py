"""Enforce Python generation invariants across valid scenarios.

This file should verify:
- one syntactically valid generated file per owning module
- expected relative file paths
- no unexpected extra module files
- per-entry invariant metadata required by the target architecture

It should not enforce exact formatting, import style, API runtime behavior, or
frontend generation behavior.
"""

import ast
from pathlib import Path

import pytest

from support.adapters import build_python_artifacts, load_catalog
from support.expectations import generated_python_expectations
from support.scenarios import Scenario, success_scenarios

SUCCESS_SCENARIOS = [
    pytest.param(scenario, id=scenario.id)
    for scenario in success_scenarios(
        Path(__file__).resolve().parents[1] / "fixtures" / "scenarios"
    )
]


@pytest.mark.parametrize("scenario", SUCCESS_SCENARIOS)
def test_python_generation_emits_module_files_with_expected_error_metadata(
    scenario: Scenario,
) -> None:
    """Generated Python should exist per module and include expected error metadata."""
    catalog = load_catalog(scenario.index_path)
    generated = build_python_artifacts(catalog)
    expected_by_module = generated_python_expectations(scenario.index_path)

    assert generated, "No Python artifacts were generated"

    for module_name, expected_entries in expected_by_module.items():
        matching_paths = [
            path for path in generated if path.startswith(f"{module_name}/")
        ]
        assert matching_paths, f"Missing generated Python file for module {module_name}"

        matching_paths = sorted(matching_paths)
        for path in matching_paths:
            ast.parse(generated[path], filename=path)

        combined_source = "\n\n".join(generated[path] for path in matching_paths)

        for entry in expected_entries:
            assert entry.code in combined_source, (
                f"Missing code {entry.code} in generated Python for module {module_name}"
            )
            assert entry.title in combined_source, (
                f"Missing title {entry.title!r} in generated Python for module {module_name}"
            )
            assert str(entry.http_status) in combined_source, (
                f"Missing http_status {entry.http_status} in generated Python for module {module_name}"
            )
            assert entry.type_slug in combined_source, (
                f"Missing type_slug {entry.type_slug} in generated Python for module {module_name}"
            )
            if entry.translation_key:
                assert entry.translation_key in combined_source, (
                    f"Missing translation_key {entry.translation_key} in generated Python for module {module_name}"
                )
