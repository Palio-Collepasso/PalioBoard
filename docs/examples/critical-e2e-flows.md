# Critical E2E Flows

## Purpose

List the end-to-end flows that are release-critical for PalioBoard v1.

These flows protect trust-critical behavior, not general feature coverage. They should remain small, stable, and high-value.

## How to use

- Each flow has a stable ID.
- Keep steps user-visible and outcome-oriented.
- Link flows to fixtures and business rules.
- Prefer a smaller reliable set over a large flaky one.

## Flow index

| Flow ID | Title | Priority | Cadence | Owner |
|---|---|---|---|---|
| `E2E-001` | Complete a ranking game | critical | per PR | api + web |
| `E2E-002` | Public standings/results update after ranking completion | critical | per PR | api + web |
| `E2E-003` | Progress and complete a 1v1 tournament | critical | per PR | api + web |
| `E2E-004` | Edit completed result and resolve admin review | critical | per PR | api + web |
| `E2E-005` | Concurrent live ranking updates with field lock behavior | critical | per PR or nightly, depending on stability | api + web |

---

## Active flows

### `E2E-001` — Complete a ranking game

- **Status:** `active`
- **Priority:** `critical`
- **Cadence:** `per PR`
- **Owner:** `api + web`
- **Business value protected:** Judges must be able to complete a normal ranking game and produce authoritative, auditable, standings-affecting results.

#### Preconditions

- use a season fixture with four teams and a ranking-format game in `draft`;
- log in as a user with capability to start and complete games;
- configured required fields are known.

#### Steps

1. Open the admin game page for a draft ranking game.
2. Start the game.
3. Enter placements for all four teams and fill required fields.
4. Optionally set a valid Palio Jolly when the fixture is a Palio game.
5. Complete the game.

#### Expected result

- the game moves to `completed`;
- official results are visible on the admin side;
- the leaderboard updates to include the game;
- audit evidence exists for the authoritative changes.

#### Failure impact

- judges cannot publish results safely;
- standings and public trust are immediately at risk.

#### Related business rules

- `BR-003`
- `BR-005`
- `BR-006`

#### Test data / fixtures

- `FX-001`
- `FX-002`

#### Automation status

- **Automated:** `yes`
- **Test location:** `<replace with Playwright path>`
- **Manual fallback:** complete a known ranking game in a seeded local environment and verify state, standings, and audit.

### `E2E-002` — Public standings/results update after ranking completion

- **Status:** `active`
- **Priority:** `critical`
- **Cadence:** `per PR`
- **Owner:** `api + web`
- **Business value protected:** Official changes must become visible to the public/maxi surfaces immediately after authoritative save.

#### Preconditions

- start from a ranking game that can be completed quickly;
- public and admin shells are both available;
- initial public standings snapshot is visible.

#### Steps

1. Open the public standings/results view.
2. In a separate admin session, complete a ranking game.
3. Wait for the expected refresh or realtime update path.
4. Re-open or refresh if the flow intentionally uses initial HTTP + realtime updates.

#### Expected result

- public results show the newly completed official result;
- public standings reflect the new counting state;
- status badges are correct for the game state.

#### Failure impact

- the event audience sees stale or misleading official information;
- public trust degrades quickly.

#### Related business rules

- `BR-004`
- `BR-009`

#### Test data / fixtures

- `FX-001`
- `FX-002`

#### Automation status

- **Automated:** `yes`
- **Test location:** `<replace with Playwright path>`
- **Manual fallback:** complete a ranking game and verify public page refresh within the expected path.

### `E2E-003` — Progress and complete a 1v1 tournament

- **Status:** `active`
- **Priority:** `critical`
- **Cadence:** `per PR`
- **Owner:** `api + web`
- **Business value protected:** Tournament progression and final official ranking must remain trustworthy.

#### Preconditions

- use a 1v1 tournament game fixture with semifinal pairings configured;
- log in as a user with capability to manage pairings and enter results.

#### Steps

1. Open a tournament game.
2. Verify or set semifinal pairings.
3. Start the game if required by the UI/workflow.
4. Save semifinal match winners.
5. Save third-place and final winners.
6. Complete the tournament game.

#### Expected result

- bracket progression updates after each saved match;
- canonical official per-team result surface is materialized;
- final official ranking is derivable and visible;
- leaderboard changes only when the whole game is completed.

#### Failure impact

- bracket logic becomes untrustworthy;
- official rankings and standings can diverge.

#### Related business rules

- `BR-007`

#### Test data / fixtures

- `FX-001`
- `FX-005`

#### Automation status

- **Automated:** `yes`
- **Test location:** `<replace with Playwright path>`
- **Manual fallback:** run a four-team tournament end to end and verify bracket plus final standings effect.

### `E2E-004` — Edit completed result and resolve admin review

- **Status:** `active`
- **Priority:** `critical`
- **Cadence:** `per PR`
- **Owner:** `api + web`
- **Business value protected:** Post-completion corrections must preserve latest official truth, review state semantics, and auditability.

#### Preconditions

- use a fixture with a completed game already counting in standings;
- have one judge-capable user and one admin-capable user.

#### Steps

1. Open a completed game as a judge.
2. Change an official result value and save.
3. Observe the game move to `pending_admin_review`.
4. Verify the latest result still counts publicly/admin-side.
5. Open the review flow as an admin.
6. Resolve the review, confirming or replacing the latest result.

#### Expected result

- judge edit writes a new authoritative result;
- the game enters `pending_admin_review`;
- the latest result still counts before resolution;
- admin resolution creates a new authoritative outcome and preserves traceability.

#### Failure impact

- correction flows become dangerous or opaque;
- scoring semantics for review state can be wrong.

#### Related business rules

- `BR-004`
- `BR-009`

#### Test data / fixtures

- `FX-001`
- `FX-004`

#### Automation status

- **Automated:** `yes`
- **Test location:** `<replace with Playwright path>`
- **Manual fallback:** modify a completed result locally and verify review-state counting plus audit evidence.

### `E2E-005` — Concurrent live ranking updates with field lock behavior

- **Status:** `active`
- **Priority:** `critical`
- **Cadence:** `per PR or nightly, depending on stability`
- **Owner:** `api + web`
- **Business value protected:** Multiple judges must not silently overwrite each other during live ranking entry.

#### Preconditions

- use a ranking game already in `in_progress` with live collaboration enabled;
- open two authenticated admin sessions with proper capabilities.

#### Steps

1. Session A begins editing a team/field and acquires a lease.
2. Session B attempts to edit the same team/field.
3. Session B observes the lock/conflict response.
4. Session A saves a change, bumping the revision.
5. Session B attempts a stale save.
6. Session B refreshes/reloads the latest state and retries correctly.

#### Expected result

- Session B receives a clear lock or version conflict response;
- no silent overwrite occurs;
- the UI can recover to the latest server state;
- authoritative completion still uses the final intended result only once.

#### Failure impact

- judges can lose work or publish incorrect results without noticing;
- trust in live operation drops sharply.

#### Related business rules

- `BR-006`

#### Test data / fixtures

- `FX-001`
- `FX-003`

#### Automation status

- **Automated:** `yes` or `partial`, depending on tooling maturity
- **Test location:** `<replace with Playwright path or mixed test path>`
- **Manual fallback:** reproduce with two browser sessions and verify lock/recovery behavior.

## Release-blocking flows

- `E2E-001` — Complete a ranking game
- `E2E-002` — Public standings/results update after ranking completion
- `E2E-003` — Progress and complete a 1v1 tournament
- `E2E-004` — Edit completed result and resolve admin review
- `E2E-005` — Concurrent live ranking updates with field lock behavior
