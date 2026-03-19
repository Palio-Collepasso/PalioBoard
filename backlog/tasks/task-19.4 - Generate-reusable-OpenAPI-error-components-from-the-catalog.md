---
id: TASK-19.4
title: Generate reusable OpenAPI error components from the catalog
status: Done
assignee:
  - '@codex'
created_date: '2026-03-18 21:01'
updated_date: '2026-03-18 22:30'
labels:
  - api
  - error-catalog
  - openapi
  - codegen
dependencies:
  - TASK-19.1
references:
  - docs/api/errors/index.yaml
  - docs/api/errors/schema.json
  - docs/api/openapi.yaml
  - apps/api/src/palio/app/export_openapi.py
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
Generate committed reusable OpenAPI error components from the validated catalog so the API contract can reference one catalog-derived set of problem schemas, examples, and shared responses without duplicating error definitions inside endpoint docs. This task must preserve the contract split where the catalog defines what an error is and OpenAPI defines which endpoints return it.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The repository has one committed OpenAPI/problem-details artifact generated from the catalog under `docs/api/`, containing the base problem shape plus per-error schemas, examples, and reusable response components or equivalent reusable structures.
- [x] #2 The generated OpenAPI/problem-details artifact remains endpoint-independent, and the committed `docs/api/openapi.yaml` references or composes it using one documented convention while endpoint-to-error mapping remains authored in OpenAPI.
- [x] #3 The task adds deterministic tests, documentation updates, and repo integration so OpenAPI error-component generation participates in the shared errors-only and broader api/combined make workflows alongside the existing OpenAPI export/type-generation workflow.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Implement the reusable OpenAPI/problem-details generator as a new CLI module in `apps/api/src/palio/app/` alongside `export_openapi.py`, consuming the validated/merged catalog model from TASK-19.1 and writing one committed catalog-derived artifact under `docs/api/` (for example a generated `problem-details.gen.yaml`) containing the base problem envelope plus per-error schemas, examples, and shared responses.
2. Add an explicit post-export composition seam so the committed `docs/api/openapi.yaml` stays self-contained with local `#/components/...` refs in the final artifact: `export_openapi.py` should remain the FastAPI export entrypoint, then a follow-up composition step injects the generated problem-details artifact into the exported spec and rewrites or normalizes the relevant operation responses so `openapi-typescript` consumes one committed spec with local component references. The generator remains endpoint-independent and never decides which endpoints return which errors.
3. Lock one documented reference convention that both the generator and TASK-19.6 checker enforce: catalog-driven errors are exposed through local component names under `#/components/responses/<Name>` and, where needed, local component schemas/examples beneath `#/components/schemas` and `#/components/examples`, with endpoint-level mapping authored in `docs/api/openapi.yaml` rather than in the catalog or generator.
4. Wire repo workflow around the three top-level grouped surfaces requested by the initiative: an errors workflow group, an api workflow group, and a combined contract workflow group. Keep any low-level helper targets underneath those groups if useful, but make the top-level grouped surface obvious and primary.
5. Make the new generator participate in the grouped workflows as appropriate, and make the combined contract workflow run the same post-export composition path before drift checks and type generation so `make openapi-export`, `make check-openapi`, and the combined group all verify the same committed `docs/api/openapi.yaml` shape.
6. Add deterministic unit tests under `apps/api/tests/unit/` for artifact emission, component naming, composition into the exported spec, stable local `$ref` output, and idempotent regeneration; keep the checks focused on generation/composition drift rather than runtime API behavior.
7. Update the workflow-facing authoritative docs that describe this change, especially `docs/api/README.md` and `docs/api/errors/README.md`, and reconcile the active catalog contract so the plan and docs no longer depend on `replaced_by` in the current format. Leave generated human-readable error documentation ownership to TASK-19.5.
8. Checkpoints/prerequisites: TASK-19.1 must supply the merged validated catalog model; TASK-19.6 must use the same local-component convention so validation and generation stay aligned; and if the FastAPI export plus post-compose seam cannot preserve a stable committed spec with local refs, pause and resolve that seam before broadening scope.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Planning review completed: implementation plan approved pending user final execution approval.

Review accepted with one integration fix: kept FastAPI export in the app-layer CLI and left pure render/compose logic in `palio.shared.error_catalog.openapi_codegen`, rather than importing `create_app()` from the shared package.

Validation run: `env -u VIRTUAL_ENV UV_CACHE_DIR=/tmp/uv-cache uv run --group dev pytest tests/unit/test_generate_openapi_error_components.py tests/unit/test_error_catalog.py` passed with `15 passed`.

Validation run: `env -u VIRTUAL_ENV UV_CACHE_DIR=/tmp/uv-cache uv run --group dev python -m palio.app.generate_openapi_error_components ../../docs/api/errors/index.yaml --artifact-output ../../docs/api/problem-details.openapi.gen.yaml --openapi-output ../../docs/api/openapi.yaml` regenerated the committed artifact and composed spec.

Integration note: `make openapi-export` now produces the composed committed OpenAPI spec plus `docs/api/problem-details.openapi.gen.yaml`, and `make api-contract` validates that path before the clean-tree drift check.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented reusable OpenAPI problem-details generation with a dedicated CLI, shared renderer/composer, committed `docs/api/problem-details.openapi.gen.yaml`, and a composed committed `docs/api/openapi.yaml` that carries local `#/components/...` refs. The task includes deterministic unit coverage and repo workflow integration for the composed export path.
<!-- SECTION:FINAL_SUMMARY:END -->
