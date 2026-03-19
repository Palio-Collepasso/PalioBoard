import subprocess
import sys
from pathlib import Path

from typer.testing import CliRunner

from error_codegen.cli import app
from support.error_catalog import write_catalog


def test_cli_validate_command_prints_catalog_summary(tmp_path: Path) -> None:
    catalog_path = write_catalog(output_dir=tmp_path)

    result = CliRunner().invoke(app, ["validate", str(catalog_path)])

    assert result.exit_code == 0
    assert "Validated 11 module fragments" in result.stdout


def test_cli_generate_command_writes_python_ts_and_docs_outputs(tmp_path: Path) -> None:
    catalog_path = write_catalog(output_dir=tmp_path)
    output_root = tmp_path / "modules"
    ts_output = tmp_path / "generated" / "error-codes.generated.ts"
    docs_output = tmp_path / "generated" / "error-contract.md"

    result = CliRunner().invoke(
        app,
        [
            "generate",
            str(catalog_path),
            "--output-root",
            str(output_root),
            "--ts-output",
            str(ts_output),
            "--docs-output",
            str(docs_output),
        ],
    )

    assert result.exit_code == 0
    assert str(ts_output.resolve()) in result.stdout
    assert str(docs_output.resolve()) in result.stdout
    assert ts_output.exists()
    assert docs_output.exists()


def test_tools_package_import_does_not_pull_in_app_factory() -> None:
    command = [
        sys.executable,
        "-c",
        (
            "import sys; "
            "import error_codegen; "
            "raise SystemExit(1 if 'palio.app.factory' in sys.modules else 0)"
        ),
    ]

    result = subprocess.run(command, check=False, capture_output=True, text=True)

    assert result.returncode == 0, result.stderr
