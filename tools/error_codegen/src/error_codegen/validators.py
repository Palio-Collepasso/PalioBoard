"""Validation helpers for the error-code generation toolchain."""

# pyright: reportUnknownVariableType=false, reportUnknownArgumentType=false, reportUnknownMemberType=false

from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

from error_codegen.common import (
    DEFAULT_CATALOG_INDEX_PATH,
    DEFAULT_MODULES_ROOT,
    display_path,
    format_issue_message,
    location,
)
from error_codegen.models import CatalogValidationIssue


class CatalogValidationError(Exception):
    """Raised when the committed catalog is invalid."""

    def __init__(self, issues: list[CatalogValidationIssue]) -> None:
        """Store validation issues and expose them through the exception."""
        self.issues = tuple(issues)
        super().__init__(format_issue_message(self.issues))


def validate_import_alignment(
    imports: list[str],
    *,
    catalog_path: Path = DEFAULT_CATALOG_INDEX_PATH,
    modules_root: Path = DEFAULT_MODULES_ROOT,
    issues: list[CatalogValidationIssue],
) -> None:
    """Validate that imported fragment files match backend module ownership."""
    backend_modules = {
        module_dir.name
        for module_dir in modules_root.iterdir()
        if module_dir.is_dir() and not module_dir.name.startswith("__")
    }
    imported_modules = {Path(import_name).stem for import_name in imports}

    for import_name in imports:
        import_path = Path(import_name)
        if import_path.parent != Path("."):
            issues.append(
                CatalogValidationIssue(
                    location=location(catalog_path, f"imports.{import_name}"),
                    message=(
                        "Module-aligned catalog fragments must live at "
                        "docs/api/errors/<module>.yaml."
                    ),
                )
            )

    for missing_module in sorted(backend_modules - imported_modules):
        issues.append(
            CatalogValidationIssue(
                location=display_path(catalog_path),
                message=(
                    "Missing catalog fragment import for backend module "
                    f"`{missing_module}`."
                ),
            )
        )
    for extra_module in sorted(imported_modules - backend_modules):
        issues.append(
            CatalogValidationIssue(
                location=display_path(catalog_path),
                message=(
                    f"Catalog import `{extra_module}` does not match a backend module."
                ),
            )
        )


def normalize_context_schema(schema: object) -> object:
    """Normalize the authoring-only `required: true/false` extension."""
    if isinstance(schema, bool):
        return schema
    if not isinstance(schema, dict):
        return schema

    normalized: dict[str, Any] = {}
    existing_required = schema.get("required")
    required_fields = (
        list(existing_required) if isinstance(existing_required, list) else []
    )

    for key, value in schema.items():
        if key == "properties" and isinstance(value, dict):
            normalized_properties: dict[str, Any] = {}
            for property_name, property_schema in value.items():
                normalized_property_schema = normalize_context_schema(property_schema)
                if isinstance(normalized_property_schema, dict) and isinstance(
                    normalized_property_schema.get("required"), bool
                ):
                    is_required = normalized_property_schema.pop("required")
                    if is_required and property_name not in required_fields:
                        required_fields.append(property_name)
                normalized_properties[property_name] = normalized_property_schema
            normalized[key] = normalized_properties
            continue

        if key in {"items", "contains", "additionalProperties", "propertyNames"}:
            normalized[key] = normalize_context_schema(value)
            continue

        if key in {"allOf", "anyOf", "oneOf", "prefixItems"} and isinstance(
            value, list
        ):
            normalized[key] = [normalize_context_schema(item) for item in value]
            continue

        normalized[key] = value

    if _is_object_schema(normalized) and "additionalProperties" not in normalized:
        normalized["additionalProperties"] = False

    if isinstance(existing_required, list):
        normalized["required"] = existing_required
    elif required_fields:
        normalized["required"] = required_fields

    return normalized


def _is_object_schema(schema: dict[str, Any]) -> bool:
    """Return whether one schema node explicitly describes an object shape."""
    if "properties" in schema:
        return True
    schema_type = schema.get("type")
    if schema_type == "object":
        return True
    return isinstance(schema_type, list) and "object" in schema_type


def validate_context_references(
    schema: object,
    *,
    shared_context_schemas: dict[str, object],
    fragment_path: Path,
    code: str,
    issues: list[CatalogValidationIssue],
) -> None:
    """Validate that context-schema references stay within the catalog."""
    for reference, reference_path in _collect_references(schema):
        if not reference.startswith("#/shared_context_schemas/"):
            issues.append(
                CatalogValidationIssue(
                    location=location(
                        fragment_path, f"errors.{code}.context_schema{reference_path}"
                    ),
                    message=(
                        "Unsupported context-schema reference; only "
                        "`#/shared_context_schemas/<Name>` is supported."
                    ),
                )
            )
            continue

        shared_name = reference.removeprefix("#/shared_context_schemas/")
        if shared_name not in shared_context_schemas:
            issues.append(
                CatalogValidationIssue(
                    location=location(
                        fragment_path, f"errors.{code}.context_schema{reference_path}"
                    ),
                    message=f"Unknown shared context schema reference `{reference}`.",
                )
            )


def validate_example_context(
    *,
    code: str,
    fragment_path: Path,
    normalized_context_schema: object,
    shared_context_schemas: dict[str, object],
    example: object,
    issues: list[CatalogValidationIssue],
) -> None:
    """Validate that an authored example matches its declared context schema."""
    if not isinstance(example, dict):
        return
    example_context = example.get("context")
    if not isinstance(example_context, dict):
        return

    validation_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "shared_context_schemas": shared_context_schemas,
        "context_schema": normalized_context_schema,
        "$ref": "#/context_schema",
    }

    try:
        validator = Draft202012Validator(
            validation_schema,
            format_checker=Draft202012Validator.FORMAT_CHECKER,
        )
        errors = list(validator.iter_errors(example_context))
    except ValidationError as error:
        issues.append(
            CatalogValidationIssue(
                location=location(fragment_path, f"errors.{code}.example.context"),
                message=f"Invalid example context schema: {error.message}",
            )
        )
        return
    except Exception as error:  # pragma: no cover
        issues.append(
            CatalogValidationIssue(
                location=location(fragment_path, f"errors.{code}.example.context"),
                message=f"Unable to validate example context: {error}",
            )
        )
        return

    for error in errors:
        path_suffix = ".".join(str(component) for component in error.absolute_path)
        error_location = "example.context"
        if path_suffix:
            error_location = f"{error_location}.{path_suffix}"
        issues.append(
            CatalogValidationIssue(
                location=location(fragment_path, f"errors.{code}.{error_location}"),
                message=error.message,
            )
        )


def _collect_references(schema: object, path: str = "") -> list[tuple[str, str]]:
    references: list[tuple[str, str]] = []
    if isinstance(schema, dict):
        for key, value in schema.items():
            next_path = f"{path}.{key}" if path else f".{key}"
            if key == "$ref" and isinstance(value, str):
                references.append((value, next_path))
                continue
            references.extend(_collect_references(value, next_path))
    elif isinstance(schema, list):
        for index, value in enumerate(schema):
            references.extend(_collect_references(value, f"{path}[{index}]"))
    return references
