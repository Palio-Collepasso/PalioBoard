from pathlib import Path
from typing import Any

from error_codegen.models import ErrorCatalog, ErrorCatalogEntry, ErrorCatalogFragment

MODULE_NAMES = (
    "audit",
    "authorization",
    "event_operations",
    "identity",
    "leaderboard_projection",
    "live_games",
    "public_read",
    "results",
    "season_setup",
    "tournaments",
    "users",
)


def sample_entry_kwargs(**overrides: object) -> dict[str, Any]:
    values: dict[str, Any] = {
        "code": "JOLLY_ALREADY_USED",
        "module_name": "event_operations",
        "source_path": Path("docs/api/errors/event_operations.yaml"),
        "type_slug": "jolly-already-used",
        "type_uri": "https://api.palioboard.local/problems/jolly-already-used",
        "http_status": 409,
        "title": "Jolly already used",
        "description": (
            "The selected team has already consumed its Jolly in a previous game, "
            "so the current result cannot be accepted as submitted."
        ),
        "category": "business_rule",
        "retry_policy": "never",
        "safe_to_expose": True,
        "translation_key": "errors.jollyAlreadyUsed",
        "raw_context_schema": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "team_id": {
                    "$ref": "#/shared_context_schemas/UuidRef",
                    "description": "Team using the Jolly",
                },
                "game_id": {
                    "$ref": "#/shared_context_schemas/UuidRef",
                    "description": "Current game being saved",
                },
                "previous_game_id": {
                    "$ref": "#/shared_context_schemas/UuidRef",
                    "description": "Earlier game where the Jolly was already used",
                },
            },
            "required": ["team_id", "game_id"],
        },
        "normalized_context_schema": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "team_id": {
                    "$ref": "#/shared_context_schemas/UuidRef",
                    "description": "Team using the Jolly",
                },
                "game_id": {
                    "$ref": "#/shared_context_schemas/UuidRef",
                    "description": "Current game being saved",
                },
                "previous_game_id": {
                    "$ref": "#/shared_context_schemas/UuidRef",
                    "description": "Earlier game where the Jolly was already used",
                },
            },
            "required": ["team_id", "game_id"],
        },
        "resolved_context_schema": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "team_id": {
                    "type": "string",
                    "format": "uuid",
                    "description": "Team using the Jolly",
                },
                "game_id": {
                    "type": "string",
                    "format": "uuid",
                    "description": "Current game being saved",
                },
                "previous_game_id": {
                    "type": "string",
                    "format": "uuid",
                    "description": "Earlier game where the Jolly was already used",
                },
            },
            "required": ["team_id", "game_id"],
        },
        "type_uri_override": None,
        "translation_key_override": None,
        "log_level": None,
        "severity": None,
        "example": {
            "context": {
                "team_id": "01956c9f-6f7e-7b42-a4b0-2d21d920c001",
                "game_id": "01956ca0-0c77-7b98-a328-39c9f8a31002",
                "previous_game_id": "01956ca0-53dd-7162-b78a-4bdb9368b003",
            }
        },
        "notes_for_operators": None,
    }
    values.update(overrides)
    return values


def build_sample_catalog() -> ErrorCatalog:
    entry = ErrorCatalogEntry(**sample_entry_kwargs())
    fragments = tuple(
        ErrorCatalogFragment(
            module_name=module_name,
            source_path=Path("docs/api/errors") / f"{module_name}.yaml",
            errors=(entry,) if module_name == "event_operations" else (),
        )
        for module_name in MODULE_NAMES
    )
    return ErrorCatalog(
        catalog_path=Path("docs/api/errors/index.yaml"),
        schema_path=Path("docs/api/errors/schema.json"),
        namespace="palioboard",
        base_type_uri="https://api.palioboard.local/problems/",
        schema_dialect="https://json-schema.org/draft/2020-12/schema",
        default_media_type="application/problem+json",
        shared_context_schemas=ErrorCatalog.freeze_mapping(
            {
                "UuidRef": {
                    "type": "string",
                    "format": "uuid",
                }
            }
        ),
        fragments=fragments,
        errors=ErrorCatalog.freeze_mapping({entry.code: entry}),
    )
