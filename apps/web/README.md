# Web

This directory is the canonical home for the Angular SPA and frontend test harness.

The current Angular 21 scaffold includes:
- one SPA and three lazy route shells: `admin`, `public`, and `maxi`
- `src/app/` boundaries for `core/`, `shell-*`, `features/`, and `shared/{api,ui,utils,types}`
- placeholder API service layers for `admin`, `public`, and `realtime`
- `npm run check-boundaries` import rules for shell/shared isolation

Current command surface:
- `npm run start` starts the Angular dev server on port `4200`
- `npm run build` builds the scaffolded SPA
- `npm run generate:api-types` regenerates TS declarations from `../../docs/api/openapi.yaml`
- `npm run typecheck` runs TypeScript-only validation
- `npm run check-boundaries` enforces the initial frontend import rules
- `npm test -- --watch=false` runs the Angular behavior-test harness through the `@angular/build:unit-test` builder with Vitest
- `npm run e2e` runs the Playwright shell smoke suite, reusing `PLAYWRIGHT_BASE_URL` when set and otherwise managing the local same-origin stack automatically
- `npm run e2e:install` installs the Playwright Chromium browser used by the smoke suite

Contract workflow baseline:
- generated API types live under `src/app/shared/api/generated/`
- committed generated frontend API artifacts include `src/app/shared/api/generated/openapi.d.ts` from `make api-contract`
- committed generated frontend API artifacts include `src/app/shared/api/generated/error-codes.generated.ts` from `make errors`
- generated API artifacts are derived from the committed API spec and error catalog; do not hand-edit them
- Angular services under `src/app/shared/api/` remain hand-written
- use repo-level `make errors`, `make api-contract`, and `make contracts` for the canonical contract workflow

The scaffold is intentionally thin: shells are reachable, shared code is generic, and feature state stays local until real product slices land.
