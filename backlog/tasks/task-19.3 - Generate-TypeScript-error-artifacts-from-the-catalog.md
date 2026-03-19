---
id: TASK-19.3
title: Generate TypeScript error artifacts from the catalog
status: Done
assignee:
  - '@codex'
created_date: '2026-03-18 21:01'
updated_date: '2026-03-18 22:30'
labels:
  - api
  - error-catalog
  - typescript
  - codegen
dependencies:
  - TASK-19.1
references:
  - docs/api/errors/index.yaml
  - docs/api/errors/schema.json
  - apps/web/src/app/
  - apps/web/src/app/shared/api/generated/
  - apps/web/package.json
  - Makefile
documentation:
  - docs/architecture/adr/ADR-0010-error-catalog-and-problem-details.md
  - docs/api/README.md
  - docs/api/errors/README.md
  - docs/api/error-contract.md
  - docs/engineering/documentation-impact-matrix.md
parent_task_id: TASK-19
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Generate committed TypeScript-side error artifacts from the validated catalog so frontend code can match on stable error codes and context payloads safely without maintaining a parallel manual error registry. Keep the catalog endpoint-independent and follow the repo’s committed-artifact workflow for generated files.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The repository has one committed merged TypeScript artifact generated from the catalog at `apps/web/src/app/shared/api/generated/error-codes.generated.ts`, exposing stable frontend error-code constants or unions, problem-shape typing, typed context payloads, and safe helpers for matching on catalog-defined error codes.
- [x] #2 The generated TypeScript output is deterministic, module-agnostic on the frontend side, and derived from the catalog rather than from duplicated frontend-maintained error definitions, while staying faithful to the declared wire contract fields (`type`, `code`, `status`, `title`, `context`).
- [x] #3 The task adds tests, documentation updates, and repo integration so the TypeScript generator participates in the shared errors-only and broader api/combined make workflows and fits the existing frontend typecheck flow.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Prerequisites
- Wait for TASK-19.1 to land the validated/merged catalog model with module provenance, and keep this task pinned to that output contract.
- Keep the generator endpoint-independent: it must consume only catalog data, not OpenAPI path ownership or any removed `replaced_by` metadata.

1. Add the repo-owned catalog generator entrypoint on the API/Python side
- Add a Python CLI in the API toolchain that follows the existing `python -m palio.app.export_openapi` pattern, with a sibling entrypoint for exporting validated error-catalog-derived frontend artifacts.
- Make the API-side CLI the primary generator path for this task; it should read the merged catalog model from TASK-19.1 and emit one committed merged TypeScript artifact at `apps/web/src/app/shared/api/generated/error-codes.generated.ts`.
- Generate stable TS surfaces for catalog-defined `code`, `type`, `status`, and `title`, plus typed `context` aliases or maps derived from each catalog `context_schema`.
- Include safe helpers that match on catalog-defined `code` and `type` only, such as `isCatalogErrorCode`, `isCatalogProblem`, and `matchesCatalogErrorCode`; do not add matching logic based on `title`.
- Keep the active contract free of `replaced_by` compatibility logic.

2. Wire the grouped repo command surface
- Add explicit top-level grouped workflows for errors, api, and combined contract work, while keeping low-level helper targets available for the underlying export/validation steps.
- Route the new Python catalog CLI into the grouped workflows where appropriate, alongside the existing OpenAPI export/type generation steps.
- Preserve a clear separation between validation-only steps and generation steps so the grouped workflows can be used for preflight checks and for committed artifact regeneration.
- Keep `apps/web/src/app/shared/api/generated/error-codes.generated.ts` committed, and make the ignore policy explicit so the repo does not continue treating that path as throwaway generated output.

