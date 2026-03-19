from pathlib import Path

from error_codegen import generate_error_artifacts
from error_codegen.generators.python import (
    GENERATED_FILENAME as PYTHON_GENERATED_FILENAME,
)
from support.catalog_paths import (
    load_module_from_path,
    materialize_catalog_fixture,
    snapshot_path,
)


def test_generate_error_artifacts_writes_full_outputs_from_valid_fixture(
    tmp_path: Path,
) -> None:
    catalog_path = materialize_catalog_fixture(
        "sample", kind="valid", output_dir=tmp_path
    )
    output_root = tmp_path / "modules"
    ts_output = tmp_path / "generated" / "error-codes.generated.ts"
    docs_output = tmp_path / "generated" / "error-contract.md"
    docs_output.parent.mkdir(parents=True, exist_ok=True)
    docs_output.write_text(
        snapshot_path("docs", "error-contract-base.md").read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    written_paths = generate_error_artifacts(
        catalog_path=catalog_path,
        python_output_root=output_root,
        typescript_output_path=ts_output,
        docs_output_path=docs_output,
    )

    assert len(written_paths) == 13
    assert (output_root / "event_operations" / PYTHON_GENERATED_FILENAME).exists()
    assert ts_output.exists()
    assert docs_output.exists()


def test_generate_error_artifacts_match_snapshots(tmp_path: Path) -> None:
    catalog_path = materialize_catalog_fixture(
        "sample", kind="valid", output_dir=tmp_path
    )
    output_root = tmp_path / "modules"
    ts_output = tmp_path / "generated" / "error-codes.generated.ts"
    docs_output = tmp_path / "generated" / "error-contract.md"
    docs_output.parent.mkdir(parents=True, exist_ok=True)
    docs_output.write_text(
        snapshot_path("docs", "error-contract-base.md").read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    generate_error_artifacts(
        catalog_path=catalog_path,
        python_output_root=output_root,
        typescript_output_path=ts_output,
        docs_output_path=docs_output,
    )

    python_output = output_root / "event_operations" / PYTHON_GENERATED_FILENAME
    assert python_output.read_text(encoding="utf-8") == snapshot_path(
        "python", "event_operations_error_defs_gen.py"
    ).read_text(encoding="utf-8")
    assert ts_output.read_text(encoding="utf-8") == snapshot_path(
        "typescript", "error-codes.generated.ts"
    ).read_text(encoding="utf-8")
    assert docs_output.read_text(encoding="utf-8") == snapshot_path(
        "docs", "error-contract.md"
    ).read_text(encoding="utf-8")

    generated_module = load_module_from_path(
        python_output,
        module_name="generated_event_operations_error_defs",
    )
    assert generated_module.JOLLY_ALREADY_USED.code == "JOLLY_ALREADY_USED"
    assert generated_module.JOLLY_ALREADY_USED.http_status == 409
