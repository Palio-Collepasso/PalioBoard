# UI Layout Docs

This folder now provides shell-level layout guidance plus route-level page specs built on top of those shells.

## Source documents

- `docs/ui/design_tokens.json`
- `docs/ui/component_checklist.md`
- `docs/product/prd.md`
- `docs/product/functional-requirements.md`
- `docs/product/acceptance-scenarios.md`

## Outputs

- `docs/ui/layouts/admin-shell.md`
- `docs/ui/layouts/public-shell.md`
- `docs/ui/layouts/maxi-shell.md`
- `docs/ui/components/shared-layout-primitives.md`
- `docs/ui/pages/admin/*.md`
- `docs/ui/pages/public/*.md`
- `docs/ui/pages/maxi/*.md`

## How to use these docs

1. Start from the shell that matches the route family:
   - `/admin/*` -> `layouts/admin-shell.md`
   - `/`, `/competition/*`, `/games/*` -> `layouts/public-shell.md`
   - `/maxi/*` -> `layouts/maxi-shell.md`
2. Pull sizing, spacing, color, and typography values from `design_tokens.json`.
3. Apply the shared card, badge, banner, and surface rules from `components/shared-layout-primitives.md`.
4. Use `component_checklist.md` as the implementation completeness list for shells, navigation, primitives, and states.
5. Use `docs/ui/pages/` when you need route-level layout guidance on top of the shell docs.

## Route docs

### Admin and auth

- `docs/ui/pages/admin/login.md`
- `docs/ui/pages/admin/competitions-hub.md`
- `docs/ui/pages/admin/competition-detail.md`
- `docs/ui/pages/admin/season-setup.md`
- `docs/ui/pages/admin/game-editor.md`
- `docs/ui/pages/admin/game-workbench.md`
- `docs/ui/pages/admin/reviews-queue.md`
- `docs/ui/pages/admin/review-detail.md`
- `docs/ui/pages/admin/audit-log.md`
- `docs/ui/pages/admin/user-management.md`

### Public

- `docs/ui/pages/public/home.md`
- `docs/ui/pages/public/competition-detail.md`
- `docs/ui/pages/public/game-detail.md`

### Maxi

- `docs/ui/pages/maxi/competition-screen.md`

## Scope note

These docs intentionally start from the three persistent layout systems that everything else sits on:

- the operations-first admin shell
- the trust-oriented public shell
- the distance-readable maxi-screen shell

The route docs layer page-specific blocks and behaviors on top of those shells without redefining the whole structure each time.
