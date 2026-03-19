"""Render human-readable API error documentation from the validated catalog."""

import json
import re
from pathlib import Path

from error_codegen.common import (
    REPOSITORY_ROOT,
    display_module_name,
    write_text_artifact,
)
from error_codegen.generators.common import render_template
from error_codegen.models import ErrorCatalog, ErrorCatalogEntry

DEFAULT_OUTPUT_PATH = REPOSITORY_ROOT / "docs" / "api" / "error-contract.md"
ERROR_CATALOG_HEADING = "# Error Catalog"
TOP_LEVEL_HEADING_PATTERN = re.compile(r"(?m)^# ")


def render_error_contract(
    catalog: ErrorCatalog,
    *,
    base_document: str | None = None,
) -> str:
    """Render the full markdown document by injecting the generated section."""
    if base_document is None:
        base_document = DEFAULT_OUTPUT_PATH.read_text(encoding="utf-8")
    return inject_error_catalog_section(
        base_document,
        render_error_catalog_section(catalog),
    )


def render_error_catalog_section(catalog: ErrorCatalog) -> str:
    """Render the generated `# Error Catalog` section."""
    return render_template(
        "error_contract.md.j2",
        module_sections=[
            {
                "title": display_module_name(fragment.module_name),
                "entries": [
                    render_error_entry(catalog, entry) for entry in fragment.errors
                ],
            }
            for fragment in catalog.fragments
        ],
    ).rstrip()


def inject_error_catalog_section(
    document: str,
    rendered_section: str,
) -> str:
    """Replace only the `# Error Catalog` section in a markdown document."""
    section_start = re.search(
        rf"(?m)^{re.escape(ERROR_CATALOG_HEADING)}\s*$",
        document,
    )
    if section_start is None:
        raise ValueError(
            "The target markdown document must contain a `# Error Catalog` heading."
        )

    remaining_document = document[section_start.end() :]
    section_end_match = TOP_LEVEL_HEADING_PATTERN.search(remaining_document)
    section_end = (
        section_start.end() + section_end_match.start()
        if section_end_match is not None
        else len(document)
    )

    prefix = document[: section_start.start()].rstrip("\n")
    suffix = document[section_end:].lstrip("\n")
    rendered_parts = [prefix, rendered_section.rstrip()]
    if suffix:
        rendered_parts.append(suffix)
    return "\n\n".join(part for part in rendered_parts if part).rstrip("\n") + "\n"


def render_error_entry(catalog: ErrorCatalog, entry: ErrorCatalogEntry) -> str:
    """Render one catalog entry using the human-readable example contract shape."""
    lines = [
        f"### {entry.code}",
        "",
        f"* **Type**: `{entry.type_uri}`",
        f"* **Category**: `{entry.category}`",
        f"* **HTTP status**: `{entry.http_status}`",
        f"* **Retry policy**: `{entry.retry_policy}`",
        f"* **Safe to expose**: `{str(entry.safe_to_expose).lower()}`",
        f"* **Translation key**: `{entry.translation_key}`",
    ]

    if entry.description:
        lines.extend(["", "#### Meaning", "", entry.description.strip()])

    context_schema = entry.normalized_context_schema
    if isinstance(context_schema, dict):
        lines.extend(
            [
                "",
                "#### Context schema",
                "",
                _render_context_schema_table(catalog, context_schema),
            ]
        )

    if entry.example is not None:
        lines.extend(
            [
                "",
                "#### Example",
                "",
                "```json",
                _render_problem_example(entry),
                "```",
            ]
        )

    return "\n".join(lines)


def write_error_contract(
    catalog: ErrorCatalog,
    output_path: Path = DEFAULT_OUTPUT_PATH,
) -> Path:
    """Write the error-contract document with only the catalog section refreshed."""
    resolved_output_path = output_path.resolve()
    base_document_path = (
        resolved_output_path if resolved_output_path.exists() else DEFAULT_OUTPUT_PATH
    )
    return write_text_artifact(
        output_path,
        render_error_contract(
            catalog,
            base_document=base_document_path.read_text(encoding="utf-8"),
        ),
    )


