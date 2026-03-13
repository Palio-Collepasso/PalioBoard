---
id: TASK-1
title: Bootstrap the monorepo layout and top-level make workflow
status: Done
assignee:
  - '@codex'
created_date: '2026-03-12 01:37'
updated_date: '2026-03-12 16:19'
labels: []
milestone: m-0
dependencies: []
documentation:
  - docs/architecture/architecture.md
  - docs/qna/architecture/module boundaries.md
  - docs/qna/architecture/deployment and operations.md
parent_task_id: M-0
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create the initial repository skeleton for the documented monorepo and establish `make` as the stable top-level command surface for local development and CI.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Root layout matches the approved monorepo structure for `apps/api/`, `apps/web/`, `infra/`, `docs/`, `tools/`, and `.github/workflows/`.
- [x] #2 A top-level `Makefile` exposes the baseline developer entrypoints needed by later M1 tasks without hiding implementation details inside ad hoc scripts.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
## Research Summary
- Canonical architecture section 14.1 and TASK-1 acceptance criteria both describe a top-level layout rooted at `backend/`, `web/`, `infra/`, `docs/`, `tools/`, and `.github/workflows/`.
- `docs/qna/architecture/module boundaries.md` still says `apps/api` and `apps/web`, so the repository-shape documentation is inconsistent and must be reconciled as part of implementation.
- `README.md` already assumes a future `backend/` and `web/` layout plus a top-level `Makefile`, but those files/directories do not exist yet.
- `docs/ops/local-dev.md` is referenced by repo instructions but does not exist yet; TASK-10 appears to own the full local bootstrap guide, so TASK-1 should avoid overreaching beyond layout and the top-level command surface.

## Proposed Implementation Plan
1. Resolve the repo-layout inconsistency before scaffolding.
   - Treat `backend/` and `web/` as the likely canonical paths because they match TASK-1, the approved architecture document, milestone M0, and the current README.
   - Update conflicting architecture/Q&A text in the same change so later tasks do not scaffold against different paths.
2. Create the minimum monorepo skeleton needed by downstream M0 tasks.
   - Add `backend/`, `web/`, `infra/`, `tools/`, and `.github/workflows/` while preserving the existing `docs/` and `backlog/` content.
   - Keep the bootstrap intentionally thin: create only placeholder files/directories required to keep the structure visible in git and ready for TASK-2/TASK-10, without pre-implementing FastAPI, Angular, Docker Compose, or CI logic that belongs to later tasks.
3. Add a transparent top-level `Makefile`.
   - Define a small baseline command surface centered on discoverability (`help`) and stable entrypoints that later M0 tasks can fill in without renaming targets.
   - Prefer direct `uv`, `npm`, and Docker/Compose invocations inside obvious targets rather than hiding behavior in ad hoc scripts.
   - Keep any pre-scaffold targets explicit about not being ready yet if their dependent app/infrastructure files do not exist.
4. Update immediately stale documentation caused by the new baseline.
   - Refresh `README.md` so its repository tree and command guidance match the scaffold that actually exists after TASK-1.
   - Reconcile the repo-structure wording in the affected architecture/Q&A docs so future agents see one consistent layout.
   - Avoid writing the full local-development guide here unless the missing `docs/ops/local-dev.md` would otherwise leave the repo misleading; if needed, add only the minimum placeholder needed to remove contradiction and let TASK-10 own the final bootstrap doc.
5. Verify the bootstrap at the scope appropriate for TASK-1.
   - Confirm the repo tree matches the agreed top-level shape.
   - Run the baseline `make` entrypoint(s) such as `make help` to ensure the command surface is syntactically valid and self-describing.
   - Check that the resulting structure is ready for dependent tasks TASK-2 and TASK-3 without forcing them to rename or move paths.

## Scope Guards
- Do not scaffold backend application code; that belongs to TASK-2.
- Do not scaffold Angular shell code; that belongs to TASK-3.
- Do not add real Compose/Nginx wiring; that belongs to TASK-6.
- Do not add the full CI/bootstrap workflow documentation; that belongs to TASK-10.

