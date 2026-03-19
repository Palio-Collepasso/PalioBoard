"""Generated Python error definitions for the `event_operations` module."""

from palio.shared.errors.base import ErrorDefinition

MODULE_NAME = "event_operations"

JOLLY_ALREADY_USED = ErrorDefinition(
    code="JOLLY_ALREADY_USED",
    module_name=MODULE_NAME,
    type_slug="jolly-already-used",
    type_uri="https://api.palioboard.local/problems/jolly-already-used",
    http_status=409,
    title="Jolly already used",
    description=(
        "The selected team has already consumed its Jolly in a previous game, so the current "
        "result cannot be accepted as submitted.\n"
    ),
    category="business_rule",
    retry_policy="never",
    safe_to_expose=True,
    translation_key="errors.jollyAlreadyUsed",
    log_level=None,
    severity=None,
    context_schema={
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "team_id": {"type": "string", "format": "uuid"},
            "game_id": {"type": "string", "format": "uuid"},
            "previous_game_id": {"type": "string", "format": "uuid"},
        },
        "required": ["team_id", "game_id"],
    },
    notes_for_operators=None,
)

ERROR_DEFINITIONS: tuple[ErrorDefinition, ...] = (JOLLY_ALREADY_USED,)
ERROR_DEFINITIONS_BY_CODE: dict[str, ErrorDefinition] = {
    JOLLY_ALREADY_USED.code: JOLLY_ALREADY_USED,
}
ERROR_CODES: tuple[str, ...] = tuple(
    error_definition.code for error_definition in ERROR_DEFINITIONS
)

__all__ = [
    "ERROR_CODES",
    "ERROR_DEFINITIONS",
    "ERROR_DEFINITIONS_BY_CODE",
    "JOLLY_ALREADY_USED",
    "MODULE_NAME",
    "ErrorDefinition",
]
