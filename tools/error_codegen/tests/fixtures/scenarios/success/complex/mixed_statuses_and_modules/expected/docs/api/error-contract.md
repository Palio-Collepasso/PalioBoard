# API Error Contract

This document is partially generated from `contracts/errors/*.yaml`.

# Error Catalog

## `authorization`

### `MISSING_CAPABILITY`
- Domain error class: `MissingCapabilityError`
- API problem spec: `MISSING_CAPABILITY_API_PROBLEM`
- Type URI: `https://api.palioboard.local/problems/missing-capability`
- HTTP status: `403`
- Translation key: `errors.missingCapability`

| Context field | Type | Required |
|---|---|---|
| `capability` | `string` | yes |


## `event_operations`

### `GAME_ALREADY_CLOSED`
- Domain error class: `GameAlreadyClosedError`
- API problem spec: `GAME_ALREADY_CLOSED_API_PROBLEM`
- Type URI: `https://api.palioboard.local/problems/game-already-closed`
- HTTP status: `409`
- Translation key: `errors.gameAlreadyClosed`

No exposed context fields.


## `teams`

### `TEAM_NOT_FOUND`
- Domain error class: `TeamNotFoundError`
- API problem spec: `TEAM_NOT_FOUND_API_PROBLEM`
- Type URI: `https://api.palioboard.local/problems/team-not-found`
- HTTP status: `404`
- Translation key: `errors.teamNotFound`

| Context field | Type | Required |
|---|---|---|
| `team_id` | `string (uuid)` | yes |


## `validation`

### `INVALID_ENTRY_PAYLOAD`
- Domain error class: `InvalidEntryPayloadError`
- API problem spec: `INVALID_ENTRY_PAYLOAD_API_PROBLEM`
- Type URI: `https://api.palioboard.local/problems/invalid-entry-payload`
- HTTP status: `400`
- Translation key: `errors.invalidEntryPayload`

| Context field | Type | Required |
|---|---|---|
| `field` | `string` | yes |
| `reason` | `string` | yes |


# Notes

This section is preserved for human edits outside `# Error Catalog`.
