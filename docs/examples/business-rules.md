# Business Rules

## Purpose

Capture PalioBoard domain truth in a stable, implementation-independent way.

This document should answer questions such as:
- what is allowed or forbidden in the domain;
- what must happen when judges/admins act on games;
- what counts toward standings and what does not;
- which behaviors are invariants rather than UI details.

## How to use this document

- Each rule has a stable ID.
- Rules describe business behavior, not controller/service implementation details.
- Update related tests, API behavior, and ops docs when a rule changes.
- When two rules appear to conflict, the more specific rule wins until the broader rule is clarified.

## Rule index

| Rule ID | Title | Area | Status |
|---|---|---|---|
| `BR-001` | One active season with four teams and three competition contexts | season setup | active |
| `BR-002` | Game setup becomes immutable after official result data exists | season setup | active |
| `BR-003` | Ranking games require complete valid official placements to finish | results | active |
| `BR-004` | Pending admin review still counts; under examination does not | event operations | active |
| `BR-005` | Jolly is Palio-only and may be used once per team | results | active |
| `BR-006` | Live ranking draft is collaborative but never official truth | live games | active |
| `BR-007` | 1v1 match saves are official immediately, leaderboard waits for completion | tournaments | active |
| `BR-008` | Manual leaderboard adjustments are explicit authoritative inputs | leaderboard | active |
| `BR-009` | Public visibility is immediate for latest official result, even during review windows | public read | active |


---

## Rules by area

## Season setup

### `BR-001` — One active season with four teams and three competition contexts

- **Status:** `active`
- **Area:** `season setup`
- **Priority:** `critical`
- **Summary:** PalioBoard v1 models exactly one active season, exactly four teams, and exactly three competition contexts.

#### Rule statement

The system must manage exactly one active season in the database, exactly four teams for that season, and exactly these competition contexts: `palio`, `prepalio`, and `giocasport`.

#### Applies when

- season creation and initialization;
- game creation and competition assignment;
- standings and public-read filtering.

#### Preconditions

- the v1 system is used for a single event year;
- team setup happens before authoritative results exist.

#### Required behavior

- every game belongs to exactly one of the three supported competition contexts;
- Palio and Giocasport remain separate standing domains;
- Prepalio subgames feed a Prepalio aggregate ranking which then contributes to Palio standings.

#### Forbidden behavior

- adding a fifth team in v1;
- creating games outside the supported competition list.

#### Outcome

- the core domain stays small and predictable;
- all scoring and projection rules operate over a fixed team set.

#### Edge cases

- teams may be renamed before official results exist;
- team identity should remain stable once authoritative data exists.

#### Rationale

PalioBoard is optimized for a single annual event with a fixed structure, so the domain model should encode that constraint directly.

#### Enforcement notes

- **API impact:** setup APIs should reject unsupported competition values.
- **UI impact:** setup screens should not expose controls for extra teams or extra competition types.
- **Audit impact:** authoritative setup changes after official data should be blocked, not merely audited.
- **Test impact:** season setup integration tests should enforce fixed team/context constraints.

#### Related items

- **Related docs:** `docs/product/functional-requirements.md`, `docs/domain/er-schema.md`

### `BR-002` — Game setup becomes immutable after official result data exists

- **Status:** `active`
- **Area:** `season setup`
- **Priority:** `critical`
- **Summary:** Once any official result data exists for a game, all result-affecting setup becomes immutable in v1.

#### Rule statement

Once a game has any official result data, the game’s setup must not change.

#### Applies when

- editing a game definition;
- attempting to delete or reconfigure a game with official entries.

#### Preconditions

- at least one canonical official per-team entry exists for the game.

#### Required behavior

- editing of competition, format, configured fields, points table, and other result-affecting configuration is blocked;
- deletion of the game is blocked.

#### Forbidden behavior

- mutating a game definition after results exist;
- “fixing” historic setup by changing current configuration in place.

