"""Enforce future generated API problem-spec coverage.

This file should cover the target API-spec contract only:
- generated constants live in `palio/api/modules/<module>/errors/specs_gen.py`
- the shared `ApiProblemSpec` type lives in `palio.api.errors.spec`
- generated constants are instances of that shared type
- one constant per catalog entry
- `code`, `type_uri`, `title`, `http_status`, `translation_key` only
- no domain-field leakage into the generated problem-spec layer
- valid generated Python

It should not cover domain-error generation, mapping generation, or CLI/runtime
behavior.
"""

from __future__ import annotations

import ast
import dataclasses
from types import ModuleType

from support.generated_contract import module_source_path, require_attr, require_module
from support.sample_catalog import build_sample_catalog

TARGET_SPEC_MODULE = "palio.api.modules.event_operations.errors.specs_gen"
SHARED_SPEC_MODULE = "palio.api.errors.spec"


def _constant_name(code: str) -> str:
    """Return the generated API-problem constant name for one error code."""
    return f"{code}_API_PROBLEM"


def _generated_spec_module() -> ModuleType:
    return require_module(TARGET_SPEC_MODULE)


def _shared_spec_type() -> type[object]:
    return require_attr(require_module(SHARED_SPEC_MODULE), "ApiProblemSpec")


def test_generated_api_problem_spec_file_exists_per_module() -> None:
    """Generated API-spec modules should live under the target package path."""
    module = _generated_spec_module()
    source_path = module_source_path(module)

    assert source_path.as_posix().endswith(
        "palio/api/modules/event_operations/errors/specs_gen.py"
    )


def test_generated_api_problem_spec_exports_constant_per_entry() -> None:
    """One generated constant should exist per catalog entry."""
    catalog = build_sample_catalog()
    module = _generated_spec_module()

    actual_constant_names = sorted(
        name for name in vars(module) if name.endswith("_API_PROBLEM")
    )
    expected_constant_names = sorted(
        _constant_name(entry.code) for entry in catalog.errors.values()
    )

    assert actual_constant_names == expected_constant_names


def test_generated_api_problem_spec_contains_only_transport_metadata() -> None:
    """Generated API specs should expose only transport metadata fields."""
    catalog = build_sample_catalog()
    module = _generated_spec_module()
    entry = catalog.errors["JOLLY_ALREADY_USED"]
    spec = require_attr(module, _constant_name(entry.code))

    assert dataclasses.is_dataclass(spec)
    assert spec.code == entry.code
    assert spec.type_uri == entry.type_uri
    assert spec.title == entry.title
    assert spec.http_status == entry.http_status
    assert spec.translation_key == entry.translation_key


def test_generated_api_problem_spec_does_not_leak_domain_fields() -> None:
    """Generated API specs should not expose domain-only fields."""
    module = _generated_spec_module()
    spec = require_attr(module, _constant_name("JOLLY_ALREADY_USED"))

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


def test_generated_api_problem_spec_is_instance_of_shared_api_problem_spec_type() -> (
    None
):
    """Generated constants should be instances of the shared `ApiProblemSpec` type."""
    catalog = build_sample_catalog()
    module = _generated_spec_module()
    shared_spec_type = _shared_spec_type()
    spec = require_attr(
        module, _constant_name(catalog.errors["JOLLY_ALREADY_USED"].code)
    )

    assert isinstance(spec, shared_spec_type)


def test_generate_api_problem_specs_outputs_valid_python() -> None:
    """Generated API-spec source should parse as valid Python."""
    source_path = module_source_path(_generated_spec_module())

    ast.parse(source_path.read_text(encoding="utf-8"), filename=str(source_path))
