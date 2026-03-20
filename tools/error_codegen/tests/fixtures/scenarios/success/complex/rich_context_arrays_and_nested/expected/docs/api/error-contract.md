# API Error Contract

This document is partially generated from `contracts/errors/*.yaml`.

# Error Catalog

## `authorization`

### `MISSING_ANY_CAPABILITY`
- Domain error class: `MissingAnyCapabilityError`
- API problem spec: `MISSING_ANY_CAPABILITY_API_PROBLEM`
- Type URI: `https://api.palioboard.local/problems/missing-any-capability`
- HTTP status: `403`
- Translation key: `errors.missingAnyCapability`

| Context field | Type | Required |
|---|---|---|
| `required_any` | `array<string>` | yes |
| `granted` | `array<string>` | yes |


## `event_operations`

### `LIVE_CYCLE_MISMATCH`
- Domain error class: `LiveCycleMismatchError`
- API problem spec: `LIVE_CYCLE_MISMATCH_API_PROBLEM`
- Type URI: `https://api.palioboard.local/problems/live-cycle-mismatch`
- HTTP status: `409`
- Translation key: `errors.liveCycleMismatch`

| Context field | Type | Required |
|---|---|---|
| `game_id` | `string (uuid)` | yes |
| `expected` | `object{state, live_cycle}` | yes |
| `actual` | `object{state, live_cycle}` | yes |


# Notes

This section is preserved for human edits outside `# Error Catalog`.
