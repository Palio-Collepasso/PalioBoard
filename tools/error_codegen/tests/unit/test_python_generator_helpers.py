"""Enforce Python generator helper behavior for the intended architecture.

This file should cover helper-level expectations such as module grouping, generated
Python validity, and domain-error-oriented invariants. It should not enforce exact
template formatting, API runtime behavior, or frontend generation behavior.
"""

import ast
import importlib
from pathlib import Path
from types import SimpleNamespace
from typing import Any


def _import_python_generator_module() -> Any:
    """Import the Python generator module using the repo-style path first."""
    candidates = [
        "tools.error_codegen.generators.python",
        "error_codegen.generators.python",
    ]
    last_error: Exception | None = None
    for name in candidates:
        try:
            return importlib.import_module(name)
        except Exception as error:  # pragma: no cover
            last_error = error
    raise AssertionError(
        f"Unable to import the Python generator module. Last error: {last_error}"
    )


def _resolve_attr(module: Any, candidates: list[str]) -> Any:
    """Resolve the first available attribute from a module."""
    for name in candidates:
        if hasattr(module, name):
            return getattr(module, name)
    raise AssertionError(f"Expected one of {candidates!r} in {module.__name__}.")


def _fake_entry(code: str, *, type_slug: str) -> Any:
    """Create a fake validated entry with the fields used by the Python template."""
    return SimpleNamespace(
        code=code,
        type_slug=type_slug,
        type_uri=f"https://api.palioboard.local/problems/{type_slug}",
        http_status=409,
        recommended_http_status=409,
        title=code.replace("_", " ").title(),
        description=None,
        category="business_rule",
        retry_policy="never",
        safe_to_expose=True,
        translation_key=f"errors.{code.lower()}",
        log_level=None,
        severity=None,
        normalized_context_schema={
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
        notes_for_operators=None,
    )


def test_render_module_source_contains_lookup_maps_and_exports() -> None:
    """Rendered Python source should include the key lookup maps and exported constants."""
    module = _import_python_generator_module()
    render_module_source = _resolve_attr(module, ["_render_module_source"])

    source = render_module_source(
        "event_operations",
        (
            _fake_entry("JOLLY_ALREADY_USED", type_slug="jolly-already-used"),
            _fake_entry("GAME_ALREADY_COMPLETED", type_slug="game-already-completed"),
        ),
    )

    assert "MODULE_NAME" in source
    assert "JOLLY_ALREADY_USED" in source
    assert "GAME_ALREADY_COMPLETED" in source
    assert "ERROR_BY_CODE" in source
    assert "ERROR_BY_TYPE_URI" in source
    assert "get_error" in source


def test_render_module_source_is_valid_python() -> None:
    """Generated module source should be syntactically valid Python."""
    module = _import_python_generator_module()
    render_module_source = _resolve_attr(module, ["_render_module_source"])

    source = render_module_source(
        "event_operations",
        (_fake_entry("JOLLY_ALREADY_USED", type_slug="jolly-already-used"),),
    )

    ast.parse(source)


def test_build_python_artifacts_creates_one_file_per_fragment(tmp_path: Path) -> None:
    """Artifact building should emit one generated file per module fragment."""
    module = _import_python_generator_module()
    build_artifacts = _resolve_attr(
        module,
        [
            "build_python_error_module_artifacts",
            "build_python_error_definition_artifacts",
        ],
    )

    fake_catalog = SimpleNamespace(
        fragments=(
            SimpleNamespace(
                module_name="event_operations",
                errors=(
                    _fake_entry("JOLLY_ALREADY_USED", type_slug="jolly-already-used"),
                ),
            ),
            SimpleNamespace(
                module_name="tournaments",
                errors=(
                    _fake_entry("TOURNAMENT_LOCKED", type_slug="tournament-locked"),
                ),
            ),
        )
    )

    artifacts = build_artifacts(fake_catalog, output_root=tmp_path)

    assert len(artifacts) == 2
    rendered_paths = {
        str(getattr(artifact, "output_path", getattr(artifact, "relative_path", "")))
        for artifact in artifacts
    }
    assert any("event_operations" in path for path in rendered_paths)
    assert any("tournaments" in path for path in rendered_paths)
