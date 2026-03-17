---
id: TASK-2
title: Scaffold the FastAPI api composition root and module facades
status: Done
assignee:
  - '@codex'
created_date: '2026-03-12 01:37'
updated_date: '2026-03-13 17:19'
labels: []
milestone: m-0
dependencies:
  - TASK-1
documentation:
  - docs/architecture/architecture.md
  - docs/qna/architecture/module boundaries.md
parent_task_id: M-0
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create the api application skeleton around FastAPI, explicit composition-root wiring, and the approved modular-monolith module layout so later slices can add behavior without reshaping the baseline.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The api package layout matches the documented modules and each module exposes a public facade entrypoint.
- [x] #2 The app boots with a minimal FastAPI composition root and placeholder wiring that keeps orchestration explicit and avoids a DI framework.
- [x] #3 A api boundary-check mechanism is defined so forbidden cross-module imports can be enforced once CI is wired.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Add the api Python project scaffold in `apps/api/` with `pyproject.toml`, package metadata, and the minimal source/test layout expected by the repo `Makefile` and api README.
2. Create `src/palio/app/` as the explicit composition root with a small FastAPI app factory, startup wiring helpers, and placeholder admin/public/realtime routing surfaces that keep dependency assembly manual and DI-framework-free.
3. Create shared api support packages (`db/`, `shared/`) only for cross-cutting technical primitives needed by the scaffold, keeping business ownership inside bounded modules.
4. Create every documented api module under `src/palio/modules/` (`identity`, `authorization`, `users`, `season_setup`, `event_operations`, `results`, `tournaments`, `live_games`, `leaderboard_projection`, `public_read`, `audit`) with the standard `facade.py`, `application/`, `domain/`, and `infrastructure/` structure plus minimal placeholder exports so later slices can extend them without reshaping paths.
5. Add an initial api boundary-check mechanism that documents/enforces facade-only cross-module imports, choosing a lightweight rule that can run locally now and in CI later.
6. Update affected docs/READMEs/local-dev notes so the api scaffold, command behavior, and boundary-check baseline match the implemented repository state.
7. Validate the scaffold with the narrowest honest checks available for TASK-2 (for example dependency install, app import/boot smoke path, and the selected boundary-check command), without expanding into TASK-8’s full api test harness scope.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Started implementation-planning pass after reviewing Backlog workflow overview/task-execution guidance plus architecture/module-boundary docs.

Draft plan prepared and internally reviewed. Pending user review before planSet. Material sequencing conflict noted: adding apps/api/pyproject.toml will make Makefile test-api stop failing fast even though docs/ops/local-dev.md and TASK-8 say api tests become runnable later.

User decision: keep current Makefile behavior, so TASK-2 may make make test-api stop failing fast before TASK-8 lands. Planning should preserve existing Makefile semantics and align docs later as part of implementation.

Implemented the api scaffold in /tmp/palio-task-2 with apps/api/pyproject.toml, src/palio/app composition-root wiring, shared db/support packages, and all documented module facades plus application/domain/infrastructure folders.

Added a lightweight api boundary checker at apps/api/src/palio/shared/module_boundaries.py and documented the local command `uv run python -m palio.shared.module_boundaries` so the same rule can move into CI later.

Validated the scaffold with `uv run pytest` and `uv run python -m palio.shared.module_boundaries` from apps/api; both passed after trimming an eager package import that initially caused a runpy warning.

User decision: collapse the later `apps/api` -> `apps/api` rename work into TASK-2 for commit/branch/PR purposes. TASK-2 now owns the canonical api app-root path change as part of the api scaffold outcome.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented TASK-2 in the dedicated worktree by scaffolding `apps/api/` as a minimal FastAPI project with explicit manual wiring and the documented modular-monolith package layout. The composition root now lives under `src/palio/app/` with a small app factory, placeholder admin/public/realtime surfaces, shared `db/` and `shared/` technical packages, and one public `facade.py` per api module so later slices can add behavior without moving paths.

Added the initial api architectural-boundary enforcement rule in `src/palio/shared/module_boundaries.py`. The checker scans code under `palio.modules` and fails when one module imports another module anywhere except that module’s `facade.py`, which gives us a local command we can wire into CI later.

Updated the api README, local-dev notes, top-level README, architecture Q&A, and testing strategy so the current scaffold state and command surface match reality. Validation run from `apps/api`: `uv run pytest` (3 passed) and `uv run python -m palio.shared.module_boundaries` (passed).

Folded the later api app-root rename into TASK-2: the canonical FastAPI app root is now `apps/api`, and the related Makefile/doc/task references were updated as part of the api scaffold deliverable.
<!-- SECTION:FINAL_SUMMARY:END -->
