"""Enforce the intended CLI smoke path only.

This file should verify the supported commands and options can drive validation
and artifact generation through the real Typer app. It should not carry
compatibility coverage for removed option names.
"""

from pathlib import Path

from support.adapters import cli_runner


def test_cli_validate_accepts_a_success_scenario() -> None:
    """The validate command should succeed on a known-good scenario."""
    runner, app = cli_runner()
    scenario_index = (
        Path(__file__).resolve().parents[1]
        / "fixtures"
        / "scenarios"
        / "success"
        / "simple"
        / "single_error_with_required_context"
        / "contracts"
        / "errors"
        / "index.yaml"
    )
    result = runner.invoke(
        app, ["validate", "--catalog-index-path", str(scenario_index)]
    )
    assert result.exit_code == 0, result.output


def test_cli_validate_rejects_a_failure_scenario() -> None:
    """The validate command should fail on a known-bad scenario."""
    runner, app = cli_runner()
    scenario_index = (
        Path(__file__).resolve().parents[1]
        / "fixtures"
        / "scenarios"
        / "failure"
        / "simple"
        / "invalid_code_format"
        / "contracts"
        / "errors"
        / "index.yaml"
    )
    result = runner.invoke(
        app, ["validate", "--catalog-index-path", str(scenario_index)]
    )
    assert result.exit_code != 0
    assert (
        "code" in result.output.lower() or "upper_snake_case" in result.output.lower()
    )


def test_cli_generate_writes_python_typescript_and_docs_outputs(tmp_path: Path) -> None:
    """The generate command should emit all expected artifact kinds."""
    runner, app = cli_runner()
    scenario_index = (
        Path(__file__).resolve().parents[1]
        / "fixtures"
        / "scenarios"
        / "success"
        / "medium"
        / "split_catalog_two_modules"
        / "contracts"
        / "errors"
        / "index.yaml"
    )

    python_out = tmp_path / "python"
    ts_out = tmp_path / "typescript" / "error-codes.gen.ts"
    docs_out = tmp_path / "docs" / "error-contract.md"

    result = runner.invoke(
        app,
        [
            "generate",
            "--catalog-index-path",
            str(scenario_index),
            "--python-output-root",
            str(python_out),
            "--typescript-output-path",
            str(ts_out),
            "--docs-output-path",
            str(docs_out),
            "--document-title",
            "Medium success — split_catalog_two_modules",
        ],
    )
    assert result.exit_code == 0, result.output

    python_files = sorted(python_out.rglob("*.py"))
    assert python_files
    assert ts_out.exists()
    assert docs_out.exists()
    assert "error" in ts_out.read_text(encoding="utf-8").lower()
    assert "error" in docs_out.read_text(encoding="utf-8").lower()
