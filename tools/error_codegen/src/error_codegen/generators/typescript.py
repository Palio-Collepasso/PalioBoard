"""Generate frontend TypeScript artifacts from the validated error catalog."""

import json
from pathlib import Path
from typing import Any

from error_codegen.common import (
    REPOSITORY_ROOT,
    pascal_case,
    write_text_artifact,
)
from error_codegen.generators.common import render_template
from error_codegen.models import ErrorCatalog, ErrorCatalogEntry

GENERATED_FILENAME = "error-codes.generated.ts"
DEFAULT_OUTPUT_PATH = (
    REPOSITORY_ROOT
    / "apps"
    / "web"
    / "src"
    / "app"
    / "shared"
    / "api"
    / "generated"
    / GENERATED_FILENAME
)


def generate_typescript_error_artifact(catalog: ErrorCatalog) -> str:
    """Render the committed frontend error catalog artifact."""
    module_names = catalog.module_names
    errors_by_module = {
        module_name: catalog.errors_for_module(module_name)
        for module_name in module_names
    }
    error_entries = [
        entry
        for module_entries in errors_by_module.values()
        for entry in module_entries
    ]
    shared_context_aliases = {
        name: _shared_context_alias_name(name)
        for name in sorted(catalog.shared_context_schemas)
    }
    error_context_aliases = {
        entry.code: _context_alias_name(entry.code) for entry in error_entries
    }

    return render_template(
        "ts_error_codes.ts.j2",
        module_names_json=json.dumps(list(module_names), indent=2),
        error_codes_json=json.dumps([entry.code for entry in error_entries], indent=2),
        shared_context_definitions=[
            {
                "alias_name": shared_context_aliases[name],
                "rendered_schema": _render_schema_type(
                    catalog.shared_context_schemas[name],
                    shared_context_aliases,
                ),
            }
            for name in sorted(catalog.shared_context_schemas)
        ],
        error_context_definitions=[
            {
                "code": entry.code,
                "alias_name": error_context_aliases[entry.code],
                "rendered_schema": _render_schema_type(
                    entry.normalized_context_schema,
                    shared_context_aliases,
                ),
            }
            for entry in error_entries
        ],
        error_context_rows=[
            f"  {entry.code}: {error_context_aliases[entry.code]};"
            for entry in error_entries
        ],
        error_metadata_rows=[
            f"  {entry.code}: CatalogErrorMetadata<{json.dumps(entry.code)}>;"
            for entry in error_entries
        ],
        error_metadata_entries=[
            _render_error_metadata(entry) for entry in error_entries
        ],
        module_code_entries=[
            {
                "module_name_json": json.dumps(module_name),
                "module_codes_json": json.dumps(
                    [entry.code for entry in errors_by_module[module_name]],
                    indent=2,
                ),
            }
            for module_name in module_names
        ],
        catalog_problem_entries=[
            _render_catalog_problem_entry(entry, shared_context_aliases)
            for entry in error_entries
        ],
    )


def write_typescript_error_artifact(
    catalog: ErrorCatalog,
    output_path: Path = DEFAULT_OUTPUT_PATH,
) -> Path:
    """Write the generated TypeScript artifact to disk."""
    return write_text_artifact(output_path, generate_typescript_error_artifact(catalog))


def _render_error_metadata(entry: ErrorCatalogEntry) -> str:
    metadata = {
        "moduleName": entry.module_name,
        "code": entry.code,
        "type": entry.type_uri,
        "status": entry.recommended_http_status,
        "title": entry.title,
        "category": entry.category,
        "retryPolicy": entry.retry_policy,
        "safeToExpose": entry.safe_to_expose,
        "translationKey": entry.translation_key,
        "contextSchema": entry.normalized_context_schema,
    }
    if entry.description is not None:
        metadata["description"] = entry.description
    if entry.log_level is not None:
        metadata["logLevel"] = entry.log_level
    if entry.severity is not None:
        metadata["severity"] = entry.severity

    return (
        f"  {json.dumps(entry.code)}: {json.dumps(metadata, indent=2, sort_keys=True)},"
    )


def _render_catalog_problem_entry(
    entry: ErrorCatalogEntry,
    shared_context_aliases: dict[str, str],
) -> str:
    rendered_context = _render_schema_type(
        entry.normalized_context_schema,
        shared_context_aliases,
    )
    rendered_code = json.dumps(entry.code)
    return f"  {entry.code}: CatalogProblem<{rendered_code}, {rendered_context}>;"


