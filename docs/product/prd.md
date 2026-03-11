# Product concept

**PalioBoard** is an operations-first web app for running the Palio, optimized for admins and judges on laptops, with a separate public read-only experience and a separate maxi-screen mode.

It is **not** a generic sports platform.
It is a **rules-aware event control system** for a 4-team competition with:

* automatic leaderboard calculation
* Jolly handling
* Prepalio aggregation into the main Palio standings
* separate Giocasport standings
* live public visibility for appeals
* full auditability for post-result edits

This fits the actual structure of the event: 4 fixed teams, `4-3-2-1` scoring with ex aequo, one Jolly per team declared before the relevant game, Giocasport tracked separately, Prepalio made of subgames whose combined ranking yields points for the main Palio, and written appeals allowed within 15 minutes after each game.     

# Problem

Today Excel is “good enough” for totals and rankings, but weak for the parts that matter most during the event:

* fast result capture
* live publication
* tournament handling
* safe corrections after publication
* consistent audit trail

The product job for v1 is to make **result entry fast, visible, and trusted**.

# Goals

## Primary goals

* Let judges/admins record game results quickly at team level.
* Publish results immediately to the public.
* Compute standings automatically.
* Support Palio, Prepalio, and Giocasport in one app, but as clearly separate competition areas.
* Preserve trust with logs, correction history, and explicit game states.

## Non-goals for v1

* player-level roster participation
* eligibility validation
* season import/export
* automatic ranking derivation from times/quantities/penalties
* scheduled datetime per game
* live 1v1 score entry
* advanced maxi-screen rotation/live logic

# Users

## Primary

* Admins
* Judges

## Secondary

* Public audience, no login

# Product principles

First, optimize for **backoffice reliability**, not feature breadth.

Second, avoid a generic form-builder.
Use only **two competition templates**:

* ranking format with optional fields
* fixed 4-team 1v1 tournament format

Third, keep every important correction **visible and auditable**.

# Scope

## Competitions

The app supports three separate competition contexts:

* **Palio**
* **Prepalio**
* **Giocasport**

Giocasport has its own leaderboard and does not assign points to the main Palio standings. Prepalio is made of subgames whose points are summed into a final Prepalio ranking, and that final ranking assigns points to the main Palio standings.  

## Teams

* Exactly 4 teams per season
* Created each year with default values, but editable before results exist

## Season scope

* One competition year per database
* No multi-year analytics in v1

# Templates

## 1. Ranking format

Used for all non-1v1 games.

Always records:

* team
* placement

Optional per game catalog fields:
* time
* quantity / score / points / etc.
* penalties
* public notes

Important: the UI must show the **seeded field-catalog label**, never a generic internal field name.

Judges can save partial data while the game is in progress. Final placements are entered manually. Leaderboard changes only when the game is completed.

## 2. Fixed 1v1 tournament format

Always modeled as:

* semifinal
* final 3rd/4th
* final 1st/2nd

Semifinal pairings are manually set shortly before the tournament. Judges record match winners only. Final tournament ranking is computed automatically from the four match outcomes. This matches the event’s recurring semifinal/final structure used in Prepalio quadrangular tournaments. 

Admins can manually override any automatically computed ranking.

# Admin setup

Admins can:

* create/edit/delete games
* choose competition: Palio / Prepalio / Giocasport
* choose format: ranking / 1v1
* choose which catalog fields the game uses
* configure points tables per game / competition item, with default `4,3,2,1`
* manage teams
* create manual leaderboard adjustments

Rules:

* competition contribution is implicit from competition type
* no active/visible toggle in v1
* a game with any recorded result cannot be deleted
* once a game has any official result data, every game property and relationship becomes immutable in v1
* the field catalog is seeded/static in v1; admins only choose which catalog fields a game uses

# Result-entry workflow

## Ranking-format flow

1. Judge/admin opens the game
2. Clicks **Start game**
3. Enters partial values team by team during the game
4. Saves in-progress updates
5. Enters final placements manually
6. Clicks **Complete game**
7. System validates structure and updates standings

Completion is blocked unless:

* all 4 teams are present
* placements are valid, including ties such as `1,2,2,4`
* all enabled required fields are filled

## 1v1 flow

1. Pairings are set before start
2. Judge/admin starts tournament
3. Winners are entered for each match
4. Bracket progression becomes visible immediately
5. Final ranking is computed automatically
6. Admin may override if needed
7. Tournament is completed and only then does it affect the leaderboard

# Scoring and standings

## Base points

Default table: `4,3,2,1`

The regulation uses `4-3-2-1`, gives ex aequo in ties, and gives Giocasport the same points structure.  

## Tie handling

Judges enter placements explicitly, for example:

* `1,2,2,4`

The system validates placement structure and applies points accordingly.

## Jolly

Model:

* each team can use Jolly once
* only in Palio
* declared before the game
* recorded at result-entry time as a per-team flag
* blocked if that team has already used Jolly in another Palio game

The regulation requires that Jolly be presented before the relevant game and doubles the points obtained in that discipline. 

The app must also provide a **Jolly summary page** by team and game.

## Prepalio

Prepalio is not just another game.

Model:

* Prepalio contains multiple subgames
* each subgame generates points using the normal game points logic
* the app sums Prepalio subgame points to produce a final Prepalio ranking
* that final ranking assigns points to the main Palio standings
* Jolly is not allowed in Prepalio

