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


## `results`

### `PLACEMENT_CONFLICT`
- Domain error class: `PlacementConflictError`
- API problem spec: `PLACEMENT_CONFLICT_API_PROBLEM`
- Type URI: `https://api.palioboard.local/problems/placement-conflict`
- HTTP status: `409`
- Translation key: `errors.placementConflict`

| Context field | Type | Required |
|---|---|---|
| `game_id` | `string (uuid)` | yes |
| `existing_result` | `object{team_id, placement}` | yes |
| `incoming_result` | `object{team_id, placement}` | yes |


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
| `source` | `enum[route, body, query]` | no |


# Notes

This section is preserved for human edits outside `# Error Catalog`.
