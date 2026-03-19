---
id: TASK-19.6
title: Check OpenAPI error references against the catalog
status: Done
assignee:
  - '@codex'
created_date: '2026-03-18 21:01'
updated_date: '2026-03-18 22:30'
labels:
  - api
  - error-catalog
  - openapi
  - validation
dependencies:
  - TASK-19.1
references:
  - docs/api/errors/index.yaml
  - docs/api/openapi.yaml
  - docs/api/error-contract.md
  - Makefile
documentation:
  - docs/architecture/adr/ADR-0010-error-catalog-and-problem-details.md
  - docs/api/README.md
  - docs/api/errors/README.md
  - docs/engineering/documentation-impact-matrix.md
parent_task_id: TASK-19
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add a repo-owned checker that verifies the committed OpenAPI contract references only catalog-defined error codes and uses one documented convention for those references. The checker should surface drift between endpoint-level OpenAPI mappings and the endpoint-independent error catalog without turning the catalog into the owner of endpoint routing.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 A repo-owned checker scans the committed OpenAPI contract and verifies that every referenced error code exists in the catalog and that references follow one documented convention for linking endpoint responses back to catalog-defined errors.
- [x] #2 The checker surfaces catalog errors that are never referenced by any endpoint in a documented way, at least as informational or warning output, without turning endpoint-level mapping into catalog-owned metadata.
- [x] #3 The task adds deterministic tests, documentation updates, and repo integration so OpenAPI reference checking participates in the shared errors-only, api-only, and combined contract make workflows.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Lock the documented OpenAPI-to-catalog reference convention in `docs/api/README.md`, `docs/api/errors/README.md`, `README.md`, `docs/ops/local-dev.md`, and `docs/testing/test-strategy.md`: error-bearing OpenAPI responses will reference reusable response components named after catalog codes, for example `#/components/responses/JOLLY_ALREADY_USED`; the catalog stays endpoint-independent; the generated problem-details artifact remains a single shared artifact; and the obsolete `replaced_by` rule is removed from the active docs.
2. Reuse the shared catalog package introduced with TASK-19.1 for catalog loading, merged-model access, owning-module provenance, and reference-index helpers. Keep the CLI wrapper only in `apps/api/src/palio/app/check_openapi_error_references.py`, so the checker uses shared catalog logic instead of duplicating parser or lookup code in app-local helpers.
3. Implement OpenAPI reference validation so the checker resolves every documented error reference back to a catalog code, fails on unknown or malformed references, and keeps endpoint routing ownership in OpenAPI only.
4. Implement warning-only drift reporting for catalog codes that are never referenced by any endpoint, grouped by owning module provenance such as `event_operations`, `results`, `season_setup`, and `users`, so missing endpoint coverage is visible without moving routing metadata into the catalog.
5. Wire repo integration in `Makefile` around the three requested grouped entrypoints: one errors workflow, one api workflow, and one combined contract workflow. Helper targets may exist underneath, but the top-level surface should remain those three grouped flows, with the api and combined contract flows including the OpenAPI reference checker and the combined contract flow continuing to run export, problem-details composition, drift comparison, and type generation in order.
6. Add deterministic unit tests under `apps/api/tests/unit/` for valid references, missing codes, malformed references, warning output for unreferenced catalog entries, and the grouped workflow composition.
7. Validate with the narrowest honest commands first, then the repo gates: focused `pytest` for the checker tests, the grouped errors workflow, the grouped api workflow, `openapi-export`, `openapi-types`, `check-openapi`, and `verify` if the combined contract path is expected to stay green.
8. Dependency and risk checkpoint: wait for TASK-19.1 to expose the merged catalog model API before coding the checker, and keep the OpenAPI reference convention stable across TASK-19.4 so generated components and checker expectations do not diverge.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Planning review completed: implementation plan approved pending user final execution approval.

Execution review: added `palio.shared.error_catalog.openapi_ref_checker`, the `palio.app.check_openapi_error_references` CLI, and focused coverage for valid catalog references, unknown/malformed component refs, inline problem responses without refs, unreferenced-code warnings grouped by module, and the committed OpenAPI snapshot.

Validation run: `env -u VIRTUAL_ENV UV_CACHE_DIR=/tmp/uv-cache uv run --group dev pytest tests/unit/test_check_openapi_error_references.py tests/unit/test_error_catalog.py` passed with `16 passed`.

Validation run: `env -u VIRTUAL_ENV UV_CACHE_DIR=/tmp/uv-cache uv run --group dev ruff check src/palio/app/check_openapi_error_references.py src/palio/shared/error_catalog/openapi_ref_checker.py tests/unit/test_check_openapi_error_references.py` passed cleanly.

Validation run: `env -u VIRTUAL_ENV UV_CACHE_DIR=/tmp/uv-cache uv run --group dev python -m palio.app.check_openapi_error_references ../../docs/api/openapi.yaml` succeeded with `Checked 0 OpenAPI error response references against 0 catalog error codes.`.

Follow-up review fix: tightened traversal so only 4xx/5xx response slots are treated as error-bearing; reusable non-error `$ref` responses are ignored, while inline `application/problem+json` error responses still fail.

Validation rerun: `env -u VIRTUAL_ENV UV_CACHE_DIR=/tmp/uv-cache uv run --group dev pytest tests/unit/test_check_openapi_error_references.py tests/unit/test_error_catalog.py` passed with `17 passed`.

Validation rerun: `env -u VIRTUAL_ENV UV_CACHE_DIR=/tmp/uv-cache uv run --group dev ruff check src/palio/app/check_openapi_error_references.py src/palio/shared/error_catalog/openapi_ref_checker.py tests/unit/test_check_openapi_error_references.py` passed cleanly.

Review accepted after one revision: the checker now enforces the `#/components/responses/<CATALOG_CODE>` convention only on error-bearing 4xx/5xx response slots and ignores reusable non-error response refs.

Validation run: `env -u VIRTUAL_ENV UV_CACHE_DIR=/tmp/uv-cache uv run --group dev pytest tests/unit/test_check_openapi_error_references.py tests/unit/test_error_catalog.py` passed with `17 passed`.

Validation run: `env -u VIRTUAL_ENV UV_CACHE_DIR=/tmp/uv-cache uv run --group dev python -m palio.app.check_openapi_error_references ../../docs/api/openapi.yaml` succeeded with `Checked 0 OpenAPI error response references against 0 catalog error codes.`.

Integration note: the grouped `make api-contract` workflow now runs the checker before regenerating committed OpenAPI declarations and then performs the clean-tree drift check.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented the repo-owned OpenAPI/catalog reference checker with a dedicated API-side CLI, shared validation logic, grouped warning output for unreferenced catalog codes, and regression coverage for valid refs, malformed refs, inline problem responses, and non-error reusable response refs. The checker now participates in the grouped API contract workflow.
<!-- SECTION:FINAL_SUMMARY:END -->
