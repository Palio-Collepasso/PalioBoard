"""Shared models for the error-code generation toolchain."""

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class CatalogValidationIssue:
    """One validation failure from the committed catalog."""

    location: str
    message: str


@dataclass(frozen=True, slots=True)
class ErrorCatalogEntry:
    """One validated error entry from the catalog."""

    code: str
    module_name: str
    source_path: Path
    type_slug: str
    type_uri: str
    recommended_http_status: int
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
    recommended_http_status: int
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
