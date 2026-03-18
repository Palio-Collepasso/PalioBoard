# ADR-0001 — System Boundary and Core Stack

- Status: Accepted
- Date: 2026-03-11

## Context

The product requires immediate public visibility, auditable official changes, live result entry, automatic scoring, and portability to plain PostgreSQL later.

The team stack preference is Python, Angular, and Supabase.

## Decision

Adopt the following system boundary:

- Angular is the only frontend.
- FastAPI is the only business/data API.
- PostgreSQL is the application database.
- Supabase is used in v1 as:
  - hosted PostgreSQL
  - identity provider
- Nginx is the reverse proxy.
- Python connects directly to PostgreSQL.
- Angular never talks directly to application data storage.

Adopt the following core stack:

- Angular SPA
- FastAPI
- Pydantic
- SQLAlchemy 2.x
- Alembic
- PostgreSQL
- Supabase Auth
- Nginx
- Docker + Docker Compose

## Consequences

### Positive

- One clear backend ownership boundary.
- Simpler authorization model.
- Better portability to self-hosted PostgreSQL later.
- No duplicated logic between frontend, Supabase data APIs, and Python.

### Negative

- Python becomes the single application bottleneck and integration point.
- Realtime and public reads must be intentionally designed, not delegated to Supabase clients.

## Follow-ups

- Keep Supabase-specific code behind explicit adapters.
- Avoid application dependence on Supabase RLS or data APIs.