## Risks / Decisions Needed Before Coding
- Repository-path conflict: `backend/` + `web/` versus `apps/api` + `apps/web`.
- Documentation ownership boundary: whether TASK-1 should create a minimal `docs/ops/local-dev.md` placeholder or simply remove/update references until TASK-10 lands.

## Planned Validation
- Repository tree inspection.
- `make help` (and any other bootstrap-safe target added in this task).
- Manual review that docs and task dependencies point to the same top-level paths.

User-directed revision after initial completion: switch the canonical app paths from top-level `backend/` and `web/` to `apps/api/` and `apps/web/`. Update the scaffold, `Makefile`, and every affected repo/documentation reference in one change so M0 tasks build against the new layout consistently.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Researched TASK-1 against the architecture baseline, milestone M0, sibling tasks TASK-2/TASK-3/TASK-6/TASK-10, README, and testing guidance. Found a material docs conflict on repo layout (`backend`/`web` vs `apps/api`/`apps/web`) plus a missing `docs/ops/local-dev.md` reference to resolve before implementation.

Implemented the canonical top-level layout with tracked placeholders for `backend/`, `web/`, `infra/`, `tools/`, and `.github/workflows`, plus a minimal `docs/ops/local-dev.md` so repo guidance no longer points to a missing file.

Added a top-level `Makefile` that exposes the stable command names already referenced by the repo (`help`, `up`, `down`, `backend-dev`, `web-dev`, `test`, `test-backend`, `test-web`, `test-e2e`) and makes missing downstream scaffolds fail fast with task-specific guidance instead of hiding behavior in scripts.

Reconciled the repository-shape documentation to the canonical `backend/` + `web/` layout in README and architecture Q&A documents. Verification run: `make help`, `make up` (expected fast failure because TASK-6 has not created `infra/compose/docker-compose.yml` yet), `git diff --check`.

User changed the repo-layout decision after the first TASK-1 pass. Reopening the task to migrate the canonical scaffold and documentation from `backend`/`web` to `apps/api`/`apps/web` rather than carrying two competing layouts.

Migrated the canonical scaffold from top-level `backend/` and `web/` into `apps/api/` and `apps/web/` after the user changed the repo-layout decision. Updated the root `Makefile`, README, architecture docs, milestone docs, and local-dev note in the same pass so downstream tasks see one consistent app-root convention.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented TASK-1 with the user-directed monorepo layout rooted under `apps/`.

What changed:
- Moved the runnable app placeholders from top-level `backend/` and `web/` into `apps/api/` and `apps/web/`.
- Added `apps/README.md` so the monorepo now makes the application grouping explicit at the top level.
- Updated the root `Makefile` so its stable command surface still works, but now points to `apps/api` and `apps/web` as the canonical app roots.
- Kept the fail-fast behavior for commands whose downstream task has not landed yet, so the command surface remains stable without pretending the app scaffolds already exist.
- Updated `README.md`, `docs/ops/local-dev.md`, `docs/architecture/architecture.md`, `docs/qna/architecture/module boundaries.md`, `docs/_raw/architecture qna.md`, and `docs/milestones.md` to use the same `apps/api` and `apps/web` convention.

Why:
- The initial TASK-1 implementation used `backend/` and `web/` because that matched part of the documentation, but the user then chose the `apps/` layout instead.
- Switching everything in one pass avoids leaving M0 tasks split across two incompatible path conventions.

Verification:
- `make help`
- `make up` (expected to fail fast until TASK-6 adds `infra/compose/docker-compose.yml`)
- `git diff --check`

Follow-up context:
- TASK-2 should now scaffold the FastAPI app under `apps/api/`.
- TASK-3 should now scaffold the Angular app under `apps/web/`.
<!-- SECTION:FINAL_SUMMARY:END -->
