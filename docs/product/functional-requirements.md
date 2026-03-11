# Functional requirements — updated

This document replaces the previous functional requirements where they conflict with the latest clarified decisions.

## 0. Scope and boundaries

The system shall support exactly one active season in the database.

The system shall support exactly three competition contexts:
- Palio
- Prepalio
- Giocasport

The system shall support exactly four teams for the season.

The system shall prefill the four default rioni/teams and allow admins to edit them before official results exist.

The system shall optimize v1 for admins and judges, with a separate public read-only experience.

The system shall not require player-level participation tracking in v1.

The system shall not require player eligibility validation in v1.

The system shall not require import/export between years in v1.

The system shall not require scheduled datetime per game in v1.

## 1. Authorization and user management

The system shall use capability-based authorization.

The system shall define capabilities in code and persist roles, role-capability mappings, and user-role assignments in the database.

The system shall provide at least these default role bundles:
- Superadmin
- Admin
- Judge
- Public

The system shall support at least these capabilities:
- manage season config
- manage tournament pairings
- start game
- complete game
- mark under examination
- resolve under examination
- enter and edit results
- set Jolly usage
- apply manual standings adjustments
- view audit log
- review post-completion edits
- manage users

The system shall provide a minimal superadmin-only user management flow in v1.

The system shall allow superadmin to create a user with:
- email
- password
- one seeded role

The system shall create the user as active immediately.

The system shall not support self-registration in v1.

The system shall not support in-app password reset/change flows in v1.

The system shall not support in-app role editing in v1.

## 2. Season setup

The system shall allow admins to create one season in the UI.

The system shall allow admins to create games belonging to exactly one competition:
- Palio
- Prepalio
- Giocasport

The system shall allow admins to configure, per game:
- name
- competition
- game format
- selected catalog fields
- points table

The system shall use a seeded/static global field catalog in v1.

The system shall allow admins to choose which seeded catalog fields a game uses.

The system shall not support runtime creation or editing of field definitions in v1.

The system shall prevent deletion of any game that already has official result data.

The system shall prevent editing of any game definition after official result data exists.

Once a game has any official result data, the system shall treat every game property and relationship as immutable in v1, including at least:
- competition type
- game format
- configured fields
- points table
- other result-affecting configuration

## 3. Game formats

The system shall support exactly two formats in v1.

### 3.1 Ranking format

The system shall maintain one official per-team result for all four teams.

The system shall support official placement for all four teams.

The system shall support extra official field values through configured catalog fields.

The system shall allow ranking games to use catalog fields such as:
- time
- penalties
- score/quantity-like metric
- notes/text

The UI shall show the seeded field-catalog label, not a generic internal field name.

### 3.2 1v1 tournament format

The system shall model a fixed four-team tournament:
- two semifinals
- final 3rd/4th
- final 1st/2nd

The system shall allow admins and judges with the proper capability to set semifinal pairings before start.

The system shall derive the final tournament ranking automatically from the four match winners.

The system shall allow admins to change the final official placements if the automatically derived ranking must be overridden.

## 4. Official result model

The system shall maintain `game_entries` as the canonical official per-team result surface for every game format.

The system shall store official placement in the canonical per-team result.

The system shall store official Jolly usage in the canonical per-team result.

The system shall store additional official per-team result values in typed field rows linked to the configured game fields.

The system shall not require separate computed-ranking or ranking-override tables in v1.

The system shall treat the current official placement in the canonical per-team result as the source of truth for projections and standings.

## 5. Game lifecycle

The system shall support these game states:
- draft
- in progress
- completed
- pending admin review
- under examination

The system shall move a game to in progress only via explicit Start game.

The system shall allow a game to leave in progress to either:
- completed
- under examination

The system shall automatically move a completed game to pending admin review when a judge edits completed results.

A pending admin review game shall still count in leaderboard calculations using the latest saved official result.

A game under examination shall remain visible publicly but shall not count in leaderboard calculations.

Judges and admins shall be allowed to mark a game under examination and resolve it.

Only admins shall be allowed to move pending admin review back to completed.

## 6. Ranking-format live entry

The system shall support live result entry for ranking games while the game is in progress.

The system shall allow team-by-team in-progress editing while a ranking game is in progress.

The system shall support multiple games being in progress at the same time.

The system shall support field-level exclusive editing semantics for live entry, so concurrent editors cannot silently overwrite each other.

The system shall detect stale/concurrent writes and reject them with a clear error.

The system shall support reconnect/conflict recovery by restoring the latest server state and informing the user that a conflict occurred.

