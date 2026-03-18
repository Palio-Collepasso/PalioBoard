# Runtime Flows

## Purpose

This document describes only the critical write flows that are easy to break.
Use it when implementing or reviewing a change that touches transactions, official truth, projections, audit, or live entry.

Read this after:
1. `docs/architecture/architecture.md`
2. `docs/architecture/module-map.md`

## How to read these flows

Each flow lists:
- trigger
- preconditions
- ordered steps
- authoritative writes
- post-commit effects
- things that must not happen

Unless an ADR says otherwise, these flows are synchronous and transaction-oriented.

## Game state transition graph

## Start ranking game

**Trigger**
- admin or judge starts a ranking-format game

**Preconditions**
- caller has `start game`
- game is in `draft`
- game format is `ranking`

**Ordered steps**
1. Authenticate principal and resolve capabilities.
2. Load the game aggregate and verify current state.
3. Move game state from `draft` to `in_progress`.
4. Increment `games.live_cycle`.
5. Load current official `game_entries` and `game_entry_fields` for the game.
6. Hydrate the live draft in `live_games` from the current official state.
7. Persist a recovery snapshot for the new `live_cycle` if the implementation snapshots on initialization.
8. Append audit rows for the authoritative state change.
9. Commit the transaction.
10. After commit, publish realtime state for the game on a best-effort basis.

**Authoritative writes**
- `games.state`
- `games.live_cycle`
- `audit_logs`
- optional provisional `game_live_drafts` snapshot for recovery

**Must not happen**
- no leaderboard recomputation here
- no official result mutation here unless the official state must be normalized for prefill consistency

## Update ranking live draft

**Trigger**
- a live-entry user edits a field while the ranking game is in progress

**Preconditions**
- caller has result-entry capability
- game is in `in_progress`
- field belongs to the configured game
- client revision matches or can be rejected as stale
- lease ownership or lease acquisition succeeds

**Ordered steps**
1. Authenticate websocket/session and verify capability.
2. Load current in-memory draft snapshot for `(game_id, live_cycle)`.
3. Verify the incoming revision against the server revision.
4. Verify field lease ownership or acquire/renew the lease.
5. Apply the provisional change in memory.
6. Increment the game live revision.
7. Best-effort persist a coarse recovery snapshot when the configured trigger fires.
8. Broadcast the full per-game snapshot with the new revision.

**Authoritative writes**
- none to official result tables
- optional update to `game_live_drafts` recovery snapshot

**Must not happen**
- do not update `game_entries`
- do not update `leaderboard_current`
- do not append authoritative audit rows for keystroke-level draft changes

## Complete ranking game

**Trigger**
- admin or judge completes a ranking-format game from `in_progress`

**Preconditions**
- caller has `complete game`
- game is in `in_progress`
- live draft exists or official state can be loaded
- all four teams have structurally valid placements
- all enabled required fields are present
- Jolly usage is valid for the competition and team

**Ordered steps**
1. Authenticate principal and authorize.
2. Load the game aggregate and current live draft for the active `live_cycle`.
3. Compare draft state against current official `game_entries` / `game_entry_fields`.
4. Validate structural placement rules and required fields.
5. Validate Jolly rules across Palio games for the affected team.
6. Move game state from `in_progress` to `completed`.
7. Materialize only changed entries into canonical official tables.
8. Produce structured workflow facts for auditing.
9. Recompute affected leaderboard projections synchronously.
10. Append audit rows for the game state change and official result changes.
11. Commit the transaction.
12. After commit, emit realtime notification for screens and obsolete/clear the live draft on a best-effort basis.

**Authoritative writes**
- `games.state`
- `game_entries`
- `game_entry_fields`
- `leaderboard_current`
- `leaderboard_position_counts`
- `audit_logs`

**Best-effort post-commit / non-authoritative effects**
- realtime publication
- live draft cleanup for the completed cycle

**Must not happen**
- do not leave `in_progress` with only partial official materialization
- do not commit official result changes without projection recomputation
- do not roll back a successful transaction only because draft cleanup or post-commit notification fails

## Mark game under examination

**Trigger**
- judge or admin marks a game under examination from `in_progress`, `completed`, or `pending_admin_review`

**Preconditions**
- caller has `mark under examination`
- current state is allowed

**Ordered steps**
1. Authenticate and authorize.
2. Load current game state.
3. Move the game to `under_examination`.
4. Recompute projections if the previous state was counted (`completed` or `pending_admin_review`).
5. Append audit rows.
6. Commit.
7. Publish best-effort realtime update.

**Authoritative writes**
- `games.state`
- projection tables if the game previously counted
- `audit_logs`

**Must not happen**
- do not delete official result truth
- do not keep the game counted once it is `under_examination`

## Resolve under examination back to completed

**Trigger**
- judge or admin resolves a suspended game back to `completed`

