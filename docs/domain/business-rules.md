# Business Rules

## Purpose

Capture the domain rules that define expected system behavior.

## How to Read This Document

- Each rule has a stable ID.
- Rules describe domain truth, not implementation details.
- If multiple rules apply, stricter or more specific rules win over generic ones.
- If a rule changes, update related tests, API behavior, and operational docs as needed.

## Rule Index

| Rule ID | Title | Area | Status |
|---|---|---|---|
| `BR-001` | Fixed season, team, and competition scope | season setup | active |
| `BR-002` | Game configuration becomes immutable after official result data exists | season setup | active |
| `BR-003` | Ranking completion requires complete and structurally valid official data | results | active |
| `BR-004` | Jolly is Palio-only and single-use per team | results | active |
| `BR-005` | Pending admin review still counts using the latest official result | leaderboard | active |
| `BR-006` | Under examination remains visible but does not count | public read | active |
| `BR-007` | Live ranking draft is provisional and never official truth | live games | active |
| `BR-008` | Tournament matches are official immediately but leaderboard impact waits for completion | tournaments | active |

---

## Rules by Area

Template for each business rule entry: `docs/templates/domain/business-rule.template.md`

## Season Setup

### `BR-001` — Fixed season, team, and competition scope

- **Status:** `active`
- **Area:** `season setup`
- **Priority:** `critical`
- **Summary:** v1 operates on exactly one active season per database, exactly four teams, and exactly three competition contexts.

#### Rule statement

`The system must model exactly one active season per database, exactly four teams for that season, and exactly three competition contexts: palio, prepalio, and giocasport.`

#### Applies when

- creating or editing season setup
- configuring teams or competitions
- validating game ownership and competition type

#### Preconditions

- the system is operating in v1 scope
- the season has not expanded beyond the approved fixed-team model

#### Required behavior

- keep one active season in the database
- keep exactly four teams in the season
- allow games to belong only to `palio`, `prepalio`, or `giocasport`

#### Forbidden behavior

- adding extra competition contexts in v1
- supporting variable team counts per season
- treating the database as a multi-season store in v1

#### Inputs / factors

- season setup data
- team records
- competition type

#### Outcome

- all downstream standings and workflow logic operate on a fixed, stable competitive scope
- the UI and API can assume the four-team model without dynamic branching

#### Edge cases

- default team names can still be edited before official result data exists
- the fixed scope applies even if no games have been configured yet

#### Rationale

`The product is intentionally optimized for one yearly event with four fixed teams and three known competition contexts, so the domain model should encode that constraint directly.`

#### Examples

- **Valid example:** a season contains exactly four teams and one `prepalio` competition.
- **Invalid example:** a fifth team is added or a new ad hoc competition type is introduced.

#### Enforcement notes

- **API impact:** setup endpoints must reject scope-breaking mutations.
- **UI impact:** season setup screens should assume a fixed four-team model.
- **Audit impact:** changes to the fixed setup should still be traceable when allowed.
- **Test impact:** setup validation and seeded-season assumptions must be covered directly.

#### Related items

- **Related rules:** `BR-002`
- **Related endpoints:** none yet
- **Related docs:** `docs/product/functional-requirements.md`, `docs/product/prd.md`, `docs/architecture/architecture.md`, `docs/domain/er-schema.md`
- **Related ADRs:** none

### `BR-002` — Game configuration becomes immutable after official result data exists

- **Status:** `active`
- **Area:** `season setup`
- **Priority:** `critical`
- **Summary:** once a game has any official result data, its result-affecting setup and relationships become immutable in v1.

#### Rule statement

`Once a game has any official result data, the system must treat the game definition and all result-affecting relationships as immutable, and the game must no longer be deletable.`

#### Applies when

- editing a configured game
- editing configured game fields or points tables
- attempting to delete a game after official data exists

#### Preconditions

- at least one piece of official result data exists for the game

#### Required behavior

