# ADR-0010 — Error Catalog and Problem Details Contract

- Status: Accepted
- Date: 2026-03-18

## Context

The API needs stable machine-readable error semantics that can be shared across backend code, frontend code, OpenAPI, and human documentation.

A prose-only error contract creates duplication and drift:
- backend code can emit an error not described in docs
- TypeScript constants can diverge from backend identifiers
- endpoint docs can duplicate routing knowledge and error definitions
- frontend message rendering can drift from backend-emitted identifiers and context shape

## Decision

Adopt an endpoint-independent YAML error catalog under `docs/api/errors/` and use it as the source of truth for problem types.

Contract rules:
- client-facing API errors use `application/problem+json`
- the catalog defines what an error is
- `docs/api/openapi.yaml` defines which endpoints can return which errors
- the catalog key is the stable symbolic `code`
- `type` is derived from `base_type_uri + type_slug` unless explicitly overridden
- `context` shape is defined by a JSON Schema stored in the catalog
- the toolchain generates:
  - module-owned backend domain errors
  - API problem specs and domain-error-to-problem mappings
  - frontend TypeScript bindings
  - the generated `# Error Catalog` section in `docs/api/error-contract.md`
- handwritten backend code is limited to:
  - shared base exception types
  - FastAPI problem-response helpers and handlers
  - module-owned handwritten wrappers or overrides when a generated mapping is not enough
- frontend templates remain frontend-owned and render from stable `code + context`

## Consequences

### Positive

- One source of truth for error semantics.
- Lower drift across backend, frontend, OpenAPI, and docs.
- Clear split between error identity and endpoint routing.
- Machine-readable context contracts for clients and tests.
- Clear split between backend transport metadata and frontend-presented copy.
- Clear split between generated contract artifacts and handwritten runtime/boundary code.

### Negative

- Requires generator and validation tooling.
- Adds a small metadata-maintenance burden when introducing new errors.
- Requires discipline to keep endpoint mapping out of the catalog.
- Requires discipline to keep HTTP/runtime tests separate from catalog/generation tests.

## Follow-ups

- Validate the catalog in CI.
- Generate backend domain errors, API problem specs, frontend bindings, and docs from the catalog.
- Generate human-readable error docs from the catalog.
