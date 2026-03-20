# API Error Contract

This document is partially generated from `contracts/errors/*.yaml`.

# Error Catalog

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
