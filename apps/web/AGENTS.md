# Web / frontend instructions

## Scope
This file applies to frontend work under `apps/web/`.

## Core rules
- Keep business rules and official truth in the api. The frontend should present and edit server-owned state, not redefine it.
- Preserve shell separation: admin, public, and maxi-screen concerns should stay explicit.
- Prefer feature-local state. Do not introduce a global store without a documented reason.
- Keep admin, public, and realtime API clients clearly separated.

## What to read first
Start from `docs/README.md`, then read the smallest relevant subset of:
- product and functional requirements
- architecture baseline and ADRs
- API contract docs
- testing docs, especially critical E2E flows

## Commands
Prefer repo `make` targets from the repository root when available.

## Required validation by change type
- Component or presentational logic: add/update local unit tests when valuable.
- Route, shell, or integration behavior: add/update integration tests.
- Critical user flow or realtime collaboration behavior: update the small E2E suite.
- API contract change consumed by the frontend: regenerate locally if required by the repo workflow, but do not commit generated TS clients if the repo policy says not to.

## Do NOT
- do NOT duplicate scoring, standings, or authorization truth in the client
- do NOT couple public/maxi-screen views to admin-only assumptions
- do NOT introduce cross-shell shortcuts when a shared API or UI abstraction is enough
