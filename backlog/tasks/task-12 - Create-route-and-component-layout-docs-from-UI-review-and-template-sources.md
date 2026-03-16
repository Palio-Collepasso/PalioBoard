---
id: TASK-12
title: Create route and component layout docs from UI review and template sources
status: Done
assignee:
  - codex
created_date: '2026-03-15 16:50'
updated_date: '2026-03-15 16:57'
labels:
  - documentation
  - ui
dependencies: []
documentation:
  - docs/README.md
  - docs/engineering/documentation-impact-matrix.md
  - docs/ui/pages_review.md
  - docs/ui/palioboard_ui_template_extracted.md
  - docs/product/prd.md
  - docs/product/functional-requirements.md
  - docs/product/acceptance-scenarios.md
priority: medium
ordinal: 2000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create a new `docs/ui` documentation set that converts the route inventory in `docs/ui/pages_review.md` and the design/layout rules in `docs/ui/palioboard_ui_template_extracted.md` into implementation-facing markdown files. The output should include one markdown file per route-level page and, where reuse is justified, separate markdown files for shared components/layout patterns. The documentation should describe each page's purpose, information architecture, layout structure, states, shared patterns, and the details needed to turn the markdown into actual pages.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 `docs/ui` contains dedicated markdown layout specs for the `/admin`, `/public`, and `/maxi` application shells.
- [x] #2 Each layout spec describes the shell structure, navigation/chrome, responsive behavior, layout regions, shared content blocks, and state/pattern rules needed to build pages within that shell.
- [x] #3 Shared component documentation is split out only when it reduces duplication across the three shell specs, and each shell doc references it.
- [x] #4 The resulting docs stay aligned with PalioBoard domain constraints and avoid generic sports-platform patterns.
- [x] #5 A short `docs/ui/README.md` explains how the shell docs and any shared component docs fit together.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Documentation impact check
- Reviewed: `docs/README.md`, `docs/engineering/documentation-impact-matrix.md`, `docs/ui/pages_review.md`, `docs/ui/palioboard_ui_template_extracted.md`, `docs/product/prd.md`, `docs/product/functional-requirements.md`, `docs/product/acceptance-scenarios.md`.
- Must update in this task: `docs/ui/README.md`; dedicated layout specs for `/admin`, `/public`, and `/maxi`; shared pattern docs under `docs/ui/components/` only where reuse materially reduces duplication.
- Considered and no change needed: `docs/api/error-contract.md`, `docs/domain/business-rules.md`, `docs/testing/test-strategy.md`, `docs/testing/critical-e2e-flows.md`, `docs/testing/fixtures.md`, `docs/ops/local-dev.md`, `docs/ops/deploy.md`, `docs/ops/runbook.md`, because this task only documents UI shell/layout guidance and does not change product behavior, domain rules, tests, or operations.

Revised implementation plan
1. Create `docs/ui/README.md` that explains the narrowed scope and points implementers to the shell-level documentation instead of route-by-route specs.
2. Write three shell docs covering `/admin`, `/public`, and `/maxi`, each describing route family, shell structure, persistent chrome, grid/container rules, layout regions, core content patterns, responsive behavior, and state presentation.
3. Split out only the genuinely shared primitives needed by all three shells, such as status/banner semantics and common surface patterns, if doing so reduces repetition.
4. Cross-reference the shell docs so feature/page authors can derive concrete page layouts from the shell guidance without re-reading the original source markdown files.
5. Review the docs for consistency with PalioBoard constraints: fixed competition contexts, fixed rioni, operational-first admin UX, trust-oriented public UX, and distance-readable maxi-screen UX.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Narrowed scope after user feedback from route-by-route page docs to shell-level layout docs for `/admin`, `/public`, and `/maxi`.

Used `docs/ui/design_tokens.json` as the exact visual token source and `docs/ui/component_checklist.md` as the implementation completeness reference instead of rewriting those files.

Created `docs/ui/README.md`, `docs/ui/layouts/admin-shell.md`, `docs/ui/layouts/public-shell.md`, `docs/ui/layouts/maxi-shell.md`, and `docs/ui/components/shared-layout-primitives.md`.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Created a shell-level UI documentation set focused on the three persistent PalioBoard layout systems instead of route-by-route page specs. Added `docs/ui/README.md` to explain the scope and how to use the new docs, then added dedicated layout specifications for `/admin`, `/public`, and `/maxi` covering shell structure, persistent chrome, layout regions, responsive behavior, state presentation, and recommended component splits.

To keep the shell docs concise and reusable, added `docs/ui/components/shared-layout-primitives.md` for shared surface, card, badge, banner, and status-language rules. The new docs explicitly align to `docs/ui/design_tokens.json` for exact sizing/color/spacing values and use `docs/ui/component_checklist.md` as the implementation completeness map.

Tests: none run, because this task only adds documentation and does not change application code.
<!-- SECTION:FINAL_SUMMARY:END -->
