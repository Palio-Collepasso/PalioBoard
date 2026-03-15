---
id: TASK-12.1
title: Expand UI shell docs into route-level page layout specifications
status: Done
assignee:
  - codex
created_date: '2026-03-15 17:01'
updated_date: '2026-03-15 17:04'
labels:
  - documentation
  - ui
dependencies: []
documentation:
  - docs/README.md
  - docs/engineering/documentation-impact-matrix.md
  - docs/ui/README.md
  - docs/ui/layouts/admin-shell.md
  - docs/ui/layouts/public-shell.md
  - docs/ui/layouts/maxi-shell.md
  - docs/ui/components/shared-layout-primitives.md
  - docs/ui/pages_review.md
  - docs/ui/design_tokens.json
  - docs/ui/component_checklist.md
  - docs/product/prd.md
  - docs/product/functional-requirements.md
  - docs/product/acceptance-scenarios.md
parent_task_id: TASK-12
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Build on the new shell documentation for `/admin`, `/public`, and `/maxi` by creating route-level page layout docs under `docs/ui/pages/`. The output should cover the minimum route inventory defined in `docs/ui/pages_review.md`, using the shell docs, design tokens, and shared primitives as the foundation. Each page doc should explain the page purpose, route, layout regions, key blocks, actions, states, and any shell-specific adaptations needed to implement the page cleanly.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 `docs/ui/pages` contains route-level page layout docs for the approved PalioBoard route inventory.
- [x] #2 Each page doc references the relevant shell doc and describes route purpose, header, layout regions, main content blocks, actions, state presentation, and responsive behavior.
- [x] #3 Shared components are only split into separate docs when they remove meaningful duplication across multiple pages.
- [x] #4 The page docs stay consistent with the admin/public/maxi shell rules, the design tokens, and the PalioBoard domain constraints.
- [x] #5 `docs/ui/README.md` is updated if needed so the shell docs and page docs are navigable together.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Documentation impact check
- Reviewed: `docs/README.md`, `docs/engineering/documentation-impact-matrix.md`, `docs/ui/README.md`, `docs/ui/layouts/admin-shell.md`, `docs/ui/layouts/public-shell.md`, `docs/ui/layouts/maxi-shell.md`, `docs/ui/components/shared-layout-primitives.md`, `docs/ui/pages_review.md`, `docs/ui/design_tokens.json`, `docs/ui/component_checklist.md`, `docs/product/prd.md`, `docs/product/functional-requirements.md`, `docs/product/acceptance-scenarios.md`.
- Must update in this task: `docs/ui/README.md`; route-level page docs under `docs/ui/pages/`; shared component docs only if repeated page structure shows a real need.
- Considered and no change needed: `docs/api/error-contract.md`, `docs/domain/business-rules.md`, `docs/testing/test-strategy.md`, `docs/testing/critical-e2e-flows.md`, `docs/testing/fixtures.md`, `docs/ops/local-dev.md`, `docs/ops/deploy.md`, `docs/ops/runbook.md`, because this follow-up adds page-layout documentation only and does not change application behavior, domain rules, tests, or operations.

Implementation plan
1. Create `docs/ui/pages/` grouped by route family and write one markdown file per approved route from the minimum IA.
2. In each page doc, reference the relevant shell doc and document purpose, route, header, layout regions, main content blocks, state handling, primary actions, and responsive behavior.
3. Reuse the existing shell docs and shared primitives as the default foundation so page docs stay narrow and do not duplicate shell rules.
4. Split out additional shared component docs only if repeated page structures show meaningful duplication beyond the current shell/primitives docs.
5. Update `docs/ui/README.md` so the shell docs, page docs, tokens, and checklist are discoverable together, then review the route docs against PalioBoard constraints.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Created 14 route-level page docs under `docs/ui/pages/`, matching the approved route inventory: 10 admin/auth, 3 public, and 1 maxi.

Kept shared structure in the existing shell docs and avoided creating extra shared component docs because the current shell and shared-primitives docs already removed the meaningful duplication.

Updated `docs/ui/README.md` so shell docs, page docs, design tokens, and the component checklist are navigable together.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Expanded the shell-level UI documentation into route-level page layout specs under `docs/ui/pages/`. Added 14 implementation-facing page docs that cover the approved route inventory: login, the key admin working pages, the three public pages, and the maxi-screen route. Each page doc references the relevant shell and captures route purpose, unique layout regions, primary blocks, actions, state handling, and responsive behavior.

Kept the shared structure in the existing shell docs and `docs/ui/components/shared-layout-primitives.md` rather than creating unnecessary extra component docs. Updated `docs/ui/README.md` so the shell docs, route docs, token file, and component checklist can be used together as the main UI documentation set.

Tests: none run, because this task only adds and updates documentation.
<!-- SECTION:FINAL_SUMMARY:END -->
