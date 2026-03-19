from pathlib import Path

from error_codegen import generate_error_docs, load_error_catalog
from error_codegen.generators.docs import (
    render_error_catalog_section,
    render_error_contract,
    render_error_entry,
)
from support.error_catalog import (
    ERRORS_DIR,
    MODULE_IMPORTS,
    REPOSITORY_ROOT,
    fragment_with_error,
    write_catalog,
)


def test_render_error_entry_matches_example_contract(tmp_path: Path) -> None:
    catalog = load_error_catalog(
        catalog_path=write_catalog(
            output_dir=tmp_path,
            imports=list(MODULE_IMPORTS),
            fragments={
                "users.yaml": (ERRORS_DIR / "examples" / "example.yaml").read_text(
                    encoding="utf-8"
                )
            },
            base_type_uri="https://api.palioboard.local/problems/",
        )
    )
    entry = catalog.errors["JOLLY_ALREADY_USED"]

    assert render_error_entry(catalog, entry) == (
        (ERRORS_DIR / "examples" / "example.md").read_text(encoding="utf-8").rstrip()
    )


def test_render_error_catalog_section_groups_modules_in_import_order(
    tmp_path: Path,
) -> None:
    catalog = load_error_catalog(
        catalog_path=write_catalog(
            output_dir=tmp_path,
            imports=[
                "users.yaml",
                "audit.yaml",
                "authorization.yaml",
                "event_operations.yaml",
                "identity.yaml",
                "leaderboard_projection.yaml",
                "live_games.yaml",
                "public_read.yaml",
                "results.yaml",
                "season_setup.yaml",
                "tournaments.yaml",
            ],
            fragments={
                "users.yaml": fragment_with_error(
                    code="USER_MISSING",
                    type_slug="user-missing",
                    description="User could not be found.",
                    category="not_found",
                ),
                "audit.yaml": fragment_with_error(
                    code="AUDIT_UNAVAILABLE",
                    type_slug="audit-unavailable",
                    description="Audit service is unavailable.",
                    category="service_failure",
                ),
            },
            include_all_modules=False,
        )
    )

    section = render_error_catalog_section(catalog)

    assert section.index("## Users") < section.index("## Audit")
    assert "### USER_MISSING" in section
    assert "### AUDIT_UNAVAILABLE" in section


def test_generate_error_docs_writes_committed_document(tmp_path: Path) -> None:
    catalog_path = write_catalog(
        imports=list(MODULE_IMPORTS),
        fragments={},
        output_dir=tmp_path,
    )
    output_path = tmp_path / "error-contract.md"

    generated_path = generate_error_docs(
        catalog_path=catalog_path,
        output_path=output_path,
    )

    assert generated_path == output_path.resolve()
    assert generated_path.read_text(encoding="utf-8") == render_error_contract(
        load_error_catalog(catalog_path=catalog_path)
    )


def test_render_error_contract_matches_committed_document() -> None:
    committed_doc = (REPOSITORY_ROOT / "docs" / "api" / "error-contract.md").read_text(
        encoding="utf-8"
    )

    assert render_error_contract(load_error_catalog()) == committed_doc


def test_render_error_contract_describes_frontend_template_ownership() -> None:
    rendered = render_error_contract(load_error_catalog())

    assert "## Frontend rendering" in rendered
    assert "- match on stable `code`" in rendered
    assert "- read structured values from `context`" in rendered
    assert "It does not own final user-facing message text." in rendered
