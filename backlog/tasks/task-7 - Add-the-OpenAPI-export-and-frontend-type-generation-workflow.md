---
id: TASK-7
title: Add the OpenAPI export and frontend type-generation workflow
status: Done
assignee:
  - '@codex'
created_date: '2026-03-12 01:37'
updated_date: '2026-03-14 14:36'
labels: []
milestone: m-0
dependencies:
  - TASK-2
  - TASK-3
documentation:
  - docs/qna/architecture/api and contracts.md
  - docs/architecture/adr/ADR-0007-api-and-contract-strategy.md
parent_task_id: M-0
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Set up the contract workflow where FastAPI owns the OpenAPI artifact, the spec is committed in the repo, and frontend TypeScript types are generated from that committed file instead of from a running api.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 A repeatable command exports the api OpenAPI spec as a committed repo artifact.
- [x] #2 Frontend TypeScript types can be regenerated from the committed OpenAPI file without requiring a running api.
- [x] #3 The workflow makes it clear that the spec is committed while generated TS types are not.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Draft plan pending user approval before coding.

1. Api-owned OpenAPI export
- Add a small api-owned export module/script that imports `create_app()`, calls `app.openapi()`, and writes a deterministic `docs/api/openapi.yaml` artifact without starting a FastAPI server.
- Wire the export behind a stable repo command in `Makefile` and document the app-local equivalent under `apps/api/README.md`.
- Keep scope limited to the FastAPI-owned HTTP contract; realtime WebSocket details remain hand-managed per ADR-0007.

2. Frontend type-generation from the committed spec
- Add a frontend generator tool and `npm` script that reads the committed `docs/api/openapi.yaml` file and writes generated TypeScript definitions under `apps/web/src/app/shared/api/generated/`.
- Keep Angular API services hand-written; generate types only, not runtime clients.
- Expose a stable repo-level command that regenerates frontend types from the committed spec without requiring a running api.

3. Repo guardrails and documentation
- Add ignore rules so generated TypeScript output is not committed while the OpenAPI spec remains tracked.
- Update `README.md`, `apps/api/README.md`, `apps/web/README.md`, and `docs/ops/local-dev.md` so the workflow is explicit about what is committed versus regenerated.
- Create the missing `docs/api/` contract-artifact path already referenced by repo docs.

4. Verification
- Run the OpenAPI export command and confirm the committed spec captures the current placeholder REST routes.
- Run the frontend type-generation command against the committed spec and confirm output lands in the ignored generated-types path.
- Run the narrow affected checks (`cd apps/api && uv run pytest`, `cd apps/web && npm run typecheck`, plus the new generator commands) to confirm the workflow is repeatable.

Risks / implementation notes
- The repo docs currently point to `docs/api/openapi.yaml`, so the export should default to YAML unless a documented change is approved.
- If YAML serialization needs an explicit Python dependency, add it deliberately instead of relying on transitive packages.
- `apps/web/AGENTS.md` is currently missing even though the root instructions reference it; for TASK-7 implementation, the web side will follow the root repo guidance unless that doc is added separately.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Research summary: the api scaffold can already emit an OpenAPI document directly from `create_app().openapi()` in `apps/api/src/palio/app/factory.py`, so TASK-7 does not need a running server to export the contract.

Research summary: there is no existing `docs/api/` directory or committed OpenAPI artifact yet, and the frontend scaffold currently has no type-generation dependency or script in `apps/web/package.json`.

Implementation summary: added `make openapi-export` plus `palio.app.export_openapi` so the api writes the committed `docs/api/openapi.yaml` artifact directly from `create_app().openapi()` without starting a server.

Implementation summary: added `make openapi-types` / `npm run generate:api-types` using `openapi-typescript`, with generated declarations written under `apps/web/src/app/shared/api/generated/` and ignored from git.

Verification: `make openapi-export`, `make openapi-types`, `cd apps/api && uv run pytest`, `cd apps/web && npm run typecheck`, and `make help` all succeeded in the TASK-7 worktree.

Follow-up adjustment: switched the OpenAPI export CLI wrapper from `argparse` to `typer` and made `typer` an explicit api dependency because the app imports it directly.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added a api-owned OpenAPI export workflow and a frontend type-generation workflow driven by the committed `docs/api/openapi.yaml` artifact. The repo now exposes `make openapi-export` and `make openapi-types`, documents that the spec is committed while generated TS declarations are not, and includes a api test covering the export helper.

Follow-up: the OpenAPI export CLI now uses `typer` instead of `argparse`, with `typer` declared explicitly in the api dependencies.
<!-- SECTION:FINAL_SUMMARY:END -->
