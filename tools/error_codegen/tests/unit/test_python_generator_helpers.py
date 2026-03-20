"""Enforce generated Python domain errors for the intended architecture.

These tests should only cover the domain-error side of the generator:
- one dataclass-like generated error class per catalog entry
- generated files under ``palio/modules/<module>/errors_gen.py``
- field names projected from ``context_schema.properties``
- required and optional context handling stays consistent
- no HTTP/API metadata, FastAPI, response, or problem-details leakage

They should not cover generated API problem specs or mapping files here.
"""

import ast
import importlib
from types import ModuleType

from error_codegen.models import ErrorCatalogEntry
from support.sample_catalog import sample_entry_kwargs


def _import_python_generator_module() -> ModuleType:
    """Import the Python generator module using the repo-style path first."""
    candidates = [
        "tools.error_codegen.generators.python",
        "error_codegen.generators.python",
    ]
    last_error: Exception | None = None
    for name in candidates:
        try:
            return importlib.import_module(name)
        except Exception as error:  # pragma: no cover - actionable mismatch path
            last_error = error
    raise AssertionError(
        f"Unable to import the Python generator module. Last error: {last_error}"
    )


def _resolve_attr(module: ModuleType, candidates: list[str]) -> object:
    """Resolve the first available attribute from a module."""
    for name in candidates:
        if hasattr(module, name):
            return getattr(module, name)
    raise AssertionError(f"Expected one of {candidates!r} in {module.__name__}.")


def _context_schema(
    *,
    required: tuple[str, ...],
    optional: tuple[str, ...] = (),
) -> dict[str, object]:
    """Build one closed object schema for a domain error context."""
    properties = {
        field_name: {
            "type": "string",
        }
        for field_name in (*required, *optional)
    }
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": properties,
        "required": list(required),
    }


def _entry(
    *,
    code: str,
    type_slug: str,
    title: str,
    required: tuple[str, ...],
    optional: tuple[str, ...] = (),
) -> ErrorCatalogEntry:
    """Create one validated catalog entry for generator assertions."""
    schema = _context_schema(required=required, optional=optional)
    example_context = {name: f"{name}-value" for name in (*required, *optional)}
    return ErrorCatalogEntry(
        **sample_entry_kwargs(
            code=code,
            type_slug=type_slug,
            title=title,
            raw_context_schema=schema,
            normalized_context_schema=schema,
            resolved_context_schema=schema,
            example={"context": example_context},
        )
    )


def _class_definitions(source: str) -> list[ast.ClassDef]:
    """Return top-level class definitions from generated Python source."""
    tree = ast.parse(source)
    return [node for node in tree.body if isinstance(node, ast.ClassDef)]


def _class_field_specs(class_def: ast.ClassDef) -> list[tuple[str, bool]]:
    """Return class field names and whether each field has a default."""
    fields: list[tuple[str, bool]] = []
    for node in class_def.body:
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            fields.append((node.target.id, node.value is not None))
    return fields


def _is_dataclass_domain_error(class_def: ast.ClassDef) -> bool:
    """Return whether one generated class matches the intended dataclass shape."""
    has_domain_error_base = any(
        isinstance(base, ast.Name) and base.id == "DomainError"
        for base in class_def.bases
    )
    has_dataclass_decorator = any(
        isinstance(decorator, ast.Call)
        and isinstance(decorator.func, ast.Name)
        and decorator.func.id == "dataclass"
        and any(
            keyword.arg == "slots"
            and isinstance(keyword.value, ast.Constant)
            and keyword.value.value is True
            for keyword in decorator.keywords
        )
        for decorator in class_def.decorator_list
    )
    return has_domain_error_base and has_dataclass_decorator


def test_render_module_source_emits_one_dataclass_domain_error_per_entry() -> None:
    """Rendered Python should expose one dataclass-like domain error class per entry."""
    module = _import_python_generator_module()
    render_module_source = _resolve_attr(module, ["_render_module_source"])

    entries = (
        _entry(
            code="JOLLY_ALREADY_USED",
            type_slug="jolly-already-used",
            title="Jolly already used",
            required=("team_id", "game_id"),
            optional=("previous_game_id",),
        ),
        _entry(
            code="GAME_NOT_IN_PROGRESS",
            type_slug="game-not-in-progress",
            title="Game not in progress",
            required=("game_id", "current_state"),
        ),
    )

    source = render_module_source("event_operations", entries)
    class_defs = _class_definitions(source)

    assert "from dataclasses import dataclass" in source
    assert "from palio.shared.errors import DomainError" in source
    assert [class_def.name for class_def in class_defs] == [
        "JollyAlreadyUsedError",
        "GameNotInProgressError",
    ]

    for class_def, entry in zip(class_defs, entries, strict=True):
        assert _is_dataclass_domain_error(class_def)
        expected_field_names = list(entry.resolved_context_schema["properties"])
        actual_fields = _class_field_specs(class_def)
        assert [field_name for field_name, _ in actual_fields] == expected_field_names

        required_names = list(entry.resolved_context_schema.get("required", []))
        optional_names = [
            field_name
            for field_name in expected_field_names
            if field_name not in required_names
        ]

        assert {
            field_name for field_name, has_default in actual_fields if not has_default
        } == set(required_names)
        assert {
            field_name for field_name, has_default in actual_fields if has_default
        } == set(optional_names)


def test_render_module_source_keeps_http_and_runtime_metadata_out_of_domain_classes(
) -> None:
    """Rendered Python should not leak transport or runtime concerns."""
    module = _import_python_generator_module()
    render_module_source = _resolve_attr(module, ["_render_module_source"])

    source = render_module_source(
        "event_operations",
        (
            _entry(
                code="JOLLY_ALREADY_USED",
                type_slug="jolly-already-used",
                title="Jolly already used",
                required=("team_id", "game_id"),
                optional=("previous_game_id",),
            ),
        ),
    )

    for forbidden_token in {
        "http_status",
        "type_uri",
        "title",
        "translation_key",
        "FastAPI",
        "JSONResponse",
        "problem_details",
        "ErrorDefinition",
        "context_schema",
    }:
        assert forbidden_token not in source