- block edits to competition type, game format, configured fields, points table, and other result-affecting configuration
- block deletion of the game
- keep the existing official result data consistent with its original setup

#### Forbidden behavior

- mutating `game_fields` after official result data exists
- mutating points mapping after official result data exists
- deleting a game with official result data

#### Inputs / factors

- existence of official `game_entries`
- configured fields and points table
- game relationships and metadata

#### Outcome

- historical official results remain interpretable against the setup that produced them
- standings and audit reconstruction stay stable

#### Edge cases

- immutability starts with any official result data, not only with full completion
- technical live-cycle changes do not override setup immutability

#### Rationale

`Allowing result-affecting setup changes after official data exists would make standings, audit history, and corrections ambiguous.`

#### Examples

- **Valid example:** an admin edits game fields before any official result data exists.
- **Invalid example:** an admin changes the points table after official placements were already saved.

#### Enforcement notes

- **API impact:** mutating setup endpoints must reject these writes once official data exists.
- **UI impact:** setup controls should become read-only once official data exists.
- **Audit impact:** attempted post-official setup changes should be traceable if surfaced administratively.
- **Test impact:** immutability checks need direct coverage in workflow tests.

#### Related items

- **Related rules:** `BR-001`, `BR-003`, `BR-008`
- **Related endpoints:** none yet
- **Related docs:** `docs/product/functional-requirements.md`, `docs/product/prd.md`, `docs/architecture/architecture.md`, `docs/domain/er-schema.md`
- **Related ADRs:** `ADR-0004`

## Event Operations

> No additional stable event-operations rules have been promoted yet beyond the lifecycle and truth rules captured below.

## Results

### `BR-003` — Ranking completion requires complete and structurally valid official data

- **Status:** `active`
- **Area:** `results`
- **Priority:** `critical`
- **Summary:** a ranking game can complete only when all four official placements are present, structurally valid, and all enabled required fields are filled.

#### Rule statement

`The system must block ranking-game completion unless all four teams have placements, the placements are structurally valid, and all enabled required fields are filled.`

#### Applies when

- a ranking game is being completed
- validation runs before leaderboard recomputation

#### Preconditions

- the game format is `ranking`
- the game is leaving `in_progress`

#### Required behavior

- require placements for all four teams
- accept explicit valid ties such as `1,2,2,4`
- require enabled required fields before completion
- trigger leaderboard recomputation only from a valid completed state

#### Forbidden behavior

- completing a ranking game with missing placements
- completing a ranking game with structurally invalid placements
- completing a ranking game while required fields are still empty

#### Inputs / factors

- official placements
- required configured fields
- game completion action

#### Outcome

- only valid official ranking data can become standings input
- tie handling stays explicit and auditable

#### Edge cases

- ties are allowed only when expressed as a structurally valid placement sequence
- partial in-progress data must not bypass completion validation

#### Rationale

`Completion is the boundary where provisional entry becomes authoritative standings input, so the data must be complete and structurally valid at that moment.`

#### Examples

- **Valid example:** placements `1,2,2,4` with all required fields filled.
- **Invalid example:** placements `1,2,2,3` or a missing placement for one team.

#### Enforcement notes

- **API impact:** completion workflows must reject invalid ranking payloads.
- **UI impact:** completion screens must show why completion is blocked.
- **Audit impact:** only successful official completion should enter the authoritative audit trail.
- **Test impact:** validation rules for completion and explicit ties need direct coverage.

#### Related items

- **Related rules:** `BR-002`, `BR-004`, `BR-007`
- **Related endpoints:** none yet
- **Related docs:** `docs/product/functional-requirements.md`, `docs/product/prd.md`, `docs/architecture/architecture.md`
- **Related ADRs:** `ADR-0004`

### `BR-004` — Jolly is Palio-only and single-use per team

