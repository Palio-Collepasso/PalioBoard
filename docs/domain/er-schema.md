# ER Schema

This document is the current ER direction to reflect the architectural decisions discussed so far.

## Notes

- `NN` means **NOT NULL**.
- `PK` means **primary key**.
- `FK` means **foreign key**.
- `UQ` means **unique constraint**.
- `CK` means **check constraint**.
- `TZ` means **timestamp with time zone / UTC in storage**.

---

## Code-defined values (stored as text + constrained in DB)

### `competition_type`
- `palio`
- `prepalio`
- `giocasport`

### `game_format`
- `ranking`
- `tournament_1v1`

### `game_state`
- `draft`
- `in_progress`
- `completed`
- `pending_admin_review`
- `under_examination`

### `field_type`
- `penalty`
- `time`
- `score`
- `text`

### `tournament_round_type`
- `semifinal`
- `final_3rd_4th`
- `final_1st_2nd`

---

## Tables

### `seasons`

Represents the current competition year.

| Column | Type | Constraints |
|---|---|---|
| id | uuid | PK |
| name | varchar(120) | NN |
| year_label | integer | NN, UQ |

---

### `teams`

Represents a rione/team for the season.

| Column | Type | Constraints |
|---|---|---|
| id | uuid | PK |
| season_id | uuid | FK -> seasons.id, NN |
| name | varchar(120) | NN |
| color | varchar(32) |  |

**Table constraints / indexes**
- `UQ (season_id, name)`
- `IDX (season_id)`

---

### `competitions`

Represents a competition for the season: `Palio`, `Prepalio`, or `Giocasport`.

| Column | Type | Constraints |
|---|---|---|
| id | uuid | PK |
| season_id | uuid | FK -> seasons.id, NN |
| type | varchar(32) | NN |

**Table constraints / indexes**
- `UQ (season_id, type)`
- `IDX (season_id)`
- `CK (type IN ('palio','prepalio','giocasport'))`

---

### `games`

One configured game inside a competition.

`live_cycle` is a **technical** counter incremented every time the game enters `in_progress`. It is not business state.

| Column | Type | Constraints |
|---|---|---|
| id | uuid | PK |
| competition_id | uuid | FK -> competitions.id, NN |
| name | varchar(160) | NN |
| game_format | varchar(32) | NN |
| state | varchar(40) | NN |
| version | integer | NN, default 0 |
| live_cycle | integer | NN, default 0 |

**Table constraints / indexes**
- `UQ (competition_id, name)`
- `IDX (competition_id, state)`
- `CK (version >= 0)`
- `CK (live_cycle >= 0)`
- `CK (game_format IN ('ranking','tournament_1v1'))`
- `CK (state IN ('draft','in_progress','completed','pending_admin_review','under_examination'))`

**Semantic rule**
- Once a game has any official result data, **every game property/relationship becomes immutable**.

---

### `fields`

Global **seeded/static** catalog of configurable result fields.

| Column | Type | Constraints |
|---|---|---|
| id | uuid | PK |
| field_key | varchar(80) | NN, UQ |
| field_label | varchar(120) | NN |
| field_type | varchar(32) | NN |

**Table constraints / indexes**
- `CK (field_type IN ('penalty','time','score','text'))`

---

### `game_fields`

Many-to-many between `games` and `fields`, plus per-game ordering.

| Column | Type | Constraints |
|---|---|---|
| game_id | uuid | PK, FK -> games.id, NN |
| field_id | uuid | PK, FK -> fields.id, NN |
| display_order | integer | NN |

**Table constraints / indexes**
- `UQ (game_id, display_order)`
- `IDX (field_id)`
- `CK (display_order >= 1)`

**Semantic rule**
- Once a game has any official result data, its `game_fields` configuration is immutable.

---

### `game_entries`

Canonical **official** per-team result surface for every game format.

This table is the official truth for placements and Jolly. Even 1v1 tournaments materialize their per-team official outcome here.

| Column | Type | Constraints |
|---|---|---|
| game_id | uuid | PK, FK -> games.id, NN |
| team_id | uuid | PK, FK -> teams.id, NN |
| placement | smallint |  |
| is_jolly | boolean | NN, default false |

**Table constraints / indexes**
- `IDX (team_id)`
- `IDX (game_id, placement)`
- `CK (placement IS NULL OR placement >= 1)`

---

### `game_entry_fields`

Official typed values for the configured fields of a `game_entry`.

| Column | Type | Constraints |
|---|---|---|
| game_id | uuid | PK, NN |
| team_id | uuid | PK, NN |
| field_id | uuid | PK, NN |
| value_number | numeric(12,3) |  |
| value_text | text |  |
| value_duration_ms | integer |  |