3. Update authoritative workflow docs
- Update `docs/api/README.md` to describe the new grouped workflows and restate that the catalog is endpoint-independent while OpenAPI owns endpoint-to-error mapping.
- Update `docs/api/errors/README.md` to remove `replaced_by`, document the merged frontend artifact location, and keep the contract field set anchored to `type`, `code`, `status`, `title`, and `context`.
- Update `apps/web/README.md` and `docs/ops/local-dev.md` so the documented command surface reflects the committed-artifact workflow and the new grouped targets.
- Do not own regeneration of `docs/api/error-contract.md` here; that remains TASK-19.5.

4. Validate the change
- Add determinism checks for the generator output so the emitted merged TS artifact can be verified against the committed file.
- Run the grouped errors workflow, then the grouped combined contract workflow, to verify the new entrypoint participates in the intended repo surface.
- Run `make openapi-export`, `make openapi-types`, `make check-openapi`, and `make typecheck` to prove the frontend still compiles against the new generated types.
- Run `make test-web` if the generated helper is imported by web code.

Risks and checkpoints
- TASK-19.1 output shape must be stable before this task lands.
- The schema-to-TypeScript mapping is the main technical risk, especially nested `context_schema` shapes, optional fields, enums, and object index signatures.
- The committed generated file under `apps/web/src/app/shared/api/generated/` needs an explicit tracked-file policy because the directory is currently ignored.
- No endpoint-specific routing should leak into the catalog output, and no human-doc generation for `docs/api/error-contract.md` should be pulled into this task.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Planning review completed: implementation plan approved pending user final execution approval.

Execution review: added `apps/api/src/palio/app/generate_ts_errors.py` and `apps/api/src/palio/shared/error_catalog/ts_codegen.py` to render a merged frontend error-codes artifact from the validated catalog without touching the accepted loader/model surface.

Execution review: emitted and committed `apps/web/src/app/shared/api/generated/error-codes.generated.ts`, including module-order constants, `ErrorCode`/module unions, per-error context typing, runtime metadata, and safe helpers for matching and probing catalog problems.

Repo integration review: narrowed `apps/web/.gitignore` so the new generated artifact is tracked while the existing generated OpenAPI declaration remains ignored.

Validation run: `env -u VIRTUAL_ENV UV_CACHE_DIR=/tmp/uv-cache uv run --group dev pytest tests/unit/test_error_catalog.py tests/unit/test_generate_ts_errors.py` passed with `13 passed in 0.59s`.

Validation run: `env -u VIRTUAL_ENV UV_CACHE_DIR=/tmp/uv-cache uv run --group dev ruff check src/palio/app/generate_ts_errors.py src/palio/shared/error_catalog/ts_codegen.py tests/unit/test_generate_ts_errors.py` passed.

Validation run: `env -u VIRTUAL_ENV UV_CACHE_DIR=/tmp/uv-cache uv run --group dev python -m palio.app.generate_ts_errors --output ../../apps/web/src/app/shared/api/generated/error-codes.generated.ts` succeeded and wrote `/home/simone/projects/palio/apps/web/src/app/shared/api/generated/error-codes.generated.ts`.

Review accepted after one revision: the generated `isCatalogProblem` guard now uses bracket access under the repo TS settings and verifies catalog membership with `isCatalogErrorCode(code)`.

Validation run: `env -u VIRTUAL_ENV UV_CACHE_DIR=/tmp/uv-cache uv run --group dev pytest tests/unit/test_error_catalog.py tests/unit/test_generate_ts_errors.py` passed.

Validation run: `npm run typecheck` in `apps/web` passed after regenerating `apps/web/src/app/shared/api/generated/error-codes.generated.ts`.

Integration note: `apps/web/.gitignore` now allows the committed generated frontend artifacts and the grouped `make errors` workflow regenerates the merged TS error catalog file.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented the merged frontend TypeScript error artifact with an API-side generator CLI, shared TS renderer, committed `apps/web/src/app/shared/api/generated/error-codes.generated.ts`, and regression coverage for the generated type guards and context typing. Repo docs and ignore policy now treat the generated frontend error artifact as committed output.
<!-- SECTION:FINAL_SUMMARY:END -->