def _render_schema_type(
    schema: object,
    shared_context_aliases: dict[str, str],
    *,
    path: tuple[str, ...] = (),
) -> str:
    if schema is True:
        return "unknown"
    if schema is False:
        return "never"
    if not isinstance(schema, dict):
        return "unknown"

    if "$ref" in schema:
        reference = schema["$ref"]
        if isinstance(reference, str) and reference.startswith(
            "#/shared_context_schemas/"
        ):
            ref_name = reference.removeprefix("#/shared_context_schemas/")
            return shared_context_aliases.get(ref_name, "unknown")
        return "unknown"

    if "const" in schema:
        return _render_literal(schema["const"])

    if "enum" in schema and isinstance(schema["enum"], list):
        values = [_render_literal(value) for value in schema["enum"]]
        return " | ".join(values) if values else "never"

    if "oneOf" in schema and isinstance(schema["oneOf"], list):
        return _join_variants(schema["oneOf"], shared_context_aliases, separator=" | ")

    if "anyOf" in schema and isinstance(schema["anyOf"], list):
        return _join_variants(schema["anyOf"], shared_context_aliases, separator=" | ")

    if "allOf" in schema and isinstance(schema["allOf"], list):
        return _join_variants(schema["allOf"], shared_context_aliases, separator=" & ")

    schema_type = schema.get("type")
    if isinstance(schema_type, list):
        return " | ".join(
            _render_schema_type({"type": value}, shared_context_aliases, path=path)
            for value in schema_type
        )

    if schema_type == "object" or "properties" in schema:
        return _render_object_type(schema, shared_context_aliases, path=path)

    if schema_type == "array":
        return _render_array_type(schema, shared_context_aliases, path=path)

    if schema_type == "string":
        return "string"
    if schema_type in {"integer", "number"}:
        return "number"
    if schema_type == "boolean":
        return "boolean"
    if schema_type == "null":
        return "null"

    return "unknown"


def _render_object_type(
    schema: dict[str, Any],
    shared_context_aliases: dict[str, str],
    *,
    path: tuple[str, ...],
) -> str:
    properties = schema.get("properties")
    if not isinstance(properties, dict):
        additional_properties = schema.get("additionalProperties", True)
        if additional_properties is False:
            return "{}"
        if additional_properties is True:
            return "Record<string, unknown>"
        rendered_additional_properties = _render_schema_type(
            additional_properties,
            shared_context_aliases,
            path=path,
        )
        return f"Record<string, {rendered_additional_properties}>"

    required = {value for value in schema.get("required", []) if isinstance(value, str)}
    property_lines: list[str] = []
    for property_name in sorted(properties):
        property_schema = properties[property_name]
        property_type = _render_schema_type(
            property_schema,
            shared_context_aliases,
            path=(*path, property_name),
        )
        optional_marker = "" if property_name in required else "?"
        property_lines.append(
            f"  {json.dumps(property_name)}{optional_marker}: {property_type};"
        )

    additional_properties = schema.get("additionalProperties", True)
    if additional_properties is False:
        if not property_lines:
            return "{}"
        return "{\n" + "\n".join(property_lines) + "\n}"

    if additional_properties is True:
        property_lines.append("  [key: string]: unknown;")
        return "{\n" + "\n".join(property_lines) + "\n}"

    rendered_additional_properties = _render_schema_type(
        additional_properties,
        shared_context_aliases,
        path=path,
    )
    property_lines.append(f"  [key: string]: {rendered_additional_properties};")
    return "{\n" + "\n".join(property_lines) + "\n}"


def _render_array_type(
    schema: dict[str, Any],
    shared_context_aliases: dict[str, str],
    *,
    path: tuple[str, ...],
) -> str:
    prefix_items = schema.get("prefixItems")
    if isinstance(prefix_items, list) and prefix_items:
        tuple_items = ", ".join(
            _render_schema_type(item, shared_context_aliases, path=(*path, str(index)))
            for index, item in enumerate(prefix_items)
        )
        return f"[{tuple_items}]"

    items = schema.get("items", True)
    rendered_items = _render_schema_type(
        items,
        shared_context_aliases,
        path=path,
    )
    return f"ReadonlyArray<{rendered_items}>"


def _join_variants(
    variants: list[Any],
    shared_context_aliases: dict[str, str],
    *,
    separator: str,
) -> str:
    rendered = [
        _render_schema_type(variant, shared_context_aliases) for variant in variants
    ]
    return separator.join(rendered) if rendered else "never"


def _render_literal(value: object) -> str:
    if isinstance(value, str):
        return json.dumps(value)
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    return json.dumps(value)


def _shared_context_alias_name(name: str) -> str:
    return f"SharedContext{pascal_case(name)}"


def _context_alias_name(code: str) -> str:
    return f"{pascal_case(code)}Context"