**Table constraints / indexes**
- `FK (game_id, team_id) -> game_entries(game_id, team_id)`
- `FK (game_id, field_id) -> game_fields(game_id, field_id)`
- `CK (value_duration_ms IS NULL OR value_duration_ms >= 0)`
- `CK (num_nonnulls(value_number, value_text, value_duration_ms) = 1)`

---

### `tournament_matches`

Operational record for the fixed 4-team 1v1 bracket.

In v1 this bypasses the live-draft subsystem: each saved match outcome is official immediately and updates canonical `game_entries`, but leaderboard recomputation still waits for game completion.

| Column | Type | Constraints |
|---|---|---|
| id | uuid | PK |
| game_id | uuid | FK -> games.id, NN |
| round_type | varchar(40) | NN |
| team_a_id | uuid | FK -> teams.id, NN |
| team_b_id | uuid | FK -> teams.id, NN |
| winner_team_id | uuid | FK -> teams.id |

**Table constraints / indexes**
- `UQ (game_id, round_type)`
- `IDX (game_id)`
- `CK (team_a_id <> team_b_id)`
- `CK (round_type IN ('semifinal','final_3_4','final_1_2'))`

---

### `points`

Placement-to-points mapping for a game.

| Column | Type | Constraints |
|---|---|---|
| game_id | uuid | PK, FK -> games.id, NN |
| placement | smallint | PK |
| value | smallint | NN |

**Table constraints / indexes**
- `IDX (game_id)`
- `CK (placement >= 1)`

**Semantic rule**
- Once a game has any official result data, its points mapping is immutable.

---

### `leaderboard_adjustments`

Manual point deltas applied directly to a competition leaderboard.

| Column | Type | Constraints |
|---|---|---|
| id | uuid | PK |
| competition_id | uuid | FK -> competitions.id, NN |
| team_id | uuid | FK -> teams.id, NN |
| delta_points | integer | NN |
| reason | text | NN |
| created_by | uuid | FK -> users.id, NN |
| created_at | timestamptz | NN |

---

### `leaderboard_current`

Current computed leaderboard totals per season / competition / team. This is a synchronous write-through projection.

| Column | Type | Constraints |
|---|---|---|
| season_id | uuid | PK, FK -> seasons.id, NN |
| competition_id | uuid | PK, FK -> competitions.id, NN |
| team_id | uuid | PK, FK -> teams.id, NN |
| total_points | integer | NN |
| games_counted | integer | NN, default 0 |
| computed_at | timestamptz | NN |

**Table constraints / indexes**
- `CK (games_counted >= 0)`

---

### `leaderboard_position_counts`

Current count of how many times each team has achieved each placement in the leaderboard scope.

| Column | Type | Constraints |
|---|---|---|
| season_id | uuid | PK, NN |
| competition_id | uuid | PK, NN |
| team_id | uuid | PK, NN |
| placement | smallint | PK, NN |
| occurrence_count | integer | NN, default 0 |

**Table constraints / indexes**
- `FK (season_id, competition_id, team_id) -> leaderboard_current(season_id, competition_id, team_id)`
- `CK (occurrence_count >= 0)`
- `CK (placement >= 1)`

---

### `users`

Application users, linked 1:1 to the external identity-provider user.

| Column | Type | Constraints |
|---|---|---|
| id | uuid | PK |
| auth_user_id | uuid | NN, UQ |
| name | varchar(120) | NN |
| email | varchar(320) | NN, UQ |

---

### `roles`

Seeded role bundles.

| Column | Type | Constraints |
|---|---|---|
| id | uuid | PK |
| name | varchar(80) | NN, UQ |

---

### `user_roles`

| Column | Type | Constraints |
|---|---|---|
| user_id | uuid | PK, FK -> users.id, NN |
| role_id | uuid | PK, FK -> roles.id, NN |

---

### `capabilities`

Capability catalog. Capabilities are defined in code; the DB stores seeded catalog rows and mappings.

| Column | Type | Constraints |
|---|---|---|
| id | uuid | PK |
| code | varchar(120) | NN, UQ |
| description | text |  |

---

### `role_capabilities`

Many-to-many between roles and capabilities.

| Column | Type | Constraints |
|---|---|---|
| role_id | uuid | PK, FK -> roles.id, NN |
| capability_id | uuid | PK, FK -> capabilities.id, NN |

---

### `user_capabilities`

Direct per-user capability grants. Supported by schema, but not used in v1 UI/flows.

| Column | Type | Constraints |
|---|---|---|
| user_id | uuid | PK, FK -> users.id, NN |
| capability_id | uuid | PK, FK -> capabilities.id, NN |
| created_at | timestamptz | NN |

---

### `audit_logs`

Generic append-only audit history for meaningful business actions.

Because some audited authoritative entities use composite keys, the table stores a structured `entity_key_json` instead of a single scalar `entity_id`.

