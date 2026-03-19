from pathlib import Path

import pytest

from error_codegen import (
    CatalogValidationError,
    load_error_catalog,
    validate_error_catalog,
)
from support.catalog_paths import materialize_catalog_fixture


def test_load_error_catalog_reads_valid_sample_fixture(tmp_path: Path) -> None:
    catalog_path = materialize_catalog_fixture(
        "sample", kind="valid", output_dir=tmp_path
    )

    catalog = load_error_catalog(catalog_path=catalog_path)

    assert catalog.module_names[2] == "event_operations"
    assert tuple(catalog.errors) == ("JOLLY_ALREADY_USED",)
    assert "UuidRef" in catalog.shared_context_schemas


def test_validate_error_catalog_returns_summary_for_valid_sample_fixture(
    tmp_path: Path,
) -> None:
    catalog_path = materialize_catalog_fixture(
        "sample", kind="valid", output_dir=tmp_path
    )

    summary = validate_error_catalog(catalog_path=catalog_path)

    assert summary == (
        "Validated 11 module fragments, 1 error entries, and 1 shared context schemas."
    )


def test_load_error_catalog_reports_duplicate_symbolic_code(tmp_path: Path) -> None:
    catalog_path = materialize_catalog_fixture(
        "duplicate_code",
        kind="invalid",
        output_dir=tmp_path,
    )

    with pytest.raises(CatalogValidationError) as error:
        load_error_catalog(catalog_path=catalog_path)

    assert "Duplicate symbolic error code" in str(error.value)


def test_load_error_catalog_reports_unknown_shared_context_reference(
    tmp_path: Path,
) -> None:
    catalog_path = materialize_catalog_fixture(
        "unknown_shared_context_reference",
        kind="invalid",
        output_dir=tmp_path,
    )

    with pytest.raises(CatalogValidationError) as error:
        load_error_catalog(catalog_path=catalog_path)

    assert "Unknown shared context schema reference" in str(error.value)


def test_load_error_catalog_reports_invalid_example_context(tmp_path: Path) -> None:
    catalog_path = materialize_catalog_fixture(
        "invalid_example_context",
        kind="invalid",
        output_dir=tmp_path,
    )

    with pytest.raises(CatalogValidationError) as error:
        load_error_catalog(catalog_path=catalog_path)

    assert "is not a 'uuid'" in str(error.value)
