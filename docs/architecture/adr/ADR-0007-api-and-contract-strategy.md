# ADR-0007 — API Surfaces and OpenAPI Contract Strategy

- Status: Accepted
- Date: 2026-03-11

## Context

The system serves three interaction modes:

- authenticated admin/judge operations
- anonymous public reads
- realtime delivery and collaboration

Frontend and backend live in one monorepo and evolve together.

## Decision

Use a REST API with explicit command/query endpoints and three backend surfaces:

- `/api/admin/...`
- `/api/public/...`
- `/realtime/...`

Contract rules:

- FastAPI owns the OpenAPI contract
- the OpenAPI spec is committed as a versioned artifact
- TypeScript types are generated from that committed spec
- generated TS types are not committed
- Angular data-access services remain hand-written
- errors use a standardized machine-readable envelope

Public read rule:

- public/maxi endpoints read only from projection/read models

## Consequences

### Positive

- Clear separation of authenticated commands, anonymous reads, and realtime transport.
- Low frontend/backend contract drift.
- No need for generated runtime clients.

### Negative

- Requires discipline to keep `/api/public` strictly projection-backed.
- Realtime contracts remain hand-managed unless later formalized further.

## Follow-ups

- Keep separate Angular API facades for admin, public, and realtime.
- Add CI checks around OpenAPI export and type generation.
