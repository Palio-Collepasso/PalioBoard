---
id: TASK-19.1
title: Implement error catalog validation CLI and repo integration
status: Done
assignee:
  - '@codex'
created_date: '2026-03-18 21:01'
updated_date: '2026-03-18 22:05'
labels:
  - api
  - error-catalog
  - validation
dependencies: []
references:
  - docs/api/errors/index.yaml
  - docs/api/errors/schema.json
  - docs/api/errors/auth.yaml
  - docs/api/errors/users.yaml
  - docs/api/errors/games.yaml
  - docs/api/errors/standings.yaml
  - docs/api/errors/validation.yaml
  - docs/templates/api/errors-area.yaml
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
Build the first tool in the API error-catalog workflow: a validator that can load `docs/api/errors/index.yaml`, resolve imported fragment files, validate the catalog structure against the schema, and enforce the cross-file invariants that downstream generators depend on. This task also owns aligning the active catalog contract with the validator by removing the obsolete `replaced_by` concept from the current docs/schema/templates and by establishing the first stable errors-only validation command in the repo workflow.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 A repo-owned validator loads `docs/api/errors/index.yaml` plus module-aligned imported fragment files, validates the root and fragment documents against `docs/api/errors/schema.json`, and produces one authoritative merged catalog model that preserves owning-module provenance for downstream generators.
- [x] #2 The validator enforces cross-file rules that JSON Schema cannot express by itself, including duplicate symbolic codes across fragments, duplicate `type_slug`, duplicate derived or overridden type URIs, unresolved imports or shared-schema references, and examples whose `context` does not conform to the declared `context_schema`.
- [x] #3 The task removes `replaced_by` from the active error-catalog contract where it is still documented, aligns the catalog split with backend module boundaries, resolves validator-related docs/template/schema contradictions surfaced during implementation, and adds repo integration with tests, a `python -m palio.app.*` CLI entrypoint, and stable grouped make workflow plumbing that later subtasks can extend.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Normalize the catalog layout around backend module ownership before adding more generators. Replace the current area-based fragment split with module-owned files under `docs/api/errors/` that align with `apps/api/src/palio/modules/*` and `docs/architecture/module-map.md`, and update `index.yaml` imports accordingly. The shared loader must preserve owning-module provenance for every error entry.
2. Build a reusable error-catalog core under `apps/api/src/palio/shared/error_catalog/` with a normalized in-memory model for `docs/api/errors/index.yaml` plus imported module fragments. The loader should resolve repo-relative imports from `docs/api/errors/`, parse YAML, validate each document against `docs/api/errors/schema.json`, and return one canonical merged catalog object that later generator tasks can reuse.
3. Implement the cross-file validator in the same shared package. Enforce the invariants JSON Schema cannot express: unique symbolic error codes across all module fragments, unique `type_slug` values, unique derived or overridden problem type URIs, unresolved import/shared-schema reference failures, and `example.context` values that satisfy the declared `context_schema`. Keep `replaced_by` out of the active contract entirely rather than supporting it.
4. Add a repo CLI entrypoint following the existing `python -m palio.app.export_openapi` pattern, likely as `apps/api/src/palio/app/validate_error_catalog.py`. The CLI should validate the committed module-aligned catalog by default, print a concise success summary, and exit non-zero with actionable file/code-path diagnostics on failure.
5. Wire the first stable Makefile surface for this workflow around the three grouped entrypoints requested by the initiative. This task should establish the validation slice and helper plumbing that later generator tasks plug into without renaming the primary grouped interface.
6. Update the authoritative docs and templates so they match the implemented contract. In scope for this task: `docs/api/errors/README.md` to remove the obsolete `replaced_by` rule and describe the module-aligned validator-backed checks, `docs/api/README.md` to document the new validation command surface, and `docs/templates/api/errors-area.yaml` only if template guidance conflicts with the validator/schema or with module ownership.
7. Add tests that prove the foundation is correct before any generators land. Cover a successful validation of the committed catalog, duplicate code/type_slug/type URI failures, missing import/shared-schema failures, invalid example context failures, module-provenance preservation, and CLI exit behavior under `apps/api/tests/unit/`. If the validator exposes a pure library API, keep the test coverage focused there and add one thin CLI smoke test.
8. Validate the implementation with the repo’s stable checks that exercise the changed surface: the grouped errors workflow, the new CLI, `make test-api-unit`, `make lint`, and `make typecheck`. Use `make check-openapi` only if this task changes the committed OpenAPI artifact or the shared contract plumbing it depends on.
9. Prerequisites and checkpoints: confirm the module-to-fragment mapping against `docs/architecture/module-map.md`, confirm the merged model shape is stable enough for TASK-19.2 through TASK-19.6, and stop if any additional doc conflict appears beyond the current `replaced_by` mismatch in the error-catalog guide.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Planning review completed: implementation plan approved pending user final execution approval.

Execution review: corrected the shared loader to validate root and fragment documents against different schema shapes, enabled JSON Schema format checking for URI/UUID validation, and fixed the temporary test fixture so the missing-module-import case actually exercises module-alignment failures.

Validation run: `env -u VIRTUAL_ENV UV_CACHE_DIR=/tmp/uv-cache uv run --group dev pytest tests/unit/test_error_catalog.py` passed with `10 passed in 0.61s`.

Validation run: `env -u VIRTUAL_ENV UV_CACHE_DIR=/tmp/uv-cache uv run --group dev python -m palio.app.validate_error_catalog ../../docs/api/errors/index.yaml` succeeded with `Validated 11 module fragments, 0 error entries, and 6 shared context schemas.`.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented the shared error-catalog foundation under `palio.shared.error_catalog`, added the validator CLI and grouped make plumbing, split `docs/api/errors/` into module-aligned fragments, removed `replaced_by` from the active catalog guidance, added unit coverage, and reviewed/fixed the worker patch before acceptance. Final review fixes included using a fragment-specific schema view for imported YAML files, enabling format-aware validation, and correcting the missing-module-import test fixture.
<!-- SECTION:FINAL_SUMMARY:END -->
