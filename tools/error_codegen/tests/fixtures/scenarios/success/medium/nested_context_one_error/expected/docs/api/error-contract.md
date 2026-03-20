# API Error Contract

This document is partially generated from `contracts/errors/*.yaml`.

# Error Catalog

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


# Notes

This section is preserved for human edits outside `# Error Catalog`.