#### Outcome

- standings remain reproducible;
- audit history matches the meaning of the stored official results.

#### Edge cases

- pre-start housekeeping is still allowed while no official result data exists;
- live ranking draft state does not count as official result data by itself.

#### Rationale

Immutability prevents silent retroactive changes that would invalidate standings, audit, and public trust.

#### Enforcement notes

- **API impact:** setup mutation endpoints should return a domain error when official entries already exist.
- **UI impact:** admin setup actions should become read-only once the game has official data.
- **Audit impact:** blocked mutations should not rewrite authoritative history.
- **Test impact:** Postgres-backed integration tests should prove immutability after official entries exist.

#### Related items

- **Related rules:** `BR-006`, `BR-007`
- **Related docs:** `docs/api/error-contract.md`

## Results and scoring

### `BR-003` — Ranking games require complete valid official placements to finish

- **Status:** `active`
- **Area:** `results`
- **Priority:** `critical`
- **Summary:** A ranking game can only complete when all four teams have structurally valid placements and required fields.

#### Rule statement

A ranking game can move to `completed` only when all four teams have official placements, the placements are structurally valid, and required configured fields are filled.

#### Applies when

- completing a ranking game;
- moving a ranking game from `in_progress` to `under_examination` if materialization occurs on exit.

#### Preconditions

- the game format is `ranking`;
- live draft changes have been materialized or are about to be materialized.

#### Required behavior

- explicit ties such as `1,2,2,4` are allowed when structurally valid;
- invalid placement structures are rejected;
- required configured fields must be present.

#### Forbidden behavior

- completing with missing placements;
- deriving placements implicitly from other fields in v1.

#### Outcome

- official placements remain explicit and auditable;
- projection logic receives a canonical valid result surface.

#### Edge cases

- optional metric fields may remain empty;
- ranking draft state alone does not count in standings before completion.

#### Rationale

Standings correctness depends on explicit, complete, and valid official result structure.

#### Enforcement notes

- **API impact:** return `invalid_placement_structure` or `required_field_missing` as appropriate.
- **UI impact:** completion CTA should surface missing/invalid fields clearly.
- **Audit impact:** materialized authoritative changes on completion must be audited.
- **Test impact:** completion validation needs both unit coverage for placement rules and integration coverage for workflow behavior.

#### Related items

- **Related rules:** `BR-005`, `BR-006`
- **Related docs:** `docs/testing/critical-e2e-flows.md`

### `BR-005` — Jolly is Palio-only and may be used once per team

- **Status:** `active`
- **Area:** `results`
- **Priority:** `critical`
- **Summary:** Jolly can be applied only in Palio games and at most once per team across Palio games.

#### Rule statement

Jolly must only be allowed in Palio competition games, and each team can use Jolly at most once across all Palio games.

#### Applies when

- editing an official Palio result;
- completing a ranking Palio game;
- overriding official placements after a tournament if Jolly is relevant.

#### Preconditions

- the target game belongs to the Palio competition context.

#### Required behavior

- if Jolly is valid, the affected team’s Palio result has doubled points;
- the system provides a Jolly summary view.

#### Forbidden behavior

- using Jolly in Prepalio or Giocasport;
- using Jolly twice for the same team in Palio.

#### Outcome

- Palio standings reflect a single, traceable Jolly choice per team.

#### Edge cases

- changing a completed result may move Jolly usage and still requires audit/review;
- under-examination games remain visible but do not count regardless of Jolly.

#### Rationale

Jolly is a central Palio rule and must remain both strict and explainable.

#### Enforcement notes

- **API impact:** use `jolly_not_allowed` or `jolly_already_used`.
- **UI impact:** Jolly controls should only appear for Palio games.
- **Audit impact:** Jolly changes are authoritative and must be audited.
- **Test impact:** regression tests should cover first use, repeated use, and non-Palio rejection.

#### Related items

