# ADR-0008 — Deployment and Operational Model

- Status: Accepted
- Date: 2026-03-11

## Context

The app is used during a short annual event window. Operational simplicity matters more than always-on scale.

## Decision

Adopt a simple v1 deployment model:

- one VPS
- Docker Compose
- one FastAPI api instance
- Angular SPA
- Nginx reverse proxy
- same-origin routing
- direct Postgres connection
- explicit migration step before app start
- manual production deploy
- planned downtime is acceptable
- no Redis, broker, worker, or separate realtime service in v1

Observability:

- structured JSON logs
- request/correlation ids
- liveness, readiness, and build/version endpoints
- no external monitoring service in v1

Config:

- env-based configuration
- `.env` only for local development

## Consequences

### Positive

- Low operational complexity.
- Easy to understand and deploy.
- Good fit for the actual event usage pattern.

### Negative

- No horizontal scale path without some future refactoring.
- Operational debugging relies on logs rather than richer monitoring.

## Follow-ups

- Keep non-business technical concerns behind adapters so infra can evolve later.
- Revisit Redis or extra services only if justified by real operational pain.
