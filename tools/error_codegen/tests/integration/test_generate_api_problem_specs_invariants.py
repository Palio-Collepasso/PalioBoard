"""Enforce future generated API problem-spec invariants.

This file should cover the artifact-level API-spec contract only:
- generated constants live in `palio/api/modules/<module>/errors/specs_gen.py`
- the shared `ApiProblemSpec` type lives in `palio.api.errors.spec`
- generated constants are instances of that shared type
- one generated file per owning module
- one constant per catalog entry
- `code`, `type_uri`, `title`, `http_status`, `translation_key` only
- no domain-field leakage
- valid generated Python

It should not cover domain-error generation, mappings, or runtime behavior.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from support.adapters import load_catalog
from support.generated_contract import module_source_path, require_attr, require_module
from support.scenarios import Scenario, success_scenarios

SCENARIOS_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "scenarios"
SUCCESS_SCENARIOS = [
    pytest.param(scenario, id=scenario.id)
    for scenario in success_scenarios(SCENARIOS_ROOT)
]


def _constant_name(code: str) -> str:
    """Return the generated API-problem constant name for one error code."""
    return f"{code}_API_PROBLEM"


@pytest.mark.parametrize("scenario", SUCCESS_SCENARIOS)
def test_generate_api_problem_specs_writes_one_file_per_module(
    scenario: Scenario,
) -> None:
    """Each owning module should have exactly one generated API-spec file."""
    catalog = load_catalog(scenario.index_path)
    for fragment in catalog.fragments:
        module = require_module(
            f"palio.api.modules.{fragment.module_name}.errors.specs_gen"
        )
        source_path = module_source_path(module)

        assert source_path.as_posix().endswith(
            f"palio/api/modules/{fragment.module_name}/errors/specs_gen.py"
        )


@pytest.mark.parametrize("scenario", SUCCESS_SCENARIOS)
def test_generate_api_problem_specs_exports_transport_metadata_only(
    scenario: Scenario,
) -> None:
    """Generated API-spec constants should carry only transport metadata."""
    catalog = load_catalog(scenario.index_path)
    shared_spec_type = require_attr(
        require_module("palio.api.errors.spec"),
        "ApiProblemSpec",
    )

    for fragment in catalog.fragments:
        module = require_module(
            f"palio.api.modules.{fragment.module_name}.errors.specs_gen"
        )
        actual_constant_names = sorted(
            name for name in vars(module) if name.endswith("_API_PROBLEM")
        )
        expected_constant_names = sorted(
            _constant_name(entry.code) for entry in fragment.errors
        )

        assert actual_constant_names == expected_constant_names
        for entry in fragment.errors:
            spec = require_attr(module, _constant_name(entry.code))
            assert isinstance(spec, shared_spec_type)
            assert spec.code == entry.code
            assert spec.type_uri == entry.type_uri
            assert spec.title == entry.title
            assert spec.http_status == entry.http_status
            assert spec.translation_key == entry.translation_key
            assert not hasattr(spec, "module_name")
            assert not hasattr(spec, "context_schema")
            assert not hasattr(spec, "retry_policy")


@pytest.mark.parametrize("scenario", SUCCESS_SCENARIOS)
def test_generate_api_problem_specs_does_not_leak_domain_fields(
    scenario: Scenario,
) -> None:
    """Generated API-spec constants should not expose domain-only fields."""
    catalog = load_catalog(scenario.index_path)

    for fragment in catalog.fragments:
        module = require_module(
            f"palio.api.modules.{fragment.module_name}.errors.specs_gen"
        )
        for entry in fragment.errors:
            spec = require_attr(module, _constant_name(entry.code))
            for forbidden_name in {
                "module_name",
                "category",
                "retry_policy",
                "safe_to_expose",
                "context_schema",
                "description",
                "log_level",
                "severity",
            }:
                assert not hasattr(spec, forbidden_name)


@pytest.mark.parametrize("scenario", SUCCESS_SCENARIOS)
def test_generate_api_problem_specs_outputs_valid_python(
    scenario: Scenario,
) -> None:
    """Generated API-spec source should parse as valid Python."""
    catalog = load_catalog(scenario.index_path)

    for fragment in catalog.fragments:
        module = require_module(
            f"palio.api.modules.{fragment.module_name}.errors.specs_gen"
        )
        source_path = module_source_path(module)
        ast.parse(source_path.read_text(encoding="utf-8"), filename=str(source_path))
