from pathlib import Path

from error_codegen.generators.docs import (
    inject_error_catalog_section,
    render_error_catalog_section,
    render_error_contract,
    render_error_entry,
)
from support.catalog_paths import snapshot_path
from support.sample_catalog import build_sample_catalog


def test_render_error_entry_matches_example_contract() -> None:
    catalog = build_sample_catalog()
    entry = catalog.errors["JOLLY_ALREADY_USED"]
    example_path = (
        Path(__file__).resolve().parents[4]
        / "docs"
        / "api"
        / "errors"
        / "examples"
        / "example.md"
    )

    assert (
        render_error_entry(catalog, entry)
        == example_path.read_text(encoding="utf-8").rstrip()
    )


def test_render_error_catalog_section_preserves_import_order() -> None:
    section = render_error_catalog_section(build_sample_catalog())

    assert section.index("## Audit") < section.index("## Event Operations")
    assert "### JOLLY_ALREADY_USED" in section


def test_render_error_catalog_section_matches_snapshot() -> None:
    assert render_error_catalog_section(build_sample_catalog()) == (
        snapshot_path("docs", "error-catalog-section.md")
        .read_text(encoding="utf-8")
        .rstrip()
    )


def test_render_error_contract_preserves_handwritten_content() -> None:
    rendered = render_error_contract(
        build_sample_catalog(),
        base_document=snapshot_path("docs", "error-contract-base.md").read_text(
            encoding="utf-8"
        ),
    )

    assert "## Frontend rendering" in rendered
    assert "- match on stable `code`" in rendered
    assert "- read structured values from `context`" in rendered
    assert rendered == snapshot_path("docs", "error-contract.md").read_text(
        encoding="utf-8"
    )


def test_inject_error_catalog_section_requires_heading() -> None:
    try:
        inject_error_catalog_section("## Missing heading\n", "# Error Catalog\n")
    except ValueError as error:
        assert "`# Error Catalog` heading" in str(error)
    else:  # pragma: no cover - defensive assertion branch
        raise AssertionError("Expected missing heading to be rejected.")
