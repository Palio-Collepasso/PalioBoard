# Error Catalog Guide

## Purpose
This directory is the authoritative source of truth for endpoint-independent API problem types.

The catalog is endpoint-independent:
- it defines what an error is
- it does not define which endpoint returns it

Endpoint-level mapping stays in `docs/api/openapi.yaml`.

## Directory structure
- `schema.json` — JSON Schema for the root catalog format
- `index.yaml` — root metadata, imports, and shared context schemas
- `audit.yaml` — audit module errors
- `authorization.yaml` — authorization module errors
- `event_operations.yaml` — event-operations module errors
- `identity.yaml` — identity module errors
- `leaderboard_projection.yaml` — leaderboard-projection module errors
- `live_games.yaml` — live-games module errors
- `public_read.yaml` — public-read module errors
- `results.yaml` — results module errors
- `season_setup.yaml` — season-setup module errors
- `tournaments.yaml` — tournaments module errors
- `users.yaml` — users module errors

## Authored vs derived data
### Authored in YAML
Each error entry authors:
- the stable symbolic key under `errors:`
- `type_slug`
- `http_status`
- `title`
- `category`
- `retry_policy`
- `safe_to_expose`
- `context_schema`
- optional metadata

All fields are documented in `docs/templates/api/errors-area.yaml`.

### Derived by tools
The toolchain derives:
- `code` from the `errors` map key
- `type` from `base_type_uri + type_slug`, unless overridden
- the default `translation_key`, unless overridden
- generated backend domain errors and API transport artifacts from the catalog
- local merged frontend artifacts under `apps/web/src/app/shared/api/generated/`
- generated human-readable docs such as `docs/api/error-contract.md`

Frontend message templates remain handwritten and frontend-owned.
They consume stable `code + context` from API problem responses.

## Target generated and handwritten split
The intended architecture is:

- generated domain errors under `apps/api/src/palio/modules/<module>/errors_gen.py`
- handwritten module-owned error wrappers or overrides under `apps/api/src/palio/modules/<module>/errors.py`
- generated API problem specs under `apps/api/src/palio/api/modules/<module>/errors/specs_gen.py`
- generated domain-error-to-problem mappings under `apps/api/src/palio/api/modules/<module>/errors/mapping_gen.py`
- handwritten shared API helpers under `apps/api/src/palio/api/errors/`
- generated `# Error Catalog` section content injected into `docs/api/error-contract.md`
- frontend-owned templates rendering user-facing copy from stable `code + context`

Generated domain errors must not know:
- HTTP status
- problem type URIs
- FastAPI
- response envelope structure

Generated API problem specs and mappings must not own domain behavior.

The docs generator must replace only the `# Error Catalog` section body and preserve the rest of `docs/api/error-contract.md`.

## Working rules
- Keep the catalog endpoint-independent.
- Do not duplicate endpoint ownership or routing here.
- Do not add speculative future errors.
- Keep one top-level fragment file per backend module under `apps/api/src/palio/modules/`.
- Keep context schemas minimal and stable.
- Keep handwritten runtime exception classes in the owning backend module.
- Keep generated backend and API artifacts module-owned; do not centralize them in one registry file.
- Keep frontend copy out of the catalog; frontend templates render from `code + context`.
- Prefer shared context schemas in `index.yaml` when the same shape recurs.

## Testing
Test the catalog tool primarily under `tools/error_codegen/tests/`. Use broad scenario coverage there for validation, generation, docs injection, deterministic output, and CLI behavior. Keep API tests focused on runtime behavior under `apps/api/tests/`: handler behavior, real endpoint flows, and serialized `application/problem+json` responses. API tests may reuse a small curated subset of catalog-derived examples for consistency checks, but they should not iterate the full tool scenario tree by default.

## Adding or changing an error
1. Pick the fragment file that matches the owning backend module.
2. Add or update the error entry under `errors:` using the symbolic code as the key.
3. Reuse shared context schemas where possible.
4. Add an example when the context shape is non-trivial.
5. Run `make errors`.
6. Update handwritten module exceptions if backend runtime behavior changed.
7. Update frontend templates that render the affected `code`.
8. Update endpoint-level OpenAPI documentation separately when endpoint-to-error mapping changed.

## Example entry
```yaml
errors:
  JOLLY_ALREADY_USED:
    type_slug: jolly-already-used
    http_status: 409
    title: Jolly already used
    category: business_rule
    retry_policy: never
    safe_to_expose: true
    context_schema:
      type: object
      additionalProperties: false
      properties:
        team_id:
          $ref: "#/shared_context_schemas/UuidRef"
        game_id:
          $ref: "#/shared_context_schemas/UuidRef"
      required: [team_id, game_id]
```

## Checks handled outside JSON Schema
The catalog validator must also enforce rules that JSON Schema alone does not express well:
- uniqueness of derived `type` URIs across imported files
- uniqueness of `type_slug` across imported files
- alignment between imported fragment files and backend module ownership
- ownership coherence between fragment files and their module-scoped error entries
- `example.context` conforms to `context_schema`
- shared-context references resolve without leaving the catalog
- public/exposure metadata stays coherent with frontend/runtime expectations

## Current status
The catalog structure is committed here even if some fragment files are still intentionally small.
Add real error definitions only when the backend commits those semantics.
