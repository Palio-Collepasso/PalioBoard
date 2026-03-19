"""Load and validate the committed API error catalog."""

# pyright: reportUnknownVariableType=false, reportUnknownArgumentType=false, reportUnknownMemberType=false

import json
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator
from pydantic import BaseModel
from pydantic import ValidationError as PydanticValidationError

from error_codegen.common import (
    DEFAULT_CATALOG_INDEX_PATH,
    DEFAULT_SCHEMA_PATH,
    display_path,
    location,
    sort_issues,
)
from error_codegen.models import (
    CatalogValidationIssue,
    ErrorCatalog,
    ErrorCatalogEntry,
    ErrorCatalogFragment,
    FragmentCatalogDocument,
    RootCatalogDocument,
)
from error_codegen.validators import (
    CatalogValidationError,
    normalize_context_schema,
    validate_context_references,
    validate_example_context,
    validate_import_alignment,
)


def load_error_catalog(
    catalog_path: Path = DEFAULT_CATALOG_INDEX_PATH,
    schema_path: Path = DEFAULT_SCHEMA_PATH,
) -> ErrorCatalog:
    """Load, validate, and merge the committed error catalog."""
    schema = _load_schema(schema_path)
    index_validator = _build_validator(schema)
    fragment_validator = _build_validator(_build_fragment_schema(schema))

    issues: list[CatalogValidationIssue] = []
    raw_catalog_document = _load_yaml_document(catalog_path, issues)
    if raw_catalog_document is None:
        raise CatalogValidationError(sort_issues(issues))

    _schema_errors(raw_catalog_document, catalog_path, index_validator, issues)
    if issues:
        raise CatalogValidationError(sort_issues(issues))

    catalog_document = _parse_document(
        RootCatalogDocument,
        raw_catalog_document,
        source_path=catalog_path,
        issues=issues,
    )
    if catalog_document is None:
        raise CatalogValidationError(sort_issues(issues))

    validate_import_alignment(
        catalog_document.imports,
        catalog_path=catalog_path,
        issues=issues,
    )
    shared_context_schemas = {
        name: normalize_context_schema(schema_value)
        for name, schema_value in catalog_document.shared_context_schemas.items()
    }

    fragments: list[ErrorCatalogFragment] = []
    merged_errors: dict[str, ErrorCatalogEntry] = {}
    seen_type_slugs: dict[str, Path] = {}
    seen_type_uris: dict[str, Path] = {}

    for relative_import_path in catalog_document.imports:
        fragment_path = (catalog_path.parent / relative_import_path).resolve()
        if catalog_path.parent.resolve() not in fragment_path.parents:
            issues.append(
                CatalogValidationIssue(
                    location=location(catalog_path, relative_import_path),
                    message="Catalog imports must stay under docs/api/errors/.",
                )
            )
            continue

        raw_fragment_document = _load_yaml_document(fragment_path, issues)
        if raw_fragment_document is None:
            continue

        schema_issue_count = len(issues)
        _schema_errors(
            raw_fragment_document,
            fragment_path,
            fragment_validator,
            issues,
        )
        if len(issues) > schema_issue_count:
            continue

        fragment_document = _parse_document(
            FragmentCatalogDocument,
            raw_fragment_document,
            source_path=fragment_path,
            issues=issues,
        )
        if fragment_document is None:
            continue

        module_name = Path(relative_import_path).stem
        entries: list[ErrorCatalogEntry] = []
        for code, parsed_entry in fragment_document.errors.items():
            if code in merged_errors:
                issues.append(
                    CatalogValidationIssue(
                        location=location(fragment_path, f"errors.{code}"),
                        message=(
                            "Duplicate symbolic error code; already defined in "
                            f"{display_path(merged_errors[code].source_path)}."
                        ),
                    )
                )
                continue

            derived_type_uri = (
                parsed_entry.type_uri_override
                if parsed_entry.type_uri_override is not None
                else f"{catalog_document.base_type_uri}{parsed_entry.type_slug}"
            )

            if parsed_entry.type_slug in seen_type_slugs:
                issues.append(
                    CatalogValidationIssue(
                        location=location(fragment_path, f"errors.{code}.type_slug"),
                        message=(
                            "Duplicate `type_slug`; already defined in "
                            f"{display_path(seen_type_slugs[parsed_entry.type_slug])}."
                        ),
                    )
                )
            else:
                seen_type_slugs[parsed_entry.type_slug] = fragment_path

            if derived_type_uri in seen_type_uris:
                duplicate_field = (
                    "type_uri_override"
                    if parsed_entry.type_uri_override is not None
                    else "type_slug"
                )
                issues.append(
                    CatalogValidationIssue(
                        location=location(
                            fragment_path,
                            f"errors.{code}.{duplicate_field}",
                        ),
                        message=(
                            "Duplicate derived problem type URI; already defined in "
                            f"{display_path(seen_type_uris[derived_type_uri])}."
                        ),
                    )
                )
            else:
                seen_type_uris[derived_type_uri] = fragment_path

            normalized_context_schema = normalize_context_schema(
                parsed_entry.context_schema
            )
            validate_context_references(
                normalized_context_schema,
                shared_context_schemas=shared_context_schemas,
                fragment_path=fragment_path,
                code=code,
                issues=issues,
            )
            validate_example_context(
                code=code,
                fragment_path=fragment_path,
                normalized_context_schema=normalized_context_schema,
                shared_context_schemas=shared_context_schemas,
                example=_model_dump(parsed_entry.example),
                issues=issues,
            )

            entry = ErrorCatalogEntry(
                code=code,
                module_name=module_name,
                source_path=fragment_path,
                type_slug=parsed_entry.type_slug,
                type_uri=derived_type_uri,
                recommended_http_status=parsed_entry.recommended_http_status,
                title=parsed_entry.title,
                description=parsed_entry.description,
                category=parsed_entry.category,
                retry_policy=parsed_entry.retry_policy,
                safe_to_expose=parsed_entry.safe_to_expose,
                translation_key=_derive_translation_key(
                    code,
                    parsed_entry.translation_key_override,
                ),
                raw_context_schema=parsed_entry.context_schema,
                normalized_context_schema=normalized_context_schema,
                type_uri_override=parsed_entry.type_uri_override,
                translation_key_override=parsed_entry.translation_key_override,
                log_level=parsed_entry.log_level,
                severity=parsed_entry.severity,
                example=_model_dump(parsed_entry.example),
                notes_for_operators=parsed_entry.notes_for_operators,
            )
            merged_errors[code] = entry
            entries.append(entry)

        fragments.append(
            ErrorCatalogFragment(
                module_name=module_name,
                source_path=fragment_path,
                errors=tuple(entries),
            )
        )

    if issues:
        raise CatalogValidationError(sort_issues(issues))

    return ErrorCatalog(
        catalog_path=catalog_path,
        schema_path=schema_path,
        namespace=catalog_document.namespace,
        base_type_uri=catalog_document.base_type_uri,
        schema_dialect=catalog_document.schema_dialect,
        default_media_type=catalog_document.default_media_type,
        shared_context_schemas=ErrorCatalog.freeze_mapping(shared_context_schemas),
        fragments=tuple(fragments),
        errors=ErrorCatalog.freeze_mapping(merged_errors),
    )