- **Related rules:** `BR-003`, `BR-004`
- **Related docs:** `docs/api/error-contract.md`

## Event operations

### `BR-004` — Pending admin review still counts; under examination does not

- **Status:** `active`
- **Area:** `event operations`
- **Priority:** `critical`
- **Summary:** `pending_admin_review` remains scoring-visible, while `under_examination` suspends the game from leaderboard calculations.

#### Rule statement

A game in `pending_admin_review` must still count in standings using the latest saved official result, while a game in `under_examination` must remain publicly visible but must not count in leaderboard calculations.

#### Applies when

- judges edit a completed result;
- admins resolve review state;
- a judge/admin marks or resolves under examination.

#### Preconditions

- the game already has an official result surface.

#### Required behavior

- judge edits to a completed game move it to `pending_admin_review`;
- latest official result remains visible and counting during `pending_admin_review`;
- latest official result remains visible but non-counting during `under_examination`.

#### Forbidden behavior

- treating `pending_admin_review` as a suspended scoring state;
- hiding an under-examination game entirely from public view.

#### Outcome

- the public sees the latest official truth quickly;
- standings reflect the correct distinction between review and suspension.

#### Edge cases

- admin resolution may confirm or effectively revert the latest result through a new authoritative write;
- moving from `under_examination` back to `completed` may keep the same official result or a corrected one.

#### Rationale

The event needs public transparency without freezing normal review flows, while still allowing true suspension for contested cases.

#### Enforcement notes

- **API impact:** transitions must be guarded by capability and current-state policy.
- **UI impact:** public/admin screens need distinct badges for counting vs non-counting visibility.
- **Audit impact:** all authoritative review and examination changes must be audited.
- **Test impact:** projection tests and E2E coverage must verify counting behavior by state.

#### Related items

- **Related rules:** `BR-009`
- **Related docs:** `docs/testing/critical-e2e-flows.md`

## Live games

### `BR-006` — Live ranking draft is collaborative but never official truth

- **Status:** `active`
- **Area:** `live games`
- **Priority:** `critical`
- **Summary:** Ranking live entry supports collaboration and recovery, but draft state never becomes official until materialized through game workflow.

#### Rule statement

Live ranking draft state may support collaborative editing and reconnect recovery, but it must never be treated as official result truth or as the direct source of standings.

#### Applies when

- a ranking game enters `in_progress`;
- editors acquire field leases and save draft values;
- the game leaves `in_progress`.

#### Preconditions

- the game format is `ranking`;
- the game is in `in_progress`.

#### Required behavior

- starting the game prefills live draft state from the current official result surface;
- concurrent edits use field-level exclusive editing semantics and version/conflict checks;
- leaving `in_progress` materializes changed draft values into official entries;
- current live draft is cleared best-effort after exit from `in_progress`.

#### Forbidden behavior

- updating standings from draft state;
- using persisted draft snapshots as official audited history.

#### Outcome

- judges can collaborate safely;
- official truth remains database-backed and auditable.

#### Edge cases

- persisted draft snapshots may survive restart for recovery purposes;
- stale draft cleanup failure does not invalidate the authoritative workflow when `live_cycle` protects against old drafts.

#### Rationale

This preserves correctness while still allowing practical live entry during the event.

#### Enforcement notes

- **API impact:** use `field_locked` and `version_conflict` for collaboration safety.
- **UI impact:** editors need clear conflict and lock feedback.
- **Audit impact:** draft-only churn is not audited as business history.
- **Test impact:** realtime integration tests are required for lease/conflict behavior.

#### Related items

- **Related rules:** `BR-003`
- **Related docs:** `docs/testing/test-strategy.md`, `docs/testing/fixtures.md`

## Tournaments

### `BR-007` — 1v1 match saves are official immediately, leaderboard waits for completion

- **Status:** `active`
- **Area:** `tournaments`
- **Priority:** `high`
- **Summary:** Tournament matches become official immediately, but leaderboard impact is deferred until the tournament game is completed.

