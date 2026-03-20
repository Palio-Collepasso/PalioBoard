"""Enforce docs generator helper behavior for section injection.

This file should cover replacing only the generated Error Catalog section,
preserving surrounding handwritten content, and idempotence or missing-heading
failure behavior. It should not depend on broad scenario traversal.
"""

from __future__ import annotations

import importlib
from types import SimpleNamespace
from typing import Any


def _import_docs_generator_module() -> Any:
    """Import the docs generator module using the repo-style path first."""
    candidates = ['tools.error_codegen.generators.docs', 'error_codegen.generators.docs']
    last_error: Exception | None = None
    for name in candidates:
        try:
            return importlib.import_module(name)
        except Exception as error:  # pragma: no cover
            last_error = error
    raise AssertionError(f'Unable to import the docs generator module. Last error: {last_error}')


def _resolve_attr(module: Any, candidates: list[str]) -> Any:
    """Resolve the first available attribute from a module."""
    for name in candidates:
        if hasattr(module, name):
            return getattr(module, name)
    raise AssertionError(f'Expected one of {candidates!r} in {module.__name__}.')


def _fake_catalog() -> Any:
    """Create a minimal fake catalog with no shared schemas."""
    return SimpleNamespace(shared_context_schemas={})


def _fake_entry() -> Any:
    """Create a fake error entry with context and example data."""
    return SimpleNamespace(
        code='JOLLY_ALREADY_USED',
        type_uri='https://api.palioboard.local/problems/jolly-already-used',
        category='business_rule',
        http_status=409,
        recommended_http_status=409,
        title='Jolly already used',
        translation_key='errors.jollyAlreadyUsed',
        safe_to_expose=True,
        description='The team has already spent its Jolly in another game.',
        retry_policy='never',
        normalized_context_schema={
            'type': 'object',
            'additionalProperties': False,
            'properties': {
                'team_id': {'type': 'string', 'format': 'uuid', 'description': 'Owning team id.'},
                'previous_game_id': {'type': 'string'},
            },
            'required': ['team_id'],
        },
        example={'detail': None, 'context': {'team_id': 'team-001', 'previous_game_id': 'game-002'}},
    )


def test_render_markdown_table_aligns_right_aligned_columns() -> None:
    """Markdown table rendering should right-align selected columns."""
    module = _import_docs_generator_module()
    render_table = _resolve_attr(module, ['_render_markdown_table'])

    table = render_table(
        ['Field', 'Required'],
        [['`team_id`', 'yes'], ['`previous_game_id`', 'no']],
        right_aligned_columns={1},
    )

    assert '| Field              | Required |' in table
    assert '| ------------------ | -------: |' in table


def test_describe_schema_type_prefers_format_for_strings() -> None:
    """String schema descriptions should surface special formats like UUID."""
    module = _import_docs_generator_module()
    describe_type = _resolve_attr(module, ['_describe_schema_type'])

    assert describe_type('string', {'format': 'uuid'}) == 'uuid'
    assert describe_type('string', {'format': 'date-time'}) == 'string (date-time)'
    assert describe_type('integer', {}) == 'integer'


def test_render_error_entry_includes_context_table_and_example() -> None:
    """Rendered entry docs should include the schema table and JSON example."""
    module = _import_docs_generator_module()
    render_error_entry = _resolve_attr(module, ['render_error_entry'])

    rendered = render_error_entry(_fake_catalog(), _fake_entry())

    assert '### JOLLY_ALREADY_USED' in rendered
    assert '#### Context schema' in rendered
    assert '`team_id`' in rendered
    assert '#### Example' in rendered
    assert '"previous_game_id": "game-002"' in rendered
