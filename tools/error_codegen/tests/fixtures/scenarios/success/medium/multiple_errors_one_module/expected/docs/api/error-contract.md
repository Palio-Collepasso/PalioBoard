# API Error Contract

This document is partially generated from `contracts/errors/*.yaml`.

# Error Catalog

## `event_operations`

### `JOLLY_ALREADY_USED`
- Domain error class: `JollyAlreadyUsedError`
- API problem spec: `JOLLY_ALREADY_USED_API_PROBLEM`
- Type URI: `https://api.palioboard.local/problems/jolly-already-used`
- HTTP status: `409`
- Translation key: `errors.jollyAlreadyUsed`

| Context field | Type | Required |
|---|---|---|
| `team_id` | `string (uuid)` | yes |
| `game_id` | `string (uuid)` | yes |
| `previous_game_id` | `string (uuid)` | yes |

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

### `INVALID_PLACEMENT`
- Domain error class: `InvalidPlacementError`
- API problem spec: `INVALID_PLACEMENT_API_PROBLEM`
- Type URI: `https://api.palioboard.local/problems/invalid-placement`
- HTTP status: `400`
- Translation key: `errors.invalidPlacement`

| Context field | Type | Required |
|---|---|---|
| `game_id` | `string (uuid)` | yes |
| `team_id` | `string (uuid)` | yes |
| `placement` | `integer` | yes |


# Notes

This section is preserved for human edits outside `# Error Catalog`.
