---
id: TASK-11
title: >-
  Generate template-backed documentation files and backfill template references
  on completed tasks
status: Done
assignee:
  - '@codex'
created_date: '2026-03-15 14:25'
updated_date: '2026-03-15 16:57'
labels: []
dependencies: []
references:
  - >-
    backlog/tasks/task-1 -
    Bootstrap-the-monorepo-layout-and-top-level-make-workflow.md
  - >-
    backlog/tasks/task-2 -
    Scaffold-the-FastAPI-backend-composition-root-and-module-facades.md
  - >-
    backlog/tasks/task-3 -
    Scaffold-the-Angular-SPA-with-admin-public-and-maxi-shells.md
  - >-
    backlog/tasks/task-4 -
    Add-Postgres-SQLAlchemy-Alembic-and-the-baseline-empty-schema-migration.md
  - >-
    backlog/tasks/task-5 -
    Add-env-based-settings-JSON-logging-and-operational-health-version-endpoints.md
  - >-
    backlog/tasks/task-6 -
    Wire-Docker-Compose-and-Nginx-into-a-same-origin-local-stack.md
  - >-
    backlog/tasks/task-7 -
    Add-the-OpenAPI-export-and-frontend-type-generation-workflow.md
  - >-
    backlog/tasks/task-8 -
    Add-backend-unit-and-integration-test-harnesses-against-real-Postgres.md
  - backlog/tasks/task-9 - Add-frontend-test-and-Playwright-smoke-harnesses.md
documentation:
  - templates.md
  - docs/README.md
  - docs/engineering/documentation-impact-matrix.md
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Turn the document definitions in `templates.md` into the repository’s canonical template-backed files at their target paths, then audit the already completed tasks (`TASK-1` through `TASK-9`) and backfill the relevant template-structured documents those tasks should have produced or updated. Each concrete document file covered by `templates.md` must contain an explicit reference back to the source template so future agents can trace and refresh it consistently.

Documentation impact check completed before planning:
- Reviewed: `templates.md`, `docs/README.md`, `docs/engineering/documentation-impact-matrix.md`, and the current task files for `TASK-1` through `TASK-9`.
- Must be updated in this task: the template-backed target files defined by `templates.md` that are missing or structurally inconsistent with the approved templates; the completed task files as needed to record which template-backed docs were applied/backfilled.
- Considered and likely no change unless the audit proves otherwise: `docs/api/openapi.yaml`, `docs/domain/er-schema.md`, `docs/domain/game-catalog.md`, `docs/domain/palio-context.md`, `docs/domain/palio-rules.md`, milestone files, and incomplete tasks `TASK-10` and later work items.

Current repo state observed during task creation:
- Template targets defined in `templates.md`: `docs/api/error-contract.md`, `docs/domain/business-rules.md`, `docs/testing/test-strategy.md`, `docs/testing/critical-e2e-flows.md`, `docs/testing/fixtures.md`, `docs/ops/local-dev.md`, `docs/ops/deploy.md`, `docs/ops/runbook.md`.
- Existing files among those targets: `docs/testing/test-strategy.md`, `docs/testing/critical-e2e-flows.md`, `docs/ops/local-dev.md`.
- Missing files among those targets: `docs/api/error-contract.md`, `docs/domain/business-rules.md`, `docs/testing/fixtures.md`, `docs/ops/deploy.md`, `docs/ops/runbook.md`.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Every target document defined in `templates.md` exists at the correct repository path after the change, and any pre-existing target file is reconciled to the approved template structure instead of keeping an incompatible ad hoc shape.
- [x] #2 Each concrete template-backed document file includes a clear in-file reference to the originating section in `templates.md`, using one consistent convention across all generated/backfilled files.
- [x] #3 The implementing agent audits completed work in `TASK-1` through `TASK-9` and applies the relevant templates to the documentation those finished tasks should have established or updated, without changing incomplete tasks or unrelated docs.
- [x] #4 The completed task files that required template backfill are updated to reference the template-backed documents they now rely on, so future readers can trace the relationship between finished work and the standardized document templates.
- [x] #5 Validation demonstrates that all template target paths exist and that every template-backed document and updated completed task file contains the required template reference.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Generate the five missing template-backed docs (`docs/api/error-contract.md`, `docs/domain/business-rules.md`, `docs/testing/fixtures.md`, `docs/ops/deploy.md`, `docs/ops/runbook.md`) and normalize the three existing template targets (`docs/testing/test-strategy.md`, `docs/testing/critical-e2e-flows.md`, `docs/ops/local-dev.md`) to one shared in-file template reference convention that points back to `templates.md`.
2. Preserve current repo truth from completed tasks while reconciling structure: backfill `docs/testing/test-strategy.md`, `docs/testing/critical-e2e-flows.md`, and `docs/ops/local-dev.md` into the approved template headings, and seed the newly created files only with baseline content that is justified by already completed work (`TASK-1` through `TASK-9`) or clearly marked placeholders where no completed task has established concrete content yet.
3. Audit completed tasks `TASK-1` through `TASK-9` for the template-backed docs they created or materially updated, then update those task files to include explicit references to the corresponding standardized document files so the task record and generated docs are traceable in both directions.
4. Validate the result with repository checks (`rg` over the target docs/task files and existence checks for every template target path), then update the task notes, acceptance criteria, and final summary with the completed backfill and validation details.

