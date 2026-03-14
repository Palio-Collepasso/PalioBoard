# Web

This directory is the canonical home for the Angular SPA and frontend test harness.

TASK-3 establishes the initial Angular 21 scaffold for M0 with:
- one SPA and three lazy route shells: `admin`, `public`, and `maxi`
- `src/app/` boundaries for `core/`, `shell-*`, `features/`, and `shared/{api,ui,utils,types}`
- placeholder API service layers for `admin`, `public`, and `realtime`
- `npm run check-boundaries` import rules for shell/shared isolation

Current command surface:
- `npm run start` starts the Angular dev server on port `4200`
- `npm run build` builds the scaffolded SPA
- `npm run typecheck` runs TypeScript-only validation
- `npm run check-boundaries` enforces the initial frontend import rules

Still reserved for later M0 tasks:
- frontend unit/integration harness wiring in TASK-9
- Playwright smoke coverage in TASK-9

The scaffold is intentionally thin: shells are reachable, shared code is generic, and feature state stays local until real product slices land.
