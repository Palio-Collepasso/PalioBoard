---
id: m-0
title: Delivery foundation and architecture skeleton
---
## Description

Milestone: Delivery foundation and architecture skeleton

Depends on: none.

Objective: establish the project skeleton, delivery rails, and architectural guardrails so every later slice is built on the approved baseline rather than on throwaway scaffolding.

Scope:
- Monorepo structure for `api/`, `web/`, `infra/`, `docs/`, and top-level tooling.
- FastAPI app skeleton with modular-monolith boundaries and per-module facades.
- Angular SPA skeleton with three shells: admin, public, maxi-screen.
- PostgreSQL, Alembic, and baseline migrations.
- Docker Compose, Nginx, health/version endpoints, env-based config.
- CI, pre-commit, lint/format/typecheck/test commands, OpenAPI export/generation workflow.
- Test harnesses for api unit/integration tests, frontend tests, and Playwright smoke setup.

Exit criteria:
- The whole stack boots locally from documented commands.
- CI runs and enforces the agreed baseline checks.
- A baseline migration creates the empty schema successfully.
- Api/frontend shells are reachable and wired through the same-origin proxy.
- Architectural guardrails are in place enough to prevent obvious boundary violations.
