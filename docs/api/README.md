# API Guide

## Purpose
Use this directory for the committed HTTP contract, the error catalog source of truth, and the small amount of human guidance needed to work on them safely.

## Source of truth split
Use these files for different concerns:

- `docs/architecture/adr/ADR-0007-api-and-contract-strategy.md` for the API surface
- `docs/api/openapi.yaml` — generated request, response, and status surface for each endpoint
- `docs/architecture/adr/ADR-0010-error-catalog-and-problem-details.md` for the error-catalog strategy
- `docs/api/errors/*.yaml` — authoritative catalog of problem types and their metadata
- `docs/api/error-contract.md` — handwritten guidance plus a generated `# Error Catalog` section
- backend code — current behavior if docs drift

The error catalog is endpoint-independent. It defines what an error is. OpenAPI defines which endpoints can return which errors.

## Current stable surfaces
The currently committed API surface is intentionally small:
- meta endpoints: `/healthz`, `/readyz`, `/version`
- protected admin endpoints: `/api/admin/session`, `/api/admin/health`
- public health endpoint: `/api/public/health`
- realtime health endpoint: `/realtime/health`

## API and Error workflow
When an API is added or changes:
1. Update the relevant `docs/api/errors/*.yaml` catalog fragment.
2. Run `make errors` to validate the catalog, regenerate local Python and TypeScript artifacts, and refresh the generated docs output.
3. Keep handwritten module exceptions aligned with the generated backend definitions when runtime behavior changed.
4. Update endpoint-level OpenAPI responses if the set of possible endpoint errors changed.
5. Run `make api-contract` to export the composed OpenAPI spec and regenerate committed consumer declarations.
6. Run `make contracts` when both the catalog and endpoint-level API mapping changed.

The top-level grouped workflow surface is:
- `make errors` — validate the catalog and regenerate local error artifacts
- `make api-contract` — export the composed OpenAPI contract and regenerate committed consumer declarations
- `make contracts` — both grouped flows together

## What does not belong here
- endpoint-specific error routing duplicated from OpenAPI
- speculative future error codes
- manually maintained per-error prose that duplicates the catalog
- transport-agnostic business rules that already live in domain docs