The regulation explicitly defines Prepalio as several competitions whose points are summed, after which `4,3,2,1` are assigned to the final Prepalio ranking.  

If the configured automatic strategy cannot fully resolve a final Prepalio tie, admin can manually override the official final ranking.

## Giocasport

Giocasport:

* has its own games
* uses the same points logic
* has its own separate leaderboard
* does not contribute to the Palio standings

That separation is explicit in the regulation.  

## Manual standings adjustments

Admins can apply manual overall-standings adjustments such as:

* e.g. `-2` points to a team
* reason required
* fully audited

This is justified by the rules allowing judges to subtract classification points for serious acts. 

# Game states

Game states in v1:

* **draft / not started**
* **in progress**
* **completed**
* **pending admin review**
* **under examination**

Transitions:

* `draft -> in progress` via explicit **Start game**
* `in progress -> completed` via **Complete game**
* `in progress -> under examination` is allowed when the latest in-progress data must be frozen for review
* `completed -> pending admin review` automatically when a judge edits a completed result
* `any relevant non-draft state -> under examination` by judge/admin
* `under examination -> completed` by judge/admin
* `pending admin review -> completed` by admin after review

Behavior:

* **completed**: counted in leaderboard
* **pending admin review**: still counted, latest edit is public, admin should verify or revert using audit history
* **under examination**: latest materialized result remains visible publicly, but the game is excluded from leaderboard calculation

This state model supports the 15-minute appeal window while keeping public visibility. The regulation allows written appeals within 15 minutes after each game and recognizes post-game rulings that may affect placements. 

# Permissions

Authorization is capability-based. Roles are only bundles.

## Capability set

* Manage season config
* Manage tournament pairings
* Start game
* Complete game
* Mark under examination
* Resolve under examination
* Enter and edit results
* Set Jolly usage
* Apply manual standings adjustments
* View audit log
* Review post-completion edits and move pending admin review back to completed

## Default bundles

**Superadmin**

* admin capabilities
* user creation capability
* future app-management capabilities

**Admin**

* all operational/admin capabilities except superadmin-only user management

**Judge**

* manage tournament pairings
* start game
* complete game
* mark/resolve under examination
* enter/edit results
* set Jolly usage
* view allowed operational screens

**Public**

* no login
* read-only

# User management and authentication

v1 keeps user management intentionally minimal.

* no self-registration
* no in-app password reset/change flow
* a **superadmin** can create a user with **email + password + one seeded role**
* created users are active immediately
* role/capability catalogs are seeded/static in v1

This keeps the private operational shell controlled without expanding v1 into a full identity-management product.

# Public experience

Public view is open without login.

Three separate sections:

* Palio
* Prepalio
* Giocasport

Public can see:

* results
* notes
* standings
* game history
* Jolly summary where relevant

Notes are public by design.

When a game is under examination:

* show latest result
* clearly label it provisional / under examination
* exclude it from the leaderboard

# Maxi-screen mode

v1 includes a dedicated maxi-screen mode, separate from the normal public UI.

But all advanced maxi-screen logic is postponed to future versions.
So v1 maxi-screen is a simpler specialized read-only layout, not a live event-control engine.

# Audit and trust

Every important change must be logged with:

* who changed it
* when
* before
* after
* reason where required

Audit is essential because:

* results become public immediately
* written appeals can be filed within 15 minutes
* completed games may later be edited
* standings may receive manual adjustments 

# Acceptance criteria for v1

v1 succeeds if:

* an admin can configure a season fully in the UI
* judges can record a raning game team by team during play
* judges can complete a game only when the result is structurally valid
* the system computes standings automatically
* Jolly is validated and applied correctly
* Prepalio subgames roll up into a final Prepalio ranking and then into the Palio leaderboard
* Giocasport remains separate
* 1v1 tournament rankings derive automatically from four match winners
* public users see updates immediately
* 1v1 bracket progression is visible while the tournament is in progress, but standings change only after tournament completion
* edits after completion are auditable and flagged
* under-examination games are visible but excluded from standings
* once a game has official result data, its setup becomes immutable

# Biggest risks
* **Scope creep**: trying to support too many custom game behaviors could turn v1 into a generic sports engine
* **Trust risk**: one incorrect leaderboard update during the event could damage adoption
* **Setup complexity**: moving configuration into the app creates UX pressure on admin setup flows
* **Prepalio complexity**: it is both an internal competition and an input into the main Palio standings
* **Permission sprawl**: capability-based authorization could become too granular too early
* **Operational ambiguity**: public visibility, post-completion edits, and under-examination states must remain easy to understand

# Success Metrics

* Judges/admins can complete result entry for a standard game quickly enough to keep pace with the live event
* 100% of completed games update standings automatically without manual spreadsheet recalculation
* 100% of post-completion edits and manual standings adjustments are captured in audit logs
* 0 invalid Jolly reuses accepted by the system
* 0 games completed with structurally invalid placements or missing required data
* Public results and leaderboards reflect updates immediately after save/complete actions
* Organizers can run the full event without relying on Excel for live operations

# Future works

Good candidates for the next phase:

* player-level roster participation
* eligibility and roster-rule validation
* import/export for reuse across years
* scheduled datetime per game
* live 1v1 score entry
* advanced maxi-screen logic and rotation
* automatic ranking calculation from configured per-game ranking logic
* review notifications to admins after post-completion edits
* multi-year history, analytics, predictions