- **Status:** `active`
- **Area:** `results`
- **Priority:** `critical`
- **Summary:** Jolly can be used only in Palio, at most once per team across Palio games, and never in Prepalio or Giocasport.

#### Rule statement

`The system must allow Jolly only for Palio games, reject any reuse by the same team across Palio games, and never allow Jolly in Prepalio or Giocasport.`

#### Applies when

- recording official Jolly usage
- computing points for a Palio result
- validating result entry for non-Palio competitions

#### Preconditions

- the game is receiving official result data
- a team attempts to mark Jolly usage

#### Required behavior

- allow per-team Jolly selection only in Palio
- reject Jolly if the team already used it in another Palio game
- double the points for the affected Palio result
- expose a Jolly summary view

#### Forbidden behavior

- accepting Jolly in Prepalio
- accepting Jolly in Giocasport
- silently accepting a second Palio Jolly for the same team

#### Inputs / factors

- competition type
- team identity
- prior Jolly usage history

#### Outcome

- Jolly remains a scarce, competition-specific scoring modifier
- standings calculations apply Jolly consistently and traceably

#### Edge cases

- Jolly must be considered part of the official per-team result, not a later adjustment
- Prepalio and Giocasport restrictions apply even if the UI exposes the same entry surface

#### Rationale

`Jolly is a Palio-specific rule with strong standings impact, so misuse or reuse would directly damage trust in the leaderboard.`

#### Examples

- **Valid example:** a team uses Jolly in one Palio game and the points are doubled there.
- **Invalid example:** the same team tries to use Jolly again in another Palio game or in Prepalio.

#### Enforcement notes

- **API impact:** result-entry workflows must reject invalid Jolly usage.
- **UI impact:** result-entry screens should disable or explain forbidden Jolly choices.
- **Audit impact:** Jolly changes must be traceable as official result changes.
- **Test impact:** single-use and competition-scope validation need direct coverage.

#### Related items

- **Related rules:** `BR-003`, `BR-005`
- **Related endpoints:** none yet
- **Related docs:** `docs/product/functional-requirements.md`, `docs/product/prd.md`, `docs/architecture/architecture.md`
- **Related ADRs:** `ADR-0004`

## Tournaments

### `BR-008` — Tournament matches are official immediately but leaderboard impact waits for completion

- **Status:** `active`
- **Area:** `tournaments`
- **Priority:** `high`
- **Summary:** each saved 1v1 match outcome becomes official immediately and updates bracket progression, but leaderboard impact is deferred until the tournament game is completed.

#### Rule statement

`In v1, each saved 1v1 match outcome must become official immediately and update canonical official entries and bracket progression, but leaderboard recomputation must wait until the tournament/game reaches completed.`

#### Applies when

- saving a 1v1 tournament match result
- deriving or overriding the final ranking
- deciding whether the leaderboard should change

#### Preconditions

- the game format is `tournament_1v1`
- a match winner is being saved

#### Required behavior

- treat each saved match outcome as official immediately
- expose bracket progression immediately
- materialize the official per-team consequences into canonical official entries immediately
- expose the resulting final ranking as soon as it is derivable
- delay leaderboard recomputation until the full tournament/game is completed

#### Forbidden behavior

- routing 1v1 through the ranking live-draft subsystem
- updating the leaderboard from partial bracket progress

#### Inputs / factors

- saved match winners
- semifinal pairings
- tournament completion state

#### Outcome

- bracket state stays operationally current without prematurely affecting the leaderboard
- final tournament standings remain derived from official match outcomes

#### Edge cases

- admins may override the final official placements when the derived ranking must be corrected
- partial tournament progress can be official without yet affecting standings

#### Rationale

`Tournament progression must be visible and official as the bracket evolves, but leaderboard impact belongs to whole-game completion rather than partial bracket state.`

#### Examples

- **Valid example:** a semifinal winner is saved, the bracket updates immediately, and the leaderboard does not move yet.
- **Invalid example:** the leaderboard changes after the first semifinal while the tournament is still in progress.

