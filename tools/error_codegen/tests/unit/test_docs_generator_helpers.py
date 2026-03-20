"""Docs generator helper tests.

This file should enforce the section-injection contract only:
preserve handwritten content before and after `# Error Catalog` byte-for-byte,
replace only that section, be idempotent on rerun, and fail clearly when the
heading is missing.
It should not assert exact full-document snapshots or scenario traversal.
"""

import pytest

from error_codegen.generators.docs import (
    ERROR_CATALOG_HEADING,
    inject_error_catalog_section,
    render_error_catalog_section,
)
from support.sample_catalog import build_sample_catalog


def _base_document() -> str:
    """Build a document with handwritten prefix and suffix around the catalog."""
    return (
        "Preamble line 1\n"
        "Preamble line 2\n"
        "\n"
        f"{ERROR_CATALOG_HEADING}\n"
        "Old generated content that should be replaced.\n"
        "\n"
        "# Appendix\n"
        "Appendix body.\n"
    )


def _split_error_catalog_document(document: str) -> tuple[str, str, str]:
    """Split a document into prefix, catalog section, and suffix."""
    heading_start = document.index(ERROR_CATALOG_HEADING)
    next_heading_index = document.find("\n# ", heading_start + len(ERROR_CATALOG_HEADING))
    if next_heading_index == -1:
        next_heading_index = len(document)
    return (
        document[:heading_start],
        document[heading_start:next_heading_index],
        document[next_heading_index:],
    )


def test_render_error_catalog_section_is_section_only() -> None:
    """The section renderer should emit the generated catalog section only."""
    rendered = render_error_catalog_section(build_sample_catalog())

    assert rendered.startswith(f"{ERROR_CATALOG_HEADING}\n")
    assert "Preamble line 1" not in rendered
    assert "Appendix body" not in rendered
    assert "## Event Operations" in rendered
    assert "### JOLLY_ALREADY_USED" in rendered


def test_inject_error_catalog_section_preserves_handwritten_prefix_and_suffix() -> (
    None
):
    """Injection should keep handwritten content unchanged and replace only the catalog section."""
    section = render_error_catalog_section(build_sample_catalog())

    rendered = inject_error_catalog_section(_base_document(), section)
    prefix, actual_section, suffix = _split_error_catalog_document(rendered)
    expected_prefix, _, expected_suffix = _split_error_catalog_document(_base_document())

    assert prefix == expected_prefix
    assert actual_section == f"{section}\n"
    assert suffix == expected_suffix
    assert "Old generated content" not in rendered


def test_inject_error_catalog_section_is_idempotent() -> None:
    """Reinserting the same section should not change the rendered document."""
    section = render_error_catalog_section(build_sample_catalog())
    rendered = inject_error_catalog_section(_base_document(), section)

    assert inject_error_catalog_section(rendered, section) == rendered


def test_inject_error_catalog_section_rejects_missing_heading() -> None:
    """Documents without `# Error Catalog` should fail clearly."""
    section = render_error_catalog_section(build_sample_catalog())

    with pytest.raises(ValueError, match="`# Error Catalog` heading"):
        inject_error_catalog_section("Intro only\n\n# Appendix\nTail\n", section)
