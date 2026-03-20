"""Prototype only for CLI smoke coverage.

This file should eventually verify the intended CLI surface can drive the real
validate and generate commands with fixture-backed scenarios. It should not
carry compatibility coverage for removed option names or deeper generator
behavior. The final version should keep generated smoke artifacts in temporary
paths so `tools/error_codegen/tests/integration/_generated/` is not left behind.
"""

import tempfile
from pathlib import Path

from support.adapters import cli_runner


def _scenario_index(*parts: str) -> Path:
    """Return the path to one scenario catalog index fixture."""
    return (
        Path(__file__).resolve().parents[1]
        / "fixtures"
        / "scenarios"
        / Path(*parts)
        / "inputs"
        / "contracts"
        / "errors"
        / "index.yaml"
    )


def test_cli_validate_smoke_is_planned_for_a_success_scenario() -> None:
    """Validate smoke coverage should target a known-good scenario."""
    runner, app = cli_runner()
    result = runner.invoke(
        app,
        [
            "validate",
            "--catalog-index",
            str(
                _scenario_index(
                    "success", "simple", "single_error_with_required_context"
                )
            ),
        ],
    )

    assert result.exit_code == 0, result.output


def test_cli_validate_smoke_is_planned_for_a_failure_scenario() -> None:
    """Validate smoke coverage should target a known-bad scenario."""
    runner, app = cli_runner()
    result = runner.invoke(
        app,
        [
            "validate",
            "--catalog-index",
            str(_scenario_index("failure", "simple", "invalid_code_format")),
        ],
    )

    assert result.exit_code != 0
    assert (
        "code" in result.output.lower() or "upper_snake_case" in result.output.lower()
    )


def test_cli_generate_smoke_is_planned_for_python_typescript_and_docs_outputs() -> None:
    """Generate smoke coverage should target all three artifact kinds."""
    runner, app = cli_runner()
    scenario_index = _scenario_index("success", "medium", "split_catalog_two_modules")

    with tempfile.TemporaryDirectory() as tmp_dir:
        temp_root = Path(tmp_dir)
        output_root = temp_root / "python"
        ts_out = temp_root / "error-codes.gen.ts"
        docs_out = temp_root / "error-contract.md"

        result = runner.invoke(
            app,
            [
                "generate",
                "--catalog-index",
                str(scenario_index),
                "--python-out",
                str(output_root),
                "--typescript-out",
                str(ts_out),
                "--docs-out",
                str(docs_out),
                "--check",
            ],
        )

        assert result.exit_code == 0, result.output
        assert any(output_root.rglob("*.py"))
        assert ts_out.exists()
        assert docs_out.exists()