| Column | Type | Constraints |
|---|---|---|
| id | uuid | PK |
| created_at | timestamptz | NN |
| actor_user_id | uuid | FK -> users.id, NN |
| entity_type | varchar(80) | NN |
| entity_key_json | jsonb | NN |
| action_type | varchar(80) | NN |
| before_json | jsonb |  |
| after_json | jsonb |  |
| reason_code | varchar(80) |  |
| reason_text | text |  |
| correlation_id | uuid |  |

**Table constraints / indexes**
- `IDX (entity_type, created_at)`
- `IDX (actor_user_id, created_at)`
- `IDX (correlation_id)`
- `GIN (entity_key_json)`

---

### `game_live_drafts`

Persisted **provisional recovery snapshots** for memory-first live entry.

This table is **not** official business state and is **not** audited as official history. It exists only to restore live draft state after reconnect/restart.

A stale row from an old `live_cycle` is harmless and ignored.

| Column | Type | Constraints |
|---|---|---|
| game_id | uuid | PK, FK -> games.id, NN |
| live_cycle | integer | PK, NN |
| revision | integer | NN |
| snapshot_json | jsonb | NN |
| persisted_at | timestamptz | NN |

**Table constraints / indexes**
- `CK (live_cycle >= 1)`
- `CK (revision >= 0)`
- `IDX (persisted_at)`

**Semantic rules**
- Active field leases do **not** live here.
- When a game re-enters `in_progress`, live draft is prefilled from current official `game_entries`.
- When a game leaves `in_progress`, changed draft values are materialized into official rows and the current live draft becomes obsolete. Draft cleanup is best-effort and does not affect business-transaction success.

---

## Relationships

### Foreign-key relationships

- `teams.season_id` -> `seasons.id`
- `competitions.season_id` -> `seasons.id`
- `games.competition_id` -> `competitions.id`
- `game_fields.game_id` -> `games.id`
- `game_fields.field_id` -> `fields.id`
- `game_entries.game_id` -> `games.id`
- `game_entries.team_id` -> `teams.id`
- `game_entry_fields.(game_id, team_id)` -> `game_entries.(game_id, team_id)`
- `game_entry_fields.(game_id, field_id)` -> `game_fields.(game_id, field_id)`
- `tournament_matches.game_id` -> `games.id`
- `tournament_matches.team_a_id` -> `teams.id`
- `tournament_matches.team_b_id` -> `teams.id`
- `tournament_matches.winner_team_id` -> `teams.id`
- `points.game_id` -> `games.id`
- `leaderboard_adjustments.competition_id` -> `competitions.id`
- `leaderboard_adjustments.team_id` -> `teams.id`
- `leaderboard_adjustments.created_by` -> `users.id`
- `leaderboard_current.season_id` -> `seasons.id`
- `leaderboard_current.competition_id` -> `competitions.id`
- `leaderboard_current.team_id` -> `teams.id`
- `leaderboard_position_counts.(season_id, competition_id, team_id)` -> `leaderboard_current.(season_id, competition_id, team_id)`
- `user_roles.user_id` -> `users.id`
- `user_roles.role_id` -> `roles.id`
- `role_capabilities.role_id` -> `roles.id`
- `role_capabilities.capability_id` -> `capabilities.id`
- `user_capabilities.user_id` -> `users.id`
- `user_capabilities.capability_id` -> `capabilities.id`
- `audit_logs.actor_user_id` -> `users.id`
- `game_live_drafts.game_id` -> `games.id`

---

## Concise semantic model

- A **season** contains multiple **teams** and **competitions**.
- A **competition** contains multiple **games**.
- Each **game** enables one or more seeded catalog fields through **game_fields**.
- Official per-team result truth always lives in **game_entries** plus **game_entry_fields**.
- A **1v1 tournament** uses **tournament_matches** as the operational bracket record, but still materializes official per-team result truth into **game_entries**.
- **points** stores placement-to-points mapping per game.
- **leaderboard_adjustments** stores manual point deltas per competition/team.
- **leaderboard_current** and **leaderboard_position_counts** are synchronous write-through projections.
- **users / roles / capabilities** implement capability-based authorization with seeded roles and future-compatible direct grants.
- **audit_logs** stores meaningful business history as append-only before/after snapshots.
- **game_live_drafts** stores provisional whole-game recovery snapshots for memory-first live-entry only.

---

## Implementation notes intentionally kept outside business schema

These are important, but they should be treated as implementation details rather than domain semantics:

- UUIDv7 generation happens in **Python**, not in database defaults.
- `live_cycle` is technical state, not user-facing business state.
- Live field leases are **memory-first** in v1 and should sit behind a `LiveGameStateStore` adapter.
- Realtime notifications are **post-commit best effort** and are not part of business consistency.