#### Rule statement

Each saved 1v1 tournament match outcome must become official immediately and update bracket progression immediately, but leaderboard recalculation must wait until the tournament game is completed.

#### Applies when

- judges/admins save semifinal or final match outcomes;
- bracket progression is displayed during the tournament;
- the tournament game is completed.

#### Preconditions

- semifinal pairings were set before start;
- the game format is `tournament_1v1`.

#### Required behavior

- saved match outcomes materialize/update the canonical official per-team result surface;
- bracket progression becomes visible immediately;
- final ranking can be auto-derived and optionally overridden by authorized users.

#### Forbidden behavior

- routing tournament edits through the ranking live-draft subsystem in v1;
- recomputing the leaderboard on every individual match save.

#### Outcome

- tournament operations remain simple and official;
- standings change only when the whole tournament game is completed.

#### Edge cases

- automatic ranking derivation may be overridden by authorized admins;
- completed-result edits still follow the review/examination rules.

#### Rationale

Tournament progression needs immediate official bracket visibility without prematurely affecting standings.

#### Enforcement notes

- **API impact:** start should reject missing pairings; match-save APIs must persist official state directly.
- **UI impact:** bracket views can be live without implying leaderboard impact.
- **Audit impact:** each official match update must be auditable.
- **Test impact:** integration and E2E tests should cover progression and completion separately.

#### Related items

- **Related rules:** `BR-004`
- **Related docs:** `docs/testing/critical-e2e-flows.md`

## Leaderboard / public read

### `BR-008` — Manual leaderboard adjustments are explicit authoritative inputs

- **Status:** `active`
- **Area:** `leaderboard`
- **Priority:** `high`
- **Summary:** Manual standings adjustments are first-class authoritative inputs, not hidden exceptions.

#### Rule statement

Manual leaderboard adjustments must be stored explicitly with competition, team, signed delta, reason, timestamp, and author, and must affect standings immediately.

#### Applies when

- an admin creates or changes a manual adjustment;
- standings are recomputed.

#### Required behavior

- adjustments participate in official standings calculation;
- reason and author are retained.

#### Forbidden behavior

- editing standings tables directly as an opaque operational shortcut;
- silently applying manual corrections without traceable context.

#### Outcome

- standings remain explainable and auditable.

#### Enforcement notes

- **Audit impact:** creating or changing an adjustment must be audited.
- **Test impact:** projection tests should include adjustment scenarios.

#### Related items

- **Related docs:** `docs/testing/fixtures.md`

### `BR-009` — Public visibility is immediate for latest official result, even during review windows

- **Status:** `active`
- **Area:** `public read`
- **Priority:** `high`
- **Summary:** Public and maxi screens should show the latest official result promptly, including during appeal/review windows.

#### Rule statement

Official result changes must become visible to public/maxi readers immediately, even when the game is in `pending_admin_review`; however, `under_examination` games remain visible with their non-counting status.

#### Applies when

- a game completes;
- a completed result is edited;
- a game enters or leaves `under_examination`.

#### Required behavior

- public/maxi views show standings, results, notes, and status badges as soon as official data changes;
- public read models reflect the counting/non-counting distinction by state.

#### Forbidden behavior

- hiding latest official results until the review window closes;
- counting an under-examination game in leaderboard projections.

#### Outcome

- the public sees timely official information;
- scoring semantics remain correct.

#### Enforcement notes

- **UI impact:** public/maxi screens need explicit status messaging.
- **Test impact:** a critical E2E flow must verify public updates after completion and after review-state changes.

#### Related items

- **Related rules:** `BR-004`
- **Related docs:** `docs/testing/critical-e2e-flows.md`

## Known ambiguities / decisions needed

- Confirm whether admins may edit Palio team labels after season setup but before any official result exists.
- Confirm whether manual leaderboard adjustments can themselves enter a review flow, or remain immediate authoritative writes in v1.
