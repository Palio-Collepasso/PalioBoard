# ADR-0004 — Official Result Model and Canonical Game Entries

- Status: Accepted
- Date: 2026-03-11

## Context

The system supports two templates in v1:

- ranking games
- fixed 4-rione 1v1 tournaments

Downstream scoring and leaderboard logic should not branch more than necessary by format.

## Decision

Use `game_entries` as the single canonical official per-team result surface for every game format.

Model:

- `game_entries`
  - official placement
  - official Jolly flag
- `game_entry_fields`
  - official typed extra values linked through the seeded field catalog
- `tournament_matches`
  - operational bracket record for 1v1
  - updates canonical `game_entries` immediately in v1

Remove the need for separate persistent computed-ranking and ranking-override tables.

The current official placement lives directly on `game_entries`.

History of automatic derivation vs manual override is preserved through the append-only audit log.

## Consequences

### Positive

- One official result surface for projections and scoring.
- Simpler leaderboard logic.
- Clear separation between official result state and bracket-operational state.

### Negative

- Side-by-side “computed vs override” comparison is no longer a first-class table-level feature.
- Audit quality becomes more important, because it is the only history source for placement changes.

## Follow-ups

- Keep audit rows rich enough to reconstruct official placement changes.
- Keep game properties and relationships immutable after official result data exists.
