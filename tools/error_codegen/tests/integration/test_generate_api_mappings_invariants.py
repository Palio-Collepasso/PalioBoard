"""Enforce future generated API mapping invariants.

This file should cover the artifact-level mapping contract only:
- generated mapping lives in `palio/api/modules/<module>/errors/mapping_gen.py`
- mapping ties generated domain error types to generated API problem specs
- one mapping entry per catalog entry
- no extra/unexpected entries beyond catalog errors
- valid generated Python

It should not cover runtime serialization or domain-error generation details.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from error_codegen.common import pascal_case
from support.adapters import load_catalog
from support.generated_contract import module_source_path, require_attr, require_module
from support.scenarios import Scenario, success_scenarios

SCENARIOS_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "scenarios"
SUCCESS_SCENARIOS = [
    pytest.param(scenario, id=scenario.id)
    for scenario in success_scenarios(SCENARIOS_ROOT)
]


def _domain_class_name(code: str) -> str:
    """Return the generated domain-error class name for one error code."""
    return f"{pascal_case(code)}Error"


def _constant_name(code: str) -> str:
    """Return the generated API-problem constant name for one error code."""
    return f"{code}_API_PROBLEM"


@pytest.mark.parametrize("scenario", SUCCESS_SCENARIOS)
def test_generate_api_mappings_writes_one_file_per_module(
    scenario: Scenario,
) -> None:
    """Each owning module should have exactly one generated mapping file."""
    catalog = load_catalog(scenario.index_path)
    for fragment in catalog.fragments:
        module = require_module(
            f"palio.api.modules.{fragment.module_name}.errors.mapping_gen"
        )
        source_path = module_source_path(module)

        assert source_path.as_posix().endswith(
            f"palio/api/modules/{fragment.module_name}/errors/mapping_gen.py"
        )


@pytest.mark.parametrize("scenario", SUCCESS_SCENARIOS)
def test_generate_api_mappings_links_domain_error_types_to_api_specs(
    scenario: Scenario,
) -> None:
    """Generated mappings should link generated domain types to API specs."""
    catalog = load_catalog(scenario.index_path)

    for fragment in catalog.fragments:
        mapping_module = require_module(
            f"palio.api.modules.{fragment.module_name}.errors.mapping_gen"
        )
        domain_module = require_module(
            f"palio.modules.{fragment.module_name}.errors_gen"
        )
        spec_module = require_module(
            f"palio.api.modules.{fragment.module_name}.errors.specs_gen"
        )
        mapping = require_attr(mapping_module, "ERROR_TO_PROBLEM")

        for entry in fragment.errors:
            domain_error_type = require_attr(
                domain_module, _domain_class_name(entry.code)
            )
            api_problem_spec = require_attr(spec_module, _constant_name(entry.code))
            assert mapping[domain_error_type] is api_problem_spec


@pytest.mark.parametrize("scenario", SUCCESS_SCENARIOS)
def test_generate_api_mappings_exports_one_entry_per_catalog_error(
    scenario: Scenario,
) -> None:
    """One mapping entry should exist per catalog error."""
    catalog = load_catalog(scenario.index_path)

    for fragment in catalog.fragments:
        mapping_module = require_module(
            f"palio.api.modules.{fragment.module_name}.errors.mapping_gen"
        )
        domain_module = require_module(
            f"palio.modules.{fragment.module_name}.errors_gen"
        )
        mapping = require_attr(mapping_module, "ERROR_TO_PROBLEM")

        expected_keys = {
            require_attr(domain_module, _domain_class_name(entry.code))
            for entry in fragment.errors
        }

        assert set(mapping) == expected_keys
        assert len(mapping) == len(fragment.errors)


@pytest.mark.parametrize("scenario", SUCCESS_SCENARIOS)
def test_generate_api_mappings_have_no_unexpected_extra_entries(
    scenario: Scenario,
) -> None:
    """Generated mappings should not contain any unexpected extra entries."""
    catalog = load_catalog(scenario.index_path)

    for fragment in catalog.fragments:
        mapping_module = require_module(
            f"palio.api.modules.{fragment.module_name}.errors.mapping_gen"
        )
        domain_module = require_module(
            f"palio.modules.{fragment.module_name}.errors_gen"
        )
        spec_module = require_module(
            f"palio.api.modules.{fragment.module_name}.errors.specs_gen"
        )
        mapping = require_attr(mapping_module, "ERROR_TO_PROBLEM")

        expected_items = {
            require_attr(domain_module, _domain_class_name(entry.code)): require_attr(
                spec_module, _constant_name(entry.code)
            )
            for entry in fragment.errors
        }

        assert mapping == expected_items


@pytest.mark.parametrize("scenario", SUCCESS_SCENARIOS)
def test_generate_api_mappings_outputs_valid_python(scenario: Scenario) -> None:
    """Generated API-mapping source should parse as valid Python."""
    catalog = load_catalog(scenario.index_path)

    for fragment in catalog.fragments:
        module = require_module(
            f"palio.api.modules.{fragment.module_name}.errors.mapping_gen"
        )
        source_path = module_source_path(module)
        ast.parse(source_path.read_text(encoding="utf-8"), filename=str(source_path))
