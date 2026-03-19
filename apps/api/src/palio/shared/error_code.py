"""Shared runtime types for catalog-defined API error codes."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ErrorDefinition:
    """Generated transport metadata for one catalog-defined error."""

    code: str
    module_name: str
    type_slug: str
    type_uri: str
    http_status: int
    title: str
    description: str | None
    category: str
    retry_policy: str
    safe_to_expose: bool
    translation_key: str
    log_level: str | None
    severity: str | None
    context_schema: object
    notes_for_operators: str | None