When a ranking game enters in progress, the system shall initialize the live draft from the current official result state.

The system shall support recovery of in-progress draft state after reconnect or backend restart.

The system shall not update the leaderboard from ranking in-progress draft data.

The system shall require manual placement entry in v1.

When a ranking game leaves in progress, the system shall materialize only the entries that actually changed compared with the official result state.

When a ranking game leaves in progress, the system shall clear the current live draft state.

## 7. 1v1 tournament result entry

In v1, the system shall bypass the live-draft subsystem for 1v1 tournaments.

Each saved 1v1 match outcome shall become official immediately.

Each saved 1v1 match outcome shall update tournament progression immediately.

Each saved 1v1 match outcome shall materialize/update the canonical official per-team result surface immediately.

The system shall expose bracket progression while the tournament is in progress.

The system shall expose the resulting final ranking as soon as it is derivable from official match outcomes.

The system shall recompute the leaderboard for a 1v1 tournament only when the tournament/game is completed.

## 8. Completion and validation

The system shall block completion unless:
- all four teams have placements
- placements are structurally valid
- enabled required fields are filled

The system shall validate ties expressed explicitly as placements such as `1,2,2,4`.

The system shall not allow structurally invalid placements to be completed.

Only completed games shall trigger leaderboard recomputation.

## 9. Scoring engine

The system shall compute points automatically from placement using the configured table.

The default points table shall be `4,3,2,1`.

The system shall support ex aequo scoring from explicitly entered placements.

The system shall support Jolly only for Palio games.

The system shall never allow Jolly for Prepalio or Giocasport.

The system shall allow per-team Jolly selection at game time.

The system shall reject Jolly if that team has already used it in another Palio game.

The system shall double the points of the affected Palio game result for that team.

The system shall provide a Jolly summary view.

## 10. Prepalio

The system shall treat Prepalio subgames as normal games within the Prepalio competition.

The system shall compute a Prepalio aggregate ranking from the points earned in Prepalio subgames.

The system shall map the final Prepalio ranking to a points table, default `4,3,2,1`, and add it to the main Palio standings.

The system shall support configurable tie strategy for the Prepalio aggregate ranking.

If automatic Prepalio tie resolution is insufficient, the system shall allow admins to set the official final placements manually.

The system shall never apply Jolly to Prepalio.

## 11. Giocasport

The system shall maintain a separate Giocasport leaderboard.

Giocasport results shall not affect the main Palio standings.

## 12. Manual standings adjustments

The system shall let admins create a leaderboard adjustment with at least:
- competition
- team
- signed point delta
- reason
- timestamp
- author

These adjustments shall affect the official standings immediately.

## 13. Public and maxi-screen views

The public interface shall be accessible without login.

The public interface shall have separate sections for:
- Palio
- Prepalio
- Giocasport

The public interface shall show:
- standings
- results
- notes
- history
- provisional status where relevant

The system shall publish official result changes immediately so the public can see them during the appeal window.

The system shall provide a separate maxi-screen mode in v1.

The maxi-screen shall be a dedicated presentation route/page, not a separate business workflow.

Advanced maxi-screen rotation/live logic remains out of scope for v1.

For live game pages, the client shall load an initial HTTP view and then subscribe to realtime updates.

## 14. Audit

The system shall maintain one generic append-only audit log for meaningful business changes.

The system shall store one audit row per changed business entity.

The system shall link audit rows from the same workflow by a shared correlation id.

Each audit record shall include at least:
- actor_user_id
- timestamp
- entity type
- entity key
- action type
- before snapshot
- after snapshot
- optional reason
- optional correlation id

The system shall store full before/after snapshots for audited entity changes.

The system shall audit authoritative business/operational entities only.

The system shall not audit read-model/projection churn.

The system shall not treat in-progress draft snapshots as official audited history.

The system shall audit at least:
- official result changes
- game state changes
- Jolly usage changes
- leaderboard adjustments
- tournament match updates
- user creation

## 15. Error behavior and collaboration safety

The system shall prevent silent overwrite of concurrent live-result edits.

The system shall return machine-readable error codes and structured data to the client.

The frontend shall be able to translate backend error codes into user-friendly messages.

## 16. E2E-critical behaviors

The system shall support these must-pass end-to-end behaviors in v1:
- complete a raning game
- update the public view after game completion
- progress and complete a 1v1 tournament
- edit a completed result and produce the expected review/audit behavior
- handle concurrent live-result updates with field lock/lease behavior