def _render_context_schema_table(
    catalog: ErrorCatalog,
    schema: dict[str, object],
) -> str:
    properties = schema.get("properties")
    if not isinstance(properties, dict) or not properties:
        return "_No structured context fields are declared._"

    required_fields = set()
    raw_required = schema.get("required")
    if isinstance(raw_required, list):
        required_fields = {field for field in raw_required if isinstance(field, str)}

    rows: list[list[str]] = []
    for field_name, field_schema in properties.items():
        if not isinstance(field_name, str):
            continue
        rows.append(
            [
                f"`{field_name}`",
                f"`{_describe_schema(catalog, field_schema)}`",
                "yes" if field_name in required_fields else "no",
                _render_schema_notes(field_schema),
            ]
        )

    return _render_markdown_table(
        ["Field", "Type", "Required", "Notes"],
        rows,
        right_aligned_columns={2},
    )


def _render_schema_notes(schema: object) -> str:
    if not isinstance(schema, dict):
        return ""
    description = schema.get("description")
    if not isinstance(description, str):
        return ""
    return " ".join(description.split())


def _describe_schema(catalog: ErrorCatalog, schema: object) -> str:
    if isinstance(schema, bool):
        return "any" if schema else "none"
    if not isinstance(schema, dict):
        return "any"

    reference = schema.get("$ref")
    if isinstance(reference, str):
        resolved_schema = _resolve_schema_reference(catalog, reference)
        if resolved_schema is not None:
            return _describe_schema(catalog, resolved_schema)
        return reference

    schema_type = schema.get("type")
    if isinstance(schema_type, str):
        return _describe_schema_type(schema_type, schema)
    if isinstance(schema_type, list):
        return " | ".join(
            _describe_schema_type(schema_type_name, schema)
            for schema_type_name in schema_type
            if isinstance(schema_type_name, str)
        )

    enum_values = schema.get("enum")
    if isinstance(enum_values, list) and enum_values:
        return " | ".join(str(value) for value in enum_values)

    if isinstance(schema.get("properties"), dict):
        return "object"
    if "items" in schema:
        return "array"
    return "any"


def _describe_schema_type(schema_type: str, schema: dict[str, object]) -> str:
    if schema_type == "string":
        format_name = schema.get("format")
        if format_name == "uuid":
            return "uuid"
        if isinstance(format_name, str):
            return f"string ({format_name})"
        return "string"
    return schema_type


def _resolve_schema_reference(
    catalog: ErrorCatalog,
    reference: str,
) -> object | None:
    prefix = "#/shared_context_schemas/"
    if not reference.startswith(prefix):
        return None
    return catalog.shared_context_schemas.get(reference.removeprefix(prefix))


def _render_problem_example(entry: ErrorCatalogEntry) -> str:
    example = dict(entry.example or {})
    problem_example: dict[str, object] = {
        "type": entry.type_uri,
        "code": entry.code,
        "title": entry.title,
        "status": entry.http_status,
    }
    detail = example.get("detail")
    if isinstance(detail, str):
        problem_example["detail"] = detail
    context = example.get("context")
    problem_example["context"] = context if isinstance(context, dict) else {}
    return json.dumps(problem_example, indent=2)


def _render_problem_example_template() -> dict[str, object]:
    return {
        "type": "https://api.palioboard.local/problems/jolly-already-used",
        "code": "JOLLY_ALREADY_USED",
        "title": "Jolly already used",
        "status": 409,
        "context": {
            "team_id": "01956c9f-6f7e-7b42-a4b0-2d21d920c001",
            "game_id": "01956ca0-0c77-7b98-a328-39c9f8a31002",
            "previous_game_id": "01956ca0-53dd-7162-b78a-4bdb9368b003",
        },
    }


def _render_markdown_table(
    headers: list[str],
    rows: list[list[str]],
    *,
    right_aligned_columns: set[int] | None = None,
) -> str:
    right_aligned_columns = right_aligned_columns or set()
    if rows:
        columns = list(zip(*[headers, *rows], strict=False))
    else:
        columns = [[header] for header in headers]
    widths = [max(len(cell) for cell in column) for column in columns]

    def format_row(row: list[str]) -> str:
        cells = []
        for index, cell in enumerate(row):
            width = widths[index]
            cells.append(
                cell.rjust(width)
                if index in right_aligned_columns
                else cell.ljust(width)
            )
        return "| " + " | ".join(cells) + " |"

    separator = []
    for index, width in enumerate(widths):
        separator.append(
            "-" * max(width - 1, 1) + ":"
            if index in right_aligned_columns
            else "-" * width
        )

    return "\n".join(
        [
            format_row(headers),
            "| " + " | ".join(separator) + " |",
            *(format_row(row) for row in rows),
        ]
    )
