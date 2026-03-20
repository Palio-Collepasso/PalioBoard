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

### `GAME_NOT_IN_PROGRESS`
- Domain error class: `GameNotInProgressError`
- API problem spec: `GAME_NOT_IN_PROGRESS_API_PROBLEM`
- Type URI: `https://api.palioboard.local/problems/game-not-in-progress`
- HTTP status: `409`
- Translation key: `errors.gameNotInProgress`

| Context field | Type | Required |
|---|---|---|
| `game_id` | `string (uuid)` | yes |
| `current_state` | `string` | yes |


# Notes

This section is preserved for human edits outside `# Error Catalog`.
