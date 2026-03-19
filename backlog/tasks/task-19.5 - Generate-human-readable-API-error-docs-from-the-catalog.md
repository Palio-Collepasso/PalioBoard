---
id: TASK-19.5
title: Generate human-readable API error docs from the catalog
status: Done
assignee:
  - '@codex'
created_date: '2026-03-18 21:01'
updated_date: '2026-03-18 22:30'
labels:
  - api
  - error-catalog
  - docs
  - codegen
dependencies:
  - TASK-19.1
references:
  - docs/api/errors/index.yaml
  - docs/api/errors/schema.json
  - docs/api/error-contract.md
  - docs/api/errors/examples/example.yaml
  - docs/api/errors/examples/example.md
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
Generate committed human-readable API error documentation from the validated catalog, with `docs/api/error-contract.md` as the minimum required artifact. The generated doc must own the `# Error Catalog` section and render errors under subsections grouped by their source fragment provenance, such as `## Users` for `users.yaml`, following the example contract structure already checked into the repo.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 `docs/api/error-contract.md` is generated from `docs/api/errors/index.yaml` and imported module-aligned fragment files, and the generator owns the `# Error Catalog` section with module-provenance-grouped subsections such as `## Event Operations`, `## Results`, and `## Season Setup`.
- [x] #2 Generated per-error documentation follows the structure shown by `docs/api/errors/examples/example.yaml` and `docs/api/errors/examples/example.md`, including stable identity metadata, meaning, recommended status, exposure and retry fields, context-schema details, and wrapped RFC 9457 examples when example data exists.
- [x] #3 The task adds deterministic tests, documentation updates, and repo integration so docs generation participates in the shared errors-only and broader api/combined make workflows and keeps the human guidance docs aligned with the generated contract.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Prerequisites and scope lock
- Consume TASK-19.1’s validated/merged module-aligned catalog model first and confirm it preserves owning-module provenance for each imported error entry.
- Treat `docs/api/error-contract.md` as a hybrid document: hand-authored prose may stay above the generated catalog block, but the generator owns the `# Error Catalog` section and everything under it.

2. Generator implementation
- Add a new API-side export module under `apps/api/src/palio/app/` beside `export_openapi.py` to render `docs/api/error-contract.md` from `docs/api/errors/index.yaml` plus imported module fragments.
- Group emitted errors by module provenance in import order, so fragments like `event_operations.yaml`, `results.yaml`, and `season_setup.yaml` render as `## Event Operations`, `## Results`, and `## Season Setup`.
- Render each error using the structure shown in `docs/api/errors/examples/example.md`, and when an authored example exists in `docs/api/errors/examples/example.yaml`, wrap the example context into the full RFC 9457 envelope deterministically.
- Keep ordering stable within each module group, and omit any `replaced_by` handling from both generated output and supporting docs because the active contract no longer uses it.

3. Repo integration
- Extend the top-level grouped workflows for errors, api, and combined contract work, then wire the docs generator into the appropriate flow(s).
- Update `docs/api/README.md`, `docs/api/errors/README.md`, and `docs/ops/local-dev.md` so the generation workflow, the generated-doc boundary, and the grouped workflows are documented in one place.
- Update `docs/engineering/documentation-impact-matrix.md` only if the new committed/generated-doc workflow changes the document ownership notes.

4. Tests and validation
- Add unit coverage for module-provenance grouping, example wrapping, and the absence of `replaced_by` in generated output.
- Add drift-style checks that generate the doc to a temp path and compare the committed `docs/api/error-contract.md` output for the generated section.
- Validate the full path with the grouped workflows, then re-run `make openapi-export`, `make openapi-types`, and `make check-openapi` to ensure the docs workflow does not disturb the existing API contract workflow.

5. Risks and checkpoints
- TASK-19.1 must supply module provenance metadata; without it, grouped documentation cannot be deterministic.
- Keep endpoint-to-error routing out of the catalog and out of this generator; OpenAPI remains the source of truth for which endpoints can return which errors.
- The catalog is currently sparse, so tests should be written to tolerate future errors while still enforcing stable grouping and example shape.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Planning review completed: implementation plan approved pending user final execution approval.

Implemented the docs generator under `palio.app.generate_error_docs` plus the shared markdown renderer in `palio.shared.error_catalog.docs_codegen`. The generator owns the `# Error Catalog` section and renders module-provenance groups in catalog import order, with placeholder sections for currently empty modules.

Added deterministic unit coverage for example rendering, module grouping order, committed-doc drift, and write-path behavior in `apps/api/tests/unit/test_generate_error_docs.py`.

Validation run: `env -u VIRTUAL_ENV UV_CACHE_DIR=/tmp/uv-cache uv run --group dev pytest tests/unit/test_generate_error_docs.py` passed with `4 passed in 0.54s`.

Validation run: `env -u VIRTUAL_ENV UV_CACHE_DIR=/tmp/uv-cache uv run --group dev ruff check src/palio/app/generate_error_docs.py src/palio/shared/error_catalog/docs_codegen.py tests/unit/test_generate_error_docs.py` passed.

Validation run: `env -u VIRTUAL_ENV UV_CACHE_DIR=/tmp/uv-cache uv run --group dev python -m palio.app.generate_error_docs ../../docs/api/errors/index.yaml --output ../../docs/api/error-contract.md` regenerated the committed markdown artifact, and a diff against the temp output was clean.

Validation run: `env -u VIRTUAL_ENV UV_CACHE_DIR=/tmp/uv-cache uv run --group dev python -m palio.app.validate_error_catalog ../../docs/api/errors/index.yaml` still succeeds after the docs update.

Review accepted: added `palio.app.generate_error_docs`, `palio.shared.error_catalog.docs_codegen`, deterministic module-grouped rendering, and committed `docs/api/error-contract.md`.

Validation run: `env -u VIRTUAL_ENV UV_CACHE_DIR=/tmp/uv-cache uv run --group dev pytest tests/unit/test_generate_error_docs.py` passed with `4 passed`.

Validation run: `env -u VIRTUAL_ENV UV_CACHE_DIR=/tmp/uv-cache uv run --group dev python -m palio.app.generate_error_docs ../../docs/api/errors/index.yaml --output ../../docs/api/error-contract.md` regenerated the committed contract.

Integration note: the generated contract currently renders deterministic empty-module placeholder sections because the committed catalog still has zero error entries.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented human-readable error-contract generation with a dedicated CLI, shared Markdown renderer, deterministic module-provenance grouping, and example-structure regression tests against the checked-in catalog example. `docs/api/error-contract.md` is now generator-owned and committed.
<!-- SECTION:FINAL_SUMMARY:END -->
