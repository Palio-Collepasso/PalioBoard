"""Framework-agnostic runtime primitives for catalog-backed errors."""

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, ClassVar, cast

from jsonschema import Draft202012Validator
from pydantic import TypeAdapter

_JSON_ENCODER = TypeAdapter(object)

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)


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


class InvalidErrorContextError(ValueError):
    """Raised when runtime context does not match the catalog definition."""


class ApplicationError(Exception):
    """Base runtime error carrying one catalog definition plus context values."""

    error_definition: ClassVar[ErrorDefinition]

    def __init__(
        self,
        *,
        context: Mapping[str, object],
        detail: str | None = None,
    ) -> None:
        """Create one runtime error instance with validated transport context."""
        definition = self._resolve_error_definition()
        encoded_context = _encode_context(context)
        _validate_context(definition, encoded_context)
        self.context = MappingProxyType(encoded_context)
        self.detail = detail
        super().__init__(detail or definition.title)

    def _resolve_error_definition(self) -> ErrorDefinition:
        """Return the subclass-owned generated error definition."""
        definition = getattr(type(self), "error_definition", None)
        if not isinstance(definition, ErrorDefinition):
            raise TypeError(
                f"{type(self).__name__} must define "
                "an `error_definition` class attribute."
            )
        return definition


def _encode_context(context: Mapping[str, object]) -> dict[str, JsonValue]:
    """Convert runtime values into a JSON-compatible mapping before validation."""
    encoded_context = _JSON_ENCODER.dump_python(dict(context), mode="json")
    if not isinstance(encoded_context, dict):
        raise InvalidErrorContextError(
            "Application error context must encode to an object."
        )
    return cast(dict[str, JsonValue], encoded_context)


def _as_json_schema(schema: object) -> Mapping[str, object] | bool:
    """Return one runtime context schema in the shape expected by `jsonschema`."""
    if isinstance(schema, bool):
        return schema
    if isinstance(schema, Mapping):
        return cast(Mapping[str, object], schema)
    raise InvalidErrorContextError(
        "Application error context schema must be a JSON Schema object."
    )


def _validate_context(
    definition: ErrorDefinition,
    context: dict[str, JsonValue],
) -> None:
    """Validate runtime context against the generated JSON Schema."""
    validator = Draft202012Validator(
        _as_json_schema(definition.context_schema),
        format_checker=Draft202012Validator.FORMAT_CHECKER,
    )
    validation_errors = list(cast(Any, validator).iter_errors(context))
    if not validation_errors:
        return

    first_error = validation_errors[0]
    path_suffix = ".".join(str(component) for component in first_error.absolute_path)
    if path_suffix:
        raise InvalidErrorContextError(
            f"Invalid context for `{definition.code}` "
            f"at `{path_suffix}`: {first_error.message}"
        )
    raise InvalidErrorContextError(
        f"Invalid context for `{definition.code}`: {first_error.message}"
    )