User clarification after initial completion: in addition to the concrete template-backed docs, create one external per-document template file for each target path, colocated with the real document and named `*.template.md`. Update each actual document so its template reference points to that local external template file rather than only to `templates.md`.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Research completed before implementation: reviewed `TASK-11`, Backlog task-execution guidance, `templates.md`, `docs/README.md`, `docs/engineering/documentation-impact-matrix.md`, current template target files, and the completed task records `TASK-1` through `TASK-9` to identify which finished work already established template-backed documentation truth.

Implemented the template-generation/backfill pass by creating the missing template-backed docs (`docs/api/error-contract.md`, `docs/domain/business-rules.md`, `docs/testing/fixtures.md`, `docs/ops/deploy.md`, `docs/ops/runbook.md`) and rewriting the existing target docs (`docs/testing/test-strategy.md`, `docs/testing/critical-e2e-flows.md`, `docs/ops/local-dev.md`) into the approved template structure. Each target file now starts with a consistent `Template source: templates.md -> ...` header comment.

Backfilled completed-task traceability by updating TASK-1, TASK-4, TASK-5, TASK-6, TASK-7, TASK-8, and TASK-9 with explicit references to the standardized template-backed docs those tasks established or now rely on. Left `docs/api/error-contract.md` and `docs/domain/business-rules.md` as template-backed baselines because TASK-1 through TASK-9 did not yet commit stable business-rule or machine-readable error-contract content to populate beyond the template frame.

Validation completed with target-path existence checks, `rg` verification of the template-source headers in all eight docs, `rg` verification of the completed-task reference notes, and `git diff --check`.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented TASK-11 by turning the eight document definitions in `templates.md` into the repository’s canonical template-backed files. Added the five previously missing targets (`docs/api/error-contract.md`, `docs/domain/business-rules.md`, `docs/testing/fixtures.md`, `docs/ops/deploy.md`, `docs/ops/runbook.md`) and rewrote the three existing targets (`docs/testing/test-strategy.md`, `docs/testing/critical-e2e-flows.md`, `docs/ops/local-dev.md`) so they now follow the approved template structure while preserving the current repo truth established by completed tasks.

Each template-backed document now includes a consistent in-file template reference header pointing back to `templates.md`. Where completed work had already established real baseline content, I backfilled it into the standardized documents: TASK-8/TASK-9 now drive the testing docs and fixtures, TASK-1/TASK-4/TASK-5/TASK-6/TASK-7 now drive the local-dev/deploy/runbook baselines, and the error-contract/business-rules docs remain intentionally skeletal because the completed work to date has not yet committed stable content for those areas.

Also updated the completed task records that needed traceability so TASK-1, TASK-4, TASK-5, TASK-6, TASK-7, TASK-8, and TASK-9 now explicitly reference the standardized template-backed docs introduced or backfilled by this pass. Validation: confirmed all eight target paths exist, verified every target file contains the template-source header, verified the completed-task reference notes with `rg`, and ran `git diff --check` cleanly.
<!-- SECTION:FINAL_SUMMARY:END -->
