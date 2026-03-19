# API Error Contract

This document combines handwritten guidance with a generated `# Error Catalog`
section derived from `docs/api/errors/index.yaml` and imported catalog files.

## Contract summary

The API returns errors as `application/problem+json`.

Clients must treat these fields as stable:

- `type`: stable problem type URI
- `code`: stable symbolic application error code
- `status`: HTTP status
- `title`: short human-readable summary
- `context`: structured machine-readable error context

Clients must **not** branch on `title` or any free-text detail.

## Frontend rendering

Frontend templates are owned by the frontend.

Frontend code should:

- match on stable `code`
- read structured values from `context`
- render localized copy in the frontend/i18n layer

The backend catalog provides transport metadata and the shape of exposed context.
It does not own final user-facing message text.

## Source of truth

- Error definitions: `docs/api/errors/*.yaml`
- Endpoint-to-error mapping: `docs/api/openapi.yaml`
- This document: handwritten guidance plus generated catalog section

## Common wire shape

```json
{
  "type": "https://api.palioboard.local/problems/jolly-already-used",
  "code": "JOLLY_ALREADY_USED",
  "title": "Jolly already used",
  "status": 409,
  "context": {
    "team_id": "01956c9f-6f7e-7b42-a4b0-2d21d920c001",
    "game_id": "01956ca0-0c77-7b98-a328-39c9f8a31002",
    "previous_game_id": "01956ca0-53dd-7162-b78a-4bdb9368b003"
  }
}
```

# Error Catalog

This placeholder section should be replaced by the generator.

# Stability rules

## Stable

These are part of the client contract:

* symbolic `code`
* problem `type`
* `http_status` as transport metadata
* `context` field names and types

## Not stable

These may evolve without changing the error identity:

* wording of `title`
* explanatory prose in this document
* ordering of fields in examples

# For implementers
When adding a new error:

1. Add it to the correct catalog file in `docs/api/errors/`
2. Validate the catalog
3. Regenerate Python, TypeScript, and docs artifacts
4. Keep handwritten module-owned exception classes in `apps/api/src/palio/modules/<module>/errors.py`
5. Add or update frontend templates that consume `code + context`
6. Add or update tests for emitted error code and context