#### Enforcement notes

- **API impact:** match-save workflows must materialize official entries without triggering standings too early.
- **UI impact:** tournament views should show progression immediately but defer leaderboard expectations.
- **Audit impact:** each official match outcome must be traceable.
- **Test impact:** progression and deferred-standings behavior need direct workflow coverage.

#### Related items

- **Related rules:** `BR-002`, `BR-005`
- **Related endpoints:** none yet
- **Related docs:** `docs/product/functional-requirements.md`, `docs/product/prd.md`, `docs/architecture/architecture.md`, `docs/domain/er-schema.md`
- **Related ADRs:** `ADR-0004`

## Live Games

### `BR-007` — Live ranking draft is provisional and never official truth

- **Status:** `active`
- **Area:** `live games`
- **Priority:** `critical`
- **Summary:** ranking live draft exists only for collaboration and recovery; it is initialized from official truth, never counts toward standings, and becomes obsolete when authoritative state is materialized.

#### Rule statement

`The live ranking draft must remain provisional collaboration state only; it must never be treated as official truth or as direct leaderboard input.`

#### Applies when

- a ranking game enters `in_progress`
- judges edit ranking data collaboratively
- the game leaves `in_progress`

#### Preconditions

- the game format is `ranking`
- the game is in live-entry mode

#### Required behavior

- initialize the live draft from the current official result state
- support exclusive field-level editing and stale-write rejection
- support reconnect and restart recovery from the latest server-side draft state
- keep the leaderboard unchanged while data is still only in the draft
- materialize changed values into official state when leaving `in_progress`
- clear the current live draft after materialization

#### Forbidden behavior

- treating live draft as official business history
- using in-progress draft data as leaderboard input
- using the live-draft subsystem for 1v1 tournaments in v1

#### Inputs / factors

- official result state
- live draft values
- live revision and conflict state
- game lifecycle transition

#### Outcome

- collaboration remains safe without polluting official truth
- authoritative writes stay separate from provisional editing

#### Edge cases

- multiple games may be in progress at the same time
- stale drafts from older live cycles must be ignored

#### Rationale

`Live collaboration improves result-entry ergonomics, but trust depends on keeping provisional draft state separate from authoritative audited state.`

#### Examples

- **Valid example:** judges edit draft fields during a ranking game while the leaderboard remains unchanged until completion.
- **Invalid example:** the public leaderboard updates from a partially saved ranking draft.

#### Enforcement notes

- **API impact:** realtime/live endpoints must reject stale concurrent writes clearly.
- **UI impact:** editors must see conflicts and know that in-progress data is provisional.
- **Audit impact:** draft snapshots are recovery state only, not authoritative business history.
- **Test impact:** realtime integration tests must protect conflict, recovery, and non-official semantics directly.

#### Related items

- **Related rules:** `BR-003`, `BR-008`
- **Related endpoints:** none yet
- **Related docs:** `docs/product/functional-requirements.md`, `docs/product/prd.md`, `docs/architecture/architecture.md`
- **Related ADRs:** `ADR-0005`

## Leaderboard / Projection

### `BR-005` — Pending admin review still counts using the latest official result

- **Status:** `active`
- **Area:** `leaderboard`
- **Priority:** `critical`
- **Summary:** pending admin review keeps the latest saved official result active in standings until an admin resolves the review.

#### Rule statement

`A game in pending_admin_review must continue to count in leaderboard calculations using the latest saved official result.`

#### Applies when

- a judge edits a completed game
- standings are recomputed or displayed while the game is pending review

#### Preconditions

- the game was already completed
- a judge edited the completed result, causing `pending_admin_review`

#### Required behavior

- move the game automatically to `pending_admin_review`
- keep the latest saved official result visible
- keep that latest official result counting in leaderboard calculations
- require admin action to move the game back to `completed`

#### Forbidden behavior