def _load_schema(schema_path: Path) -> dict[str, Any]:
    return json.loads(schema_path.read_text(encoding="utf-8"))


def _build_fragment_schema(schema: dict[str, Any]) -> dict[str, Any]:
    return {
        "$schema": schema.get(
            "$schema", "https://json-schema.org/draft/2020-12/schema"
        ),
        "$defs": schema.get("$defs", {}),
        "type": "object",
        "additionalProperties": False,
        "required": ["errors"],
        "properties": {"errors": {"$ref": "#/$defs/errorMap"}},
    }


def _build_validator(schema: dict[str, Any]) -> Draft202012Validator:
    return Draft202012Validator(
        schema,
        format_checker=Draft202012Validator.FORMAT_CHECKER,
    )


def _load_yaml_document(
    path: Path, issues: list[CatalogValidationIssue]
) -> dict[str, Any] | None:
    try:
        raw_document = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        issues.append(
            CatalogValidationIssue(
                location=display_path(path),
                message="Imported catalog file does not exist.",
            )
        )
        return None
    except yaml.YAMLError as error:
        issues.append(
            CatalogValidationIssue(
                location=display_path(path),
                message=f"Invalid YAML: {error}",
            )
        )
        return None

    if not isinstance(raw_document, dict):
        issues.append(
            CatalogValidationIssue(
                location=display_path(path),
                message="Catalog documents must deserialize to a mapping.",
            )
        )
        return None

    return raw_document


def _schema_errors(
    document: dict[str, Any],
    source_path: Path,
    validator: Draft202012Validator,
    issues: list[CatalogValidationIssue],
) -> None:
    for error in validator.iter_errors(document):
        path_suffix = ".".join(str(component) for component in error.absolute_path)
        issues.append(
            CatalogValidationIssue(
                location=location(source_path, path_suffix or "<root>"),
                message=error.message,
            )
        )


def _parse_document[DocumentT: BaseModel](
    model_type: type[DocumentT],
    raw_document: dict[str, Any],
    *,
    source_path: Path,
    issues: list[CatalogValidationIssue],
) -> DocumentT | None:
    try:
        return model_type.model_validate(raw_document)
    except PydanticValidationError as error:
        for parsed_issue in error.errors():
            path_suffix = ".".join(str(component) for component in parsed_issue["loc"])
            issues.append(
                CatalogValidationIssue(
                    location=location(source_path, path_suffix or "<root>"),
                    message=parsed_issue["msg"],
                )
            )
        return None


def _model_dump(model: BaseModel | None) -> dict[str, object] | None:
    if model is None:
        return None
    return model.model_dump(mode="python")


def _derive_translation_key(code: str, override: str | None) -> str:
    if override is not None:
        return override

    parts = code.lower().split("_")
    camel_case = parts[0] + "".join(part.title() for part in parts[1:])
    return f"errors.{camel_case}"
