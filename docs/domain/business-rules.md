# Business Rules

## Purpose
Capture the compact set of normative domain rules that agents must preserve when implementing code.

## Document boundary
This file owns **domain truth and invariants**.
It does **not** own:
- exact API envelopes or statuses — see `docs/api/*`
- test depth or automation choice — see `docs/testing/*`
- seeded game-by-game configuration — see `docs/domain/game-catalog.md`
- implementation placement — see `docs/architecture/module-map.md`

Use this file when you need to know what must stay true regardless of UI flow, endpoint shape, or persistence details.

## Rule index

Numbers refers to `### <number>. ` in `docs/product/acceptance-scenarios.md`

| Rule ID | Title | Area | Primary related scenarios |
|---|---|---|---|
| `BR-001` | Fixed season, team, and competition scope | season setup | setup flows |
| `BR-002` | Game configuration becomes immutable after official result data exists | season setup | `AS-016` |
| `BR-003` | Ranking completion requires complete and structurally valid official data | results | `AS-001`, `AS-002` |
| `BR-004` | Jolly is Palio-only and single-use per team | results | `AS-011`, `AS-012` |
| `BR-005` | Pending admin review still counts using the latest official result | leaderboard | `AS-009` |
| `BR-006` | Under examination remains visible but does not count | public read | `AS-010` |
| `BR-007` | Live ranking draft is provisional and never official truth | live games | `AS-004`, `AS-005`, `AS-006` |
| `BR-008` | Tournament matches are official immediately but leaderboard impact waits for completion | tournaments | `AS-007`, `AS-008` |
| `BR-009` | Protected admin actions require a linked application user and capability check | auth | auth integration |

## Rules
### `BR-001` — Fixed season, team, and competition scope
**Statement**
- v1 models exactly one active season per database.
- v1 models exactly four teams for that season.
- Games may belong only to `palio`, `prepalio`, or `giocasport`.

**Required behavior**
- Setup flows and validations must preserve the fixed four-team, one-season, three-competition model.
- Downstream standings and workflow logic may rely on that fixed scope.

**Must reject or never support in v1**
- extra competition contexts
- variable team counts per season
- multi-season runtime behavior in the same database

**Related docs**
- `docs/product/functional-requirements.md`
- `docs/domain/er-schema.md`
- `docs/architecture/architecture.md`

### `BR-002` — Game configuration becomes immutable after official result data exists
**Statement**
- Once a game has any official result data, every result-affecting part of its configuration becomes immutable in v1.

**Required behavior**
- Block edits to competition, format, selected fields, points table, and other result-affecting setup.
- Block deletion of the game.
- Keep official historical data interpretable against the configuration that produced it.

**Must reject or never allow**
- changing result-affecting configuration after official data exists
- deleting a game that already has official result data

**Notes**
- Immutability starts with any official data, not only after final completion.
- Technical live-cycle counters do not override setup immutability.

**Related scenarios**
- `AS-016`

### `BR-003` — Ranking completion requires complete and structurally valid official data
**Statement**
- A ranking game may complete only when all four teams have official placements, the placements are structurally valid, and all enabled required fields are filled.

**Required behavior**
- Require placements for all four teams.
- Accept explicit valid ties such as `AS-001`,`AS-002`,`AS-002`,`AS-004`.
- Require every enabled required field before completion.
- Recompute standings only from a valid completed state.

**Must reject**
- missing placements
- structurally invalid placements such as `AS-001`,`AS-002`,`AS-002`,`AS-003`
- completion while required enabled fields are still empty

**Related scenarios**
- `AS-001`
- `AS-002`

### `BR-004` — Jolly is Palio-only and single-use per team
**Statement**
- Jolly may be recorded only for Palio games and at most once per team across Palio games.

**Required behavior**
- Reject any Jolly usage in Prepalio or Giocasport.
- Reject Jolly reuse for the same team.
- When valid, double that team's points for the affected Palio game.

**Must reject**
- second Jolly for the same team
- Jolly on non-Palio competitions

**Notes**
- In v1 Jolly is recorded during result entry, even though the real-world rule expects pre-game declaration.

**Related scenarios**
- `AS-011`
- `AS-012`

### `BR-005` — Pending admin review still counts using the latest official result
**Statement**
- `pending_admin_review` keeps counting in standings using the latest saved official result until an admin resolves the review.

**Required behavior**
- Move a completed game into `pending_admin_review` when a judge edits it.
- Keep the latest saved result visible.
- Keep that latest saved result counting in standings.
- Require admin action to return to normal completed state.

**Must reject or never do**
- dropping the game from standings only because it is pending review
- letting judges resolve the review state back to normal completion on their own

**Related scenarios**
- `AS-009`

### `BR-006` — Under examination remains visible but does not count
**Statement**
- `under_examination` keeps the latest official result visible but excludes the game from standings until resolved.

**Required behavior**
- Keep the official result visible in public and admin reads.
- Exclude the game from leaderboard calculations.
- Allow the state to be marked and resolved through the proper workflow.

**Must reject or never do**
- hiding the game entirely from public views
- continuing to count it in standings while it is under examination

**Related scenarios**
- `AS-010`

### `BR-007` — Live ranking draft is provisional and never official truth
**Statement**
- Live ranking entry stores provisional draft state only; it must never become authoritative until the official completion workflow succeeds.

**Required behavior**
- Prefill live draft state from the current official result when a ranking game starts.
- Keep live draft updates separate from authoritative result storage.
- Reject stale concurrent writes instead of silently overwriting newer draft state.
- Restore the latest saved draft after reconnect or restart when draft state exists.

**Must reject or never do**
- changing standings from live draft saves alone
- treating live draft storage as official business history

**Related scenarios**
- `AS-004`
- `AS-005`
- `AS-006`

### `BR-008` — Tournament matches are official immediately but leaderboard impact waits for completion
**Statement**
- Tournament match outcomes become official as soon as they are saved, but leaderboard impact happens only when the whole tournament game is completed.

**Required behavior**
- Save semifinal and final match winners as official tournament state.
- Expose derived bracket progression immediately.
- Delay leaderboard impact until the tournament game reaches completed state.

**Must reject or never do**
- counting tournament points in the leaderboard before completion
- treating intermediate bracket state as provisional draft data

**Related scenarios**
- `AS-007`
- `AS-008`

### `BR-009` — Protected admin actions require a linked application user and capability check
**Statement**
- A protected admin action requires both a valid authenticated identity that resolves to a linked application user and the required capability check in Python.

**Required behavior**
- Validate the bearer token through the configured identity adapter.
- Resolve the linked application user before treating the request as authenticated.
- Derive effective capabilities from application authorization data.
- Return `unauthenticated` for missing, invalid, or unlinked identities.
- Return `forbidden` for authenticated users that lack the required capability.

**Must reject or never do**
- trusting provider JWT claims as business authorization truth
- allowing a valid identity-provider user through without a linked application user
- bypassing Python capability checks for protected business actions

**Related docs and tests**
- `docs/api/error-contract.md`
- `docs/domain/capabilities.yaml`
- `docs/testing/fixtures.md` (`FX-003`)
