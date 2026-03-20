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


# Notes

This section is preserved for human edits outside `# Error Catalog`.