- removing the game from the leaderboard while it is only pending review
- allowing judges to resolve pending admin review back to completed

#### Inputs / factors

- lifecycle state
- latest saved official result
- reviewer role/capability

#### Outcome

- post-completion corrections stay visible and reviewable without erasing current standings truth
- admin review remains explicit

#### Edge cases

- the latest saved edit may already be publicly visible while review is pending
- audit history must support admin verification or reversion

#### Rationale

`Pending review means the latest authoritative save is still the current official result until an admin decides otherwise, so the leaderboard must not silently discard it.`

#### Examples

- **Valid example:** a judge edits a completed game, the game enters pending review, and the leaderboard still reflects the new saved result.
- **Invalid example:** the leaderboard drops the game entirely just because it is pending admin review.

#### Enforcement notes

- **API impact:** lifecycle and projection logic must preserve standings inclusion during pending review.
- **UI impact:** the state must be clearly labeled without implying the game stopped counting.
- **Audit impact:** post-completion edits and review decisions must be traceable.
- **Test impact:** pending-review projection semantics need direct integration coverage.

#### Related items

- **Related rules:** `BR-004`, `BR-006`, `BR-008`
- **Related endpoints:** none yet
- **Related docs:** `docs/product/functional-requirements.md`, `docs/product/prd.md`, `docs/architecture/architecture.md`
- **Related ADRs:** `ADR-0004`

## Authorization / Capabilities

> No additional stable authorization-specific business rules have been promoted here yet beyond the lifecycle restrictions captured in the rules above.

## Public Read / Visibility

### `BR-006` — Under examination remains visible but does not count

- **Status:** `active`
- **Area:** `public read`
- **Priority:** `critical`
- **Summary:** under-examination games remain publicly visible with the latest official result, but they are excluded from leaderboard calculations until resolved.

#### Rule statement

`A game under_examination must remain visible publicly using the latest official result, but it must not count in leaderboard calculations until the state is resolved.`

#### Applies when

- a judge or admin marks a game under examination
- public or internal read models render the game while it is under examination

#### Preconditions

- the game is in a relevant non-draft state
- the game has been marked `under_examination`

#### Required behavior

- keep the latest official result visible
- exclude the game from leaderboard calculations
- allow judges and admins to mark and resolve the state

#### Forbidden behavior

- hiding the game entirely from public visibility
- continuing to count the game in standings while it is under examination

#### Inputs / factors

- lifecycle state
- latest official result
- projection and public-read logic

#### Outcome

- the public can still see the contested official result
- standings remain protected from data that is temporarily under review

#### Edge cases

- a game can move into under examination from in progress or from an already official state
- latest official visibility does not imply standings inclusion

#### Rationale

`Under examination signals that the official result is visible but temporarily untrusted for standings, so visibility and counting must be separated deliberately.`

#### Examples

- **Valid example:** a completed game is marked under examination, remains visible publicly, and disappears from leaderboard totals.
- **Invalid example:** an under-examination game still contributes points to the leaderboard.

#### Enforcement notes

- **API impact:** public-read and leaderboard-projection paths must diverge on visibility vs counting.
- **UI impact:** the public view should label the game clearly as under examination.
- **Audit impact:** mark and resolve actions must be traceable.
- **Test impact:** non-counting semantics need direct coverage at the projection layer.

#### Related items

- **Related rules:** `BR-005`, `BR-007`
- **Related endpoints:** none yet
- **Related docs:** `docs/product/functional-requirements.md`, `docs/product/prd.md`, `docs/architecture/architecture.md`
- **Related ADRs:** `ADR-0004`, `ADR-0005`

---

## Known Ambiguities / Decisions Needed

- Additional stable BR entries should be promoted here when the current docs already agree on Prepalio aggregation details, Giocasport-specific standings behavior, or authorization/business-policy semantics beyond the rules above.
- When a rule is promoted here, keep the supporting test and API docs aligned in the same change.
