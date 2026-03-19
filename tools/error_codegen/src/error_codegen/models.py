"""Shared models for the error-code generation toolchain."""

import re
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any, TypeVar

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

T = TypeVar("T")

CODE_PATTERN = re.compile(r"^[A-Z][A-Z0-9_]*$")
TYPE_SLUG_PATTERN = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")
TRANSLATION_KEY_PATTERN = re.compile(r"^[a-z][A-Za-z0-9]*(?:\.[A-Za-z0-9]+)*$")


@dataclass(frozen=True, slots=True)
class CatalogValidationIssue:
    """One validation failure from the committed catalog."""

    location: str
    message: str


class ErrorCatalogEntry(BaseModel):
    """One validated error entry from the catalog."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    code: str
    module_name: str
    source_path: Path
    type_slug: str
    type_uri: str
    http_status: int
    title: str
    description: str | None
    category: str
    retry_policy: str
    safe_to_expose: bool
    translation_key: str
    raw_context_schema: object
    normalized_context_schema: object
    type_uri_override: str | None
    translation_key_override: str | None
    log_level: str | None
    severity: str | None
    example: Mapping[str, object] | None
    notes_for_operators: str | None

    @field_validator("code")
    @classmethod
    def validate_code(cls, value: str) -> str:
        """Ensure generated symbolic codes stay stable and machine-friendly."""
        if not CODE_PATTERN.fullmatch(value):
            raise ValueError(
                "String should match the symbolic UPPER_SNAKE_CASE format."
            )
        return value

    @field_validator("type_slug")
    @classmethod
    def validate_type_slug(cls, value: str) -> str:
        """Ensure problem-type slugs remain kebab-case."""
        if not TYPE_SLUG_PATTERN.fullmatch(value):
            raise ValueError("String should match the kebab-case `type_slug` format.")
        return value

    @field_validator("http_status")
    @classmethod
    def validate_http_status(cls, value: int) -> int:
        """Ensure catalog transport metadata represents a real HTTP error."""
        if not 400 <= value <= 599:
            raise ValueError("HTTP status must be between 400 and 599.")
        return value

    @field_validator("translation_key")
    @classmethod
    def validate_translation_key(cls, value: str) -> str:
        """Ensure translation keys stay compatible with frontend template lookup."""
        if not TRANSLATION_KEY_PATTERN.fullmatch(value):
            raise ValueError("String should match the dotted translation-key format.")
        return value

    @field_validator("normalized_context_schema")
    @classmethod
    def validate_normalized_context_schema(cls, value: object) -> object:
        """Ensure exposed runtime context is always described as a closed object."""
        _validate_runtime_context_schema(value)
        return value


@dataclass(frozen=True, slots=True)
class ErrorCatalogFragment:
    """One module-owned fragment imported by the root catalog."""

    module_name: str
    source_path: Path
    errors: tuple[ErrorCatalogEntry, ...]


@dataclass(frozen=True, slots=True)
class ErrorCatalog:
    """Validated root catalog plus imported fragments."""

    catalog_path: Path
    schema_path: Path
    namespace: str
    base_type_uri: str
    schema_dialect: str
    default_media_type: str
    shared_context_schemas: Mapping[str, object]
    fragments: tuple[ErrorCatalogFragment, ...]
    errors: Mapping[str, ErrorCatalogEntry]

    def errors_for_module(self, module_name: str) -> tuple[ErrorCatalogEntry, ...]:
        """Return the validated errors owned by one backend module."""
        for fragment in self.fragments:
            if fragment.module_name == module_name:
                return fragment.errors
        return ()

    @property
    def module_names(self) -> tuple[str, ...]:
        """Return imported backend module names in catalog order."""
        return tuple(fragment.module_name for fragment in self.fragments)

    @staticmethod
    def freeze_mapping(values: Mapping[str, T]) -> Mapping[str, T]:
        """Return a read-only mapping for catalog metadata."""
        return MappingProxyType(dict(values))


class ErrorExampleDocument(BaseModel):
    """Typed parsed view of an authored catalog example."""

    model_config = ConfigDict(extra="forbid")

    detail: str | None = None
    context: dict[str, Any]


class ErrorEntryDocument(BaseModel):
    """Typed parsed view of one authored error entry."""

    model_config = ConfigDict(extra="forbid")

    type_slug: str
    type_uri_override: str | None = None
    http_status: int
    title: str
    description: str | None = None
    category: str
    retry_policy: str
    safe_to_expose: bool
    translation_key_override: str | None = None
    context_schema: object
    log_level: str | None = None
    severity: str | None = None
    example: ErrorExampleDocument | None = None
    notes_for_operators: str | None = None

    @field_validator("type_slug")
    @classmethod
    def validate_authored_type_slug(cls, value: str) -> str:
        """Validate the authored problem-type slug before generation."""
        if not TYPE_SLUG_PATTERN.fullmatch(value):
            raise ValueError("String should match the kebab-case `type_slug` format.")
        return value

    @field_validator("http_status")
    @classmethod
    def validate_authored_http_status(cls, value: int) -> int:
        """Validate authored transport metadata before code generation."""
        if not 400 <= value <= 599:
            raise ValueError("HTTP status must be between 400 and 599.")
        return value

    @field_validator("translation_key_override")
    @classmethod
    def validate_translation_key_override(cls, value: str | None) -> str | None:
        """Validate an explicit frontend translation lookup key when authored."""
        if value is None:
            return None
        if not TRANSLATION_KEY_PATTERN.fullmatch(value):
            raise ValueError("String should match the dotted translation-key format.")
        return value

    @field_validator("context_schema")
    @classmethod
    def validate_context_schema(cls, value: object) -> object:
        """Require client-facing `context` to be described by an object schema."""
        _validate_runtime_context_schema(value)
        return value

    @model_validator(mode="after")
    def validate_exposure_rules(self) -> "ErrorEntryDocument":
        """Keep translation metadata aligned with client exposure semantics."""
        if not self.safe_to_expose and self.translation_key_override is not None:
            raise ValueError(
                "Non-exposed errors must not declare `translation_key_override`."
            )
        return self


class FragmentCatalogDocument(BaseModel):
    """Typed parsed view of a module-owned catalog fragment."""

    model_config = ConfigDict(extra="forbid")

    errors: dict[str, ErrorEntryDocument] = Field(default_factory=dict)


class RootCatalogDocument(BaseModel):
    """Typed parsed view of the root catalog index."""

    model_config = ConfigDict(extra="forbid")

    catalog_version: int
    namespace: str
    base_type_uri: str
    schema_dialect: str
    default_media_type: str
    imports: list[str] = Field(default_factory=list)
    shared_context_schemas: dict[str, object] = Field(default_factory=dict)
    errors: dict[str, ErrorEntryDocument] = Field(default_factory=dict)


def _validate_runtime_context_schema(schema: object) -> None:
    """Validate that catalog `context` describes a structured client-safe object."""
    if not isinstance(schema, dict):
        raise ValueError("Context schema must be a JSON Schema object.")

    if not _is_object_like_schema(schema):
        raise ValueError(
            "Context schema must describe an object-shaped `context` payload."
        )

    additional_properties = schema.get("additionalProperties")
    if additional_properties is True:
        raise ValueError(
            "Context schema must not use `additionalProperties: true`; "
            "declare explicit fields or a nested schema instead."
        )


def _is_object_like_schema(schema: dict[str, object]) -> bool:
    """Return whether a JSON Schema object can describe a JSON object value."""
    if "$ref" in schema:
        return True
    if "properties" in schema:
        return True

    schema_type = schema.get("type")
    if schema_type == "object":
        return True
    if isinstance(schema_type, list) and "object" in schema_type:
        return True

    for keyword in ("allOf", "anyOf", "oneOf"):
        variants = schema.get(keyword)
        if isinstance(variants, list) and variants:
            return True

    return False