**Preconditions**
- caller has `resolve under examination`
- game is in `under_examination`
- official result truth is present and valid

**Ordered steps**
1. Authenticate and authorize.
2. Load the game and current official result state.
3. Verify the official result state is valid for a counted game.
4. Move state to `completed`.
5. Recompute projections synchronously.
6. Append audit rows.
7. Commit.
8. Publish best-effort realtime update.

## Judge edits a completed game

**Trigger**
- judge edits official result data after a game is already `completed`

**Preconditions**
- caller has result-edit capability
- current state is `completed`
- requested edit preserves immutable setup and structural validity

**Ordered steps**
1. Authenticate and authorize.
2. Load current official result state.
3. Validate the requested official change against result rules.
4. Persist the changed official entries/fields.
5. Move the game state to `pending_admin_review`.
6. Recompute projections synchronously; the latest official result still counts.
7. Append audit rows for the result change and state change.
8. Commit.
9. Publish best-effort realtime update.

**Must not happen**
- do not exclude the game from standings just because it entered `pending_admin_review`
- do not allow edits that mutate setup/configuration instead of official result truth

## Admin resolves pending review back to completed

**Trigger**
- admin accepts or finalizes a game in `pending_admin_review`

**Preconditions**
- caller has `review post-completion edits`
- current state is `pending_admin_review`

**Ordered steps**
1. Authenticate and authorize.
2. Load the current official result state.
3. Verify the state is valid for counted standings.
4. Move the game back to `completed`.
5. Recompute projections if needed.
6. Append audit rows.
7. Commit.
8. Publish best-effort realtime update.

## Save tournament match outcome

**Trigger**
- admin or judge saves a semifinal or final outcome in a 1v1 tournament game

**Preconditions**
- caller has result-entry capability
- game format is `tournament_1v1`
- current match pairing is valid
- winner is one of the paired teams

**Ordered steps**
1. Authenticate and authorize.
2. Load the game aggregate and current tournament bracket state.
3. Persist the match outcome in `tournament_matches`.
4. Derive newly known bracket consequences.
5. Materialize the corresponding current official per-team surface in `game_entries`.
6. If the last required match is now official, derive final placements for all four teams.
7. If the tournament/game becomes complete, move `games.state` to `completed` and recompute the leaderboard.
8. Append audit rows.
9. Commit.
10. Publish best-effort realtime/public updates.

**Authoritative writes**
- `tournament_matches`
- `game_entries`
- possibly `games.state`
- projection tables only when the whole tournament becomes complete
- `audit_logs`

**Must not happen**
- do not route tournament outcomes through ranking live draft
- do not recompute leaderboard on every intermediate match if the tournament is not complete

## Apply manual leaderboard adjustment

**Trigger**
- an authorized admin applies a manual delta to a competition leaderboard

**Preconditions**
- caller has adjustment capability
- target competition and team exist
- reason is provided

**Ordered steps**
1. Authenticate and authorize.
2. Persist the authoritative adjustment input.
3. Recompute the affected leaderboard scope synchronously.
4. Append audit rows.
5. Commit.
6. Publish best-effort read-model update.

**Authoritative writes**
- `leaderboard_adjustments`
- `leaderboard_current`
- `leaderboard_position_counts`
- `audit_logs`

## Provision a new user

**Trigger**
- superadmin creates a new user in v1

**Preconditions**
- caller has `manage users`
- email is not already linked to an application user
- selected role is one of the seeded roles

**Ordered steps**
1. Authenticate and authorize the superadmin.
2. Create the identity-provider account through the identity adapter.
3. Create the application user row linked to the auth user id.
4. Assign the seeded role.
5. Append audit rows.
6. Commit the local transaction.
7. If local user creation fails after remote identity creation, attempt best-effort compensation by removing the remote identity and surface the partial-failure state clearly.

**Must not happen**
- do not leave silent split-brain between identity provider and app user truth
- do not bypass audit for user-management actions

## Common transaction rules

These rules apply to all critical flows unless a later ADR changes them:
- authoritative state writes, audit writes, and required projection updates succeed or fail together
- realtime notifications are post-commit and best effort
- draft cleanup failures do not invalidate a successful authoritative transaction
- read models are recomputed from authoritative truth; they are never the source of truth
- cross-module sequencing belongs in explicit orchestrators, not in hidden callbacks or transport code

## Review checklist for high-risk changes

Before merging a change that touches one of these flows, verify:
- source of truth is unchanged or intentionally updated with docs/ADR support
- `pending_admin_review` still counts and `under_examination` still excludes
- tournament outcomes still bypass live draft
- only changed ranking entries are materialized on completion
- audit rows are still written for authoritative changes
- projection recomputation still happens inside the business transaction
- post-commit notification failure still does not roll back the transaction
