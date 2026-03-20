"""Enforce TypeScript generator helper behavior and metadata shape.

This file should cover helper rendering behavior, exported metadata shape, and
context typing or nested-schema handling. It should not enforce exact full-file
formatting when invariant checks are sufficient.
"""

import importlib
from types import SimpleNamespace
from typing import Any


def _import_typescript_generator_module() -> Any:
    """Import the TypeScript generator module using the repo-style path first."""
    candidates = [
        "tools.error_codegen.generators.typescript",
        "error_codegen.generators.typescript",
    ]
    last_error: Exception | None = None
    for name in candidates:
        try:
            return importlib.import_module(name)
        except Exception as error:  # pragma: no cover
            last_error = error
    raise AssertionError(
        f"Unable to import the TypeScript generator module. Last error: {last_error}"
    )


def _resolve_attr(module: Any, candidates: list[str]) -> Any:
    """Resolve the first available attribute from a module."""
    for name in candidates:
        if hasattr(module, name):
            return getattr(module, name)
    raise AssertionError(f"Expected one of {candidates!r} in {module.__name__}.")


def _fake_entry(code: str, *, module_name: str = "event_operations") -> Any:
    """Create a fake validated entry with the fields used by the TS generator."""
    slug = code.lower().replace("_", "-")
    return SimpleNamespace(
        module_name=module_name,
        code=code,
        type_uri=f"https://api.palioboard.local/problems/{slug}",
        recommended_http_status=409,
        http_status=409,
        title=code.replace("_", " ").title(),
        category="business_rule",
        retry_policy="never",
        safe_to_expose=True,
        translation_key=f"errors.{code.lower()}",
        normalized_context_schema={
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
        description=None,
        log_level=None,
        severity=None,
    )


def test_render_literal_handles_scalar_values() -> None:
    """Literal rendering should preserve TypeScript-compatible scalars."""
    module = _import_typescript_generator_module()
    render_literal = _resolve_attr(module, ["_render_literal"])

    assert render_literal("abc") == '"abc"'
    assert render_literal(True) == "true"
    assert render_literal(False) == "false"
    assert render_literal(None) == "null"
    assert render_literal(7) == "7"


def test_alias_name_helpers_generate_stable_context_type_names() -> None:
    """Alias helpers should derive stable exported type names from codes and shared schemas."""
    module = _import_typescript_generator_module()
    shared_alias_name = _resolve_attr(module, ["_shared_context_alias_name"])
    context_alias_name = _resolve_attr(module, ["_context_alias_name"])

    assert shared_alias_name("uuid_ref") == "SharedContextUuidRef"
    assert context_alias_name("JOLLY_ALREADY_USED") == "JollyAlreadyUsedContext"


def test_render_schema_type_handles_nested_object_schema() -> None:
    """Schema rendering should preserve required-vs-optional object fields."""
    module = _import_typescript_generator_module()
    render_schema_type = _resolve_attr(module, ["_render_schema_type"])

    schema = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "team_id": {"type": "string"},
            "previous_game_id": {"type": "string"},
        },
        "required": ["team_id"],
    }

    rendered = render_schema_type(schema, {}, path=())

    assert '"team_id": string;' in rendered
    assert '"previous_game_id"?: string;' in rendered


def test_generate_typescript_artifact_contains_codes_translation_keys_and_modules() -> (
    None
):
    """Full TS generation should include codes, translation keys, and module ownership."""
    module = _import_typescript_generator_module()
    generate_artifact = _resolve_attr(
        module,
        ["generate_typescript_error_artifact", "render_typescript_error_artifact"],
    )

    fake_catalog = SimpleNamespace(
        module_names=("event_operations", "tournaments"),
        shared_context_schemas={},
        errors_for_module=lambda name: (
            (_fake_entry("JOLLY_ALREADY_USED", module_name="event_operations"),)
            if name == "event_operations"
            else (_fake_entry("TOURNAMENT_LOCKED", module_name="tournaments"),)
        ),
    )

    output = generate_artifact(fake_catalog)

    assert "JOLLY_ALREADY_USED" in output
    assert "TOURNAMENT_LOCKED" in output
    assert "errors.jolly_already_used" in output
    assert "event_operations" in output
    assert "tournaments" in output
