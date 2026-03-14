---
id: TASK-3
title: 'Scaffold the Angular SPA with admin, public, and maxi shells'
status: Done
assignee:
  - '@codex'
created_date: '2026-03-12 01:37'
updated_date: '2026-03-12 17:28'
labels: []
milestone: m-0
dependencies:
  - TASK-1
documentation:
  - docs/architecture/architecture.md
  - docs/qna/ui/frontend architecture.md
  - docs/qna/architecture/module boundaries.md
parent_task_id: M-0
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create the single Angular application with three lazy route shells and the agreed internal folder boundaries for `core`, `features`, and `shared` code.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The web app exposes separate lazy-loaded admin, public, and maxi-screen route areas in one SPA.
- [x] #2 The frontend source layout reflects the documented `core`, `shell-*`, `features`, and `shared/*` boundaries.
- [x] #3 A frontend boundary-check approach is defined so shells and shared code can be enforced by linting or import rules in CI.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Add the Angular project scaffold in `apps/web/` with `package.json`, Angular workspace/config files, and the minimal source/test layout expected by the repo `Makefile` and web README.
2. Create one SPA under `src/app/` with explicit `core/`, `shell-admin/`, `shell-public/`, `shell-maxi/`, `features/`, and `shared/{api,ui,utils,types}` boundaries matching the architecture baseline.
3. Implement the initial app bootstrap and router so admin, public, and maxi areas are separate lazy-loaded route shells with minimal placeholder pages and no accidental eager cross-shell coupling.
4. Add placeholder shell-specific API service layers for admin, public, and realtime access in the documented frontend structure, keeping state feature-local and avoiding a global store.
5. Add an initial frontend boundary-check mechanism that can later run in CI to keep shells isolated and `shared/` generic, choosing the lightest rule/tooling that fits the scaffold.
6. Update affected docs/READMEs/local-dev notes so the frontend scaffold, command behavior, and boundary-check baseline match the implemented repository state.
7. Validate the scaffold with the narrowest honest checks available for TASK-3 (for example install/build/lint or route smoke checks plus the selected boundary-rule command), without expanding into TASK-9’s full frontend and Playwright harness scope.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Started implementation-planning pass after reviewing Backlog workflow overview/task-execution guidance plus architecture/module-boundary and frontend-architecture docs.

Draft plan prepared and internally reviewed. Pending user review before planSet. Material sequencing conflict noted: adding apps/web/package.json will make Makefile test-web and test-e2e stop failing fast even though docs/ops/local-dev.md and TASK-9 say frontend/browser tests become runnable later.

User decision: keep current Makefile behavior, so TASK-3 may make make test-web and make test-e2e stop failing fast before TASK-9 lands. Planning should preserve existing Makefile semantics and align docs later as part of implementation.

Completed the Angular 21 scaffold in /tmp/palio-task-3 with one SPA, lazy-loaded admin/public/maxi route areas, documented src/app boundaries, placeholder API layers, and dependency-cruiser boundary checks.

Validated the scaffold with npm install, npm run typecheck, npm run check-boundaries, and npm run build in apps/web. npm test -- --watch=false and npm run e2e still fail intentionally with the TASK-9 reserved-target message, matching the approved Makefile behavior.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented the initial Angular 21 frontend scaffold for M0 under apps/web. The SPA now boots through standalone Angular configuration, exposes separate lazy-loaded /admin, /public, and /maxi route areas, and uses explicit src/app boundaries for core, shell-admin, shell-public, shell-maxi, features, and shared/{api,ui,utils,types}. Each shell renders a minimal placeholder page through feature-local components backed by separate admin, public, and realtime API service layers, with no global store introduced.

Added dependency-cruiser as the initial frontend architectural guardrail and wired it to npm run check-boundaries so CI can enforce shell isolation and generic shared/core imports. Updated the repository README, apps documentation, local-dev notes, and test-strategy baseline to reflect the new Angular scaffold, current command surface, and the fact that npm test / npm run e2e remain TASK-9 placeholders.

Validation run in apps/web:
- npm install
- npm run typecheck
- npm run check-boundaries
- npm run build
- npm test -- --watch=false (expected TASK-9 placeholder failure)
- npm run e2e (expected TASK-9 placeholder failure)
<!-- SECTION:FINAL_SUMMARY:END -->
