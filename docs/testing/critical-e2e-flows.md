# Critical E2E Flows


## Purpose

List the end-to-end flows that must remain healthy because they protect core business value or high-risk operations.

## How to Use

- Each flow has a stable ID.
- Keep steps user-visible and outcome-oriented.
- Link each flow to the fixtures and docs it depends on.
- Record whether the flow is required on every PR, on release, nightly, or manually.

## Current Coverage Note

The current critical set is intentionally limited to the same-origin shell smoke path because the repo does not yet expose stable browser-tested business workflows.

Future note:
- promote ranking completion, public update, tournament progression, post-completion review, and live-collaboration flows here as soon as those slices exist and their browser coverage is reliable enough to protect the release gate

## Flow Index

| Flow ID | Title | Priority | Cadence | Owner |
|---|---|---|---|---|
| `E2E-001` | Same-origin shell smoke | critical | per PR | web/app platform |

---

## Flow Definitions

Template for each critical E2E flow: `docs/templates/testing/e2e-flow.template.md`

> Next-pass guidance: keep this file small and limited to trust-critical browser flows. If live-collaboration coverage is added later, keep the browser version in the per-PR gate only if it proves stable in CI; otherwise prefer deterministic realtime integration coverage and move the heavier browser flow to nightly or release validation.

### `E2E-001` — Same-origin shell smoke

- **Status:** active
- **Priority:** critical
- **Cadence:** per PR
- **Owner:** web/app platform
- **Business value protected:** Proves the local same-origin stack still serves the SPA shells and proxy paths through Nginx.

#### Preconditions

- The local stack is reachable through `http://127.0.0.1:8080`.
- The Angular SPA has been built and is being served through the Nginx same-origin stack.
- No special user capability is required because the current smoke scope only verifies scaffold reachability.

#### Test data / fixtures

- `FX-002` — same-origin shell smoke routes
- built SPA assets from the current `apps/web` scaffold

#### Steps

1. Navigate to `/`.
2. Confirm the browser lands on the public shell.
3. Visit `/admin`, `/public`, and `/maxi`.

#### Expected result

- `/` resolves to the public shell.
- Each shell route renders its expected scaffold heading and placeholder-card count through Nginx.

#### Failure impact

- Browser smoke verification for the stack is no longer trustworthy.
- Reviewers lose the fastest user-visible signal that the same-origin deployment path still works.

#### Related business rules

- None yet. This flow protects infrastructure reachability rather than domain-rule behavior.

#### Related API / modules

- `infra/compose/docker-compose.yml`
- `infra/nginx/default.conf`
- `apps/web/e2e/shell-smoke.spec.ts`

#### Notes / edge cases

- This intentionally does not prove scoring, standings, or realtime conflict behavior yet.
- Broader browser flows should be added only when the corresponding product slice lands.

#### Automation status

- **Automated:** yes
- **Test location:** `apps/web/e2e/shell-smoke.spec.ts`
- **Manual fallback:** Run `make up`, browse `/`, `/admin`, `/public`, and `/maxi`, then verify scaffold headings render.

---

## Release-Blocking Flows

- `E2E-001` — Same-origin shell smoke

## Nightly / Extended Flows

> No nightly-only flows are defined yet. Add them when broader user journeys become automation-worthy.
