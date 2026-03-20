"""Enforce future generated API mapping coverage.

This file should cover the target mapping contract only:
- generated mapping lives in `palio/api/modules/<module>/errors/mapping_gen.py`
- mapping connects generated domain error types to generated API problem specs
- one mapping entry per catalog entry
- no extra/unexpected entries beyond catalog errors
- valid generated Python

It should not cover domain-error generation, API runtime behavior, or docs.
"""

from __future__ import annotations

import ast
from types import ModuleType

from error_codegen.common import pascal_case
from support.generated_contract import module_source_path, require_attr, require_module
from support.sample_catalog import build_sample_catalog

TARGET_DOMAIN_MODULE = "palio.modules.event_operations.errors_gen"
TARGET_MAPPING_MODULE = "palio.api.modules.event_operations.errors.mapping_gen"
TARGET_SPEC_MODULE = "palio.api.modules.event_operations.errors.specs_gen"


def _domain_class_name(code: str) -> str:
    """Return the generated domain-error class name for one error code."""
    return f"{pascal_case(code)}Error"


def _constant_name(code: str) -> str:
    """Return the generated API-problem constant name for one error code."""
    return f"{code}_API_PROBLEM"


def _generated_domain_module() -> ModuleType:
    return require_module(TARGET_DOMAIN_MODULE)


def _generated_mapping_module() -> ModuleType:
    return require_module(TARGET_MAPPING_MODULE)


def _generated_spec_module() -> ModuleType:
    return require_module(TARGET_SPEC_MODULE)


def test_generated_api_mapping_file_exists_per_module() -> None:
    """Generated API-mapping modules should live under the target package path."""
    source_path = module_source_path(_generated_mapping_module())

    assert source_path.as_posix().endswith(
        "palio/api/modules/event_operations/errors/mapping_gen.py"
    )


def test_generated_api_mapping_connects_domain_error_to_problem_spec() -> None:
    """Generated domain errors should map to generated API problem specs."""
    catalog = build_sample_catalog()
    domain_module = _generated_domain_module()
    mapping_module = _generated_mapping_module()
    spec_module = _generated_spec_module()
    mapping = require_attr(mapping_module, "ERROR_TO_PROBLEM")
    entry = catalog.errors["JOLLY_ALREADY_USED"]
    domain_error_type = require_attr(domain_module, _domain_class_name(entry.code))
    problem_spec = require_attr(spec_module, _constant_name(entry.code))

    assert mapping == {domain_error_type: problem_spec}
    assert mapping[domain_error_type] is problem_spec


def test_generated_api_mapping_exports_one_entry_per_catalog_error() -> None:
    """One mapping entry should exist per catalog error."""
    catalog = build_sample_catalog()
    domain_module = _generated_domain_module()
    mapping = require_attr(_generated_mapping_module(), "ERROR_TO_PROBLEM")

    expected_keys = {
        require_attr(domain_module, _domain_class_name(entry.code))
        for entry in catalog.errors.values()
    }

    assert set(mapping) == expected_keys
    assert len(mapping) == len(catalog.errors)


def test_generated_api_mapping_has_no_unexpected_extra_entries() -> None:
    """Generated mappings should not contain any unexpected extra entries."""
    catalog = build_sample_catalog()
    domain_module = _generated_domain_module()
    spec_module = _generated_spec_module()
    mapping = require_attr(_generated_mapping_module(), "ERROR_TO_PROBLEM")

    expected_items = {
        require_attr(domain_module, _domain_class_name(entry.code)): require_attr(
            spec_module, _constant_name(entry.code)
        )
        for entry in catalog.errors.values()
    }

    assert mapping == expected_items


def test_generate_api_mappings_outputs_valid_python() -> None:
    """Generated API-mapping source should parse as valid Python."""
    source_path = module_source_path(_generated_mapping_module())

    ast.parse(source_path.read_text(encoding="utf-8"), filename=str(source_path))
