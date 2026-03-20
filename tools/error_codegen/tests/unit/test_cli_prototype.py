"""Enforce the public CLI help contract only.

This file should verify command names, supported options, and public help wording
for the intended CLI surface. It should not enforce runtime generation or
validation behavior.
"""

import re

from typer.testing import CliRunner

from error_codegen.cli import app


def _help(*args: str) -> str:
    runner = CliRunner()
    result = runner.invoke(
        app,
        [*args, "--help"],
        prog_name="error-codegen",
        color=False,
        terminal_width=140,
    )
    assert result.exit_code == 0, result.output
    return result.output


def _normalized_help(*args: str) -> str:
    output = _help(*args)
    output = re.sub(r"[│╭╮╰╯─]+", " ", output)
    return re.sub(r"\s+", " ", output).strip()


def test_root_help_matches_requested_prototype() -> None:
    output = _normalized_help()

    assert "Usage: error-codegen [OPTIONS] COMMAND [ARGS]..." in output
    assert "Validate the error catalog and generate shared error artifacts." in output
    assert "The catalog is the single source of truth for:" in output
    assert "- error identifiers" in output
    assert "- HTTP transport metadata" in output
    assert "- safe-to-expose context schema" in output
    assert "Generated artifacts include:" in output
    assert "- Python module-local error definitions" in output
    assert "- frontend TypeScript error metadata" in output
    assert "- Markdown error contract documentation" in output
    assert "validate Validate the error catalog." in output
    assert "generate Generate Python, TypeScript, and Markdown artifacts." in output


def test_validate_help_matches_requested_prototype() -> None:
    output = _normalized_help("validate")

    assert "Usage: error-codegen validate [OPTIONS]" in output
    assert "Validate the error catalog." in output
    assert "This command checks:" in output
    assert "- YAML/schema structure" in output
    assert "- per-entry semantic rules" in output
    assert "- cross-catalog invariants" in output
    assert "- context schema consistency" in output
    assert "--catalog-index PATH" in output
    assert "Path to the root catalog index.yaml." in output
    assert "[default:" in output
    assert "contracts/errors/index" in output
    assert "--json" in output
    assert "Output validation results as JSON." in output
    assert "--fail-fast" in output
    assert "--no-fail-fast" in output
    assert "Stop at the first validation error." in output
    assert "[default: no-fail-fast]" in output
    assert "--catalog-index-path" not in output
    assert "--schema" not in output
    assert "--format" not in output


def test_generate_help_matches_requested_prototype() -> None:
    output = _normalized_help("generate")

    assert "Usage: error-codegen generate [OPTIONS]" in output
    assert "Generate all shared error artifacts from the catalog." in output
    assert "Generated outputs:" in output
    assert "- Python module-local error definitions" in output
    assert "- TypeScript frontend error metadata" in output
    assert "- Markdown error contract documentation" in output
    assert "--catalog-index PATH" in output
    assert "[default:" in output
    assert "contracts/errors/index" in output
    assert "--python-out PATH" in output
    assert "Output directory for generated Python module files." in output
    assert "apps/api/app/modules" in output
    assert "--typescript-out PATH" in output
    assert "Output file for generated TypeScript artifact." in output
    assert "apps/web/src/shared/api/error-code" in output
    assert "--docs-out PATH" in output
    assert "Output file for generated Markdown documentation." in output
    assert "docs/api/error-contract.md" in output
    assert "--check" in output
    assert "--no-check" in output
    assert "Validate the catalog before generating artifacts." in output
    assert "[default: check]" in output
    assert "--python-output-root" not in output
    assert "--typescript-output-path" not in output
    assert "--docs-output-path" not in output
    assert "--document-title" not in output
    assert "--schema" not in output
