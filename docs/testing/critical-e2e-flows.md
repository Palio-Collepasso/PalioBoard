# Critical E2E Flows

## Purpose
List the small automated browser flow set that protects the highest-risk user-visible behavior.

## Document boundary
This file owns **the browser-level shortlist only**.
It does not replace `docs/product/acceptance-scenarios.md` or `docs/testing/test-strategy.md`.

## Promotion rule
A flow belongs here only when all are true:
- it is user-visible and cross-layer
- unit/integration tests alone are not enough protection
- breaking it would block a release or undermine trust
- the flow has a stable spec path and clear owner

## Flow index
| Flow ID | Flow | Owner | Playwright spec | Promotion source |
|---|---|---|---|---|
| `E2E-001` | Same-origin shell smoke | web/app owner | `apps/web/e2e/smoke/same-origin-shell.spec.ts` | foundation smoke until broader flows are promoted |

## Flow definitions
### `E2E-001` — Same-origin shell smoke
- **Owner:** web/app owner
- **Playwright spec:** `apps/web/e2e/smoke/same-origin-shell.spec.ts`
- **Related acceptance source:** foundation smoke / shell reachability gate
- **Related fixtures:** `FX-002`
- **Run cadence:** every PR touching shell routing, proxy wiring, or app bootstrapping; also on release verification

**Preconditions**
- same-origin local stack is up
- required env vars are present

**Steps**
1. open the shell root through the same-origin route
2. confirm the shell loads without fatal startup error
3. confirm the shell can reach the expected health-backed paths

**Expected result**
- the browser can load the shell through the same-origin path
- proxy routing does not block the app bootstrap

**Failure impact**
- release-blocking for shell/proxy changes

## Future promotion candidates
Promote a new flow into this file only after it has:
- a stable acceptance scenario
- stable fixture/setup ownership
- a clear Playwright spec path
- evidence that it is release-critical rather than merely useful
