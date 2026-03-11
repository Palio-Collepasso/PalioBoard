# PalioBoard — discovery Q&A summary

This document consolidates the interview into a structured Q&A, using the **final clarified decisions** rather than earlier intermediate answers. It is aligned with the Palio regulation and description, especially around the 4-team structure, `4-3-2-1` scoring, Jolly, Prepalio, Giocasport, and the 15-minute appeal window.

---

## v1 — questions and improved answers

### 1) Who is the main user we should optimize for?
**Answer:** The product is primarily for **admins and judges**. The **public audience** is a secondary user and should access a read-only experience for schedules, results, rankings, and history.

### 2) What is the biggest pain today?
**Answer:** The biggest pain is **fast result entry during the event**. Excel already helps with ranking totals, but it does not handle well the operational flow of recording game results quickly and clearly. Secondary pains, but lower-priority for v1, are **tournament bracket management** and **player eligibility checks**, which are currently handled manually.

### 3) What must the system record for games in v1?
**Answer:** In v1 the app records results at **team level**, not player level. It must capture whatever is needed to determine the winner and standings:
- **placement** (most important)
- **time**, when relevant
- **quantity / score / points** as one configurable result field with a game-specific UI label
- **penalties**, when relevant
- **public notes**

### 4) How should games be modeled?
**Answer:** v1 uses only **two templates**:
1. **Ranking format** with optional fields (placement plus any needed time / quantity / penalties / notes)
2. **1v1 tournament format**

This avoids building a generic form builder.

### 5) Should points be computed automatically or entered manually?
**Answer:** Points must be **computed automatically**. The system must handle:
- placement-to-points mapping
- ties/ex aequo
- Jolly
- Prepalio roll-up into the main Palio leaderboard

Configuration should live in the **web app / database**, not in hardcoded values.

### 6) Should results become public immediately?
**Answer:** Yes. A saved result should be **visible immediately**, because visibility is essential for the 15-minute appeal window.

### 7) Who can change data after publication?
**Answer:** Distinguish between **game definition changes** and **result changes**:
- **Game definition** (name, format, enabled fields, etc.) can be changed **only by admins**, and only until results exist.
- **Results** can be entered and edited by judges.
- Every result change must be **fully audited**.

### 8) What devices will judges use?
**Answer:** Judges are expected to use **laptops**.

### 9) Which result-entry model should the product support first?
**Answer:** The app must support **all games**, but in v1 it records them through the two fixed templates. For ranking-based games, player-level participation is deferred.

### 10) Can we assume a fixed 1v1 tournament structure?
**Answer:** Yes. A 1v1 tournament is always:
- semifinal
- final for 3rd/4th
- final for 1st/2nd

This is not only a v1 assumption, but a general modeling rule.

### 11) Should Giocasport be included in v1?
**Answer:** Yes. **Giocasport** is a separate competition for children, with its own games and its own leaderboard.

### 12) Who can configure the season?
**Answer:** **Admins only.**

### 13) How should Jolly work?
**Answer:** Jolly is **not pre-assigned** during season setup. Each team decides **shortly before a Palio game** whether to use it and communicates that choice to the judges. Then the judge/admin records it inside the game result flow.

The system must:
- allow a **per-team Jolly flag** on Palio games
- ensure a team **cannot use Jolly more than once**
- block invalid reuse and show an error
- provide a **Jolly summary page** by team and game

### 14) What counts as the moment a game starts?
**Answer:** A game starts only when a judge/admin explicitly clicks **Start game**.

### 15) Should the system compute placements automatically from metrics?
**Answer:** No. In v1, judges must **enter final placements manually**. Automatic ranking logic is postponed.

### 16) How should ties be entered?
**Answer:** Judges should enter placements explicitly, for example:
- `1,2,2,4`

The system validates the structure and computes points accordingly.

### 17) Can judges save partial results while a game is running?
**Answer:** Yes. Judges can save **in-progress partial data** that is publicly visible, but the main leaderboard updates only when the game is marked **Completed**.

### 18) How should user accounts work?
**Answer:** The product should be designed for **individual accounts** for admins and judges. In practice, admins may do most of the work, judges may share usage patterns, or judges may not always use the software directly, but the model should still support individual identities and auditability.

### 19) Does v1 depend on local hosting or cloud hosting?
**Answer:** No strong product dependency was requested. v1 can be **deployment-agnostic**.

### 20) Does v1 need game order or scheduled datetime?
**Answer:** No. In v1, **order does not matter** and games do not need a scheduled datetime.

### 21) How is the season created each year?
**Answer:** In v1, admins create and manage the season **manually in the UI**. They can:
- add games
- edit games
- remove games

A game with results cannot be deleted.

### 22) How should games be classified?
**Answer:** Every game belongs to exactly one competition type:
- **Palio**
- **Prepalio**
- **Giocasport**

### 23) Should admins be able to adjust standings manually?
**Answer:** Yes. Admins need a way to apply **manual leaderboard adjustments** outside normal game results, with a reason and audit trail.

### 24) What should the public see when a game is under examination?
**Answer:** The public should see:
- the game
- the latest entered result
- a clear **under examination / provisional** status

That game must be **excluded from leaderboard calculation** until it returns to Completed.

### 25) What can admins configure per game?
**Answer:** For each game, admins can configure:
- game name
- competition type: Palio / Prepalio / Giocasport
- game format: ranking or 1v1
- enabled optional result fields: time / quantity / penalties / notes
- custom UI label for the quantity-like field

No separate “contributes to leaderboard” flag is needed, because contribution is implied by competition type.

### 26) Can a game with results be deleted?
**Answer:** No. A game with recorded results **cannot be deleted at all**.

### 27) What happens if a judge edits a completed game?
**Answer:** Editing a completed game result creates a distinct state: **pending admin review** (better naming can still be chosen). This is different from **under examination**, which is for appeals or disputes requiring a judge decision.

### 28) Does pending admin review still affect standings?
**Answer:** Yes. While in **pending admin review**, the game behaves like **completed** for standings and public visibility. The latest judge edit is shown publicly; the status is there to signal admins to review or revert the change through the audit trail.

### 29) How is the 1v1 final ranking produced?
**Answer:** The system should **derive the final ranking automatically** from the four match outcomes.

### 30) How are 1v1 semifinal pairings defined?
**Answer:** Pairings are **not part of season setup**. They are an operational action performed shortly before the tournament, usually after a random extraction. This should be handled via a dedicated permission/capability, not by broad season-setup rights.

### 31) How should points tables be configured?
**Answer:** Points tables should be configurable **per game / competition item**, with sensible defaults.

### 32) What are the default points tables?
**Answer:** Default values are:
- **Palio game:** `4,3,2,1`
- **Giocasport game:** `4,3,2,1`
- **Prepalio final ranking:** `4,3,2,1`

### 33) How is the final Prepalio ranking produced?
**Answer:** It is **computed automatically** from the points earned in the Prepalio subgames.

### 34) How should ties in the final Prepalio ranking work?
**Answer:** The tie-break strategy should be **configurable**, because it may change year by year. The product should not hardcode a single rule. It should support cases where the final ranking remains tied or follows another yearly strategy.

### 35) Can admins override automatic rankings?
**Answer:** Yes. For **every automatically computed ranking**, admins must be able to apply a **manual override**. The system should retain both the computed version and the official overridden one, with audit history.

### 36) How should teams be created?
**Answer:** Each year, admins can **create/edit the 4 teams**, but the system should prefill them with default values.

### 37) Do normal games always involve all 4 teams?
**Answer:** Yes. In v1, normal games always include **all four teams**.

### 38) When is a game allowed to be completed?
**Answer:** The system must block **Complete game** until the result is structurally valid, meaning:
- all 4 teams have placements
- placements form a valid ranking pattern
- all enabled required fields are filled

### 39) What permission model should the app use?
**Answer:** The app should use **capability-based authorization**. Roles are just a convenient way to assign bundles of capabilities.

### 40) What capability set is needed in v1?
**Answer:** The capability set should include:
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
- review post-completion edits and move pending admin review back to completed

### 41) Who can mark a game under examination and resolve it?
**Answer:** **Judges and admins** can do both.

### 42) What is the result-entry style for ranking games?
**Answer:** Ranking-format games need **live, team-by-team entry** while the game is running. Judges save partial values as each team performs, then assign final placements at the end.

### 43) Are notes internal or public?
**Answer:** Notes are **public**.

### 44) Does the public view require login?
**Answer:** No. The public view should be **accessible without login**.

### 45) How should Palio, Prepalio, and Giocasport be shown to users?
**Answer:** They should be shown as **three clearly separate sections/views**, not mixed together in one combined homepage.

### 46) What default role bundles should exist on top of capabilities?
**Answer:** Default bundles are:
- **Admin**: all capabilities
- **Judge**: operational capabilities (results, states, Jolly, pairings, etc.)
- **Public**: no login, read-only

### 47) What should the maxi-screen be in v1?
**Answer:** v1 should include a **separate maxi-screen mode**, but without advanced live rotation / live-score logic.

---

## >v1 — questions and improved answers

### 1) Should the system manage player-level participation and player identities inside each game?
**Answer:** Yes, but **after v1**. v1 stays at team level. Later versions can record which players took part in each game and support richer player-based history.

### 2) Should the app validate player eligibility and roster rules?
**Answer:** Yes, but **after v1**. Eligibility checks are currently manual and are important, but not the first priority.

### 3) Should tournament handling become more advanced than simple winner tracking?
**Answer:** Yes, but **after v1**. v1 handles the fixed 4-team tournament flow and derives rankings automatically. Later versions can support more advanced tournament reasoning.

### 4) Should there be a review mode that suspends leaderboard impact during result discussion?
**Answer:** Yes. In a later version, judges should be able to mark a game as being in a **review mode / disputed mode**, where the whole game is effectively suspended from the leaderboard while a decision is pending.

### 5) Should the system notify admins when someone edits a completed result?
**Answer:** Yes. In a later version, the app should **notify admins** whenever a judge edits a completed game.

### 6) Should games support scheduled datetime?
**Answer:** Yes, but **after v1**. A game should eventually support an optional **scheduled datetime**, and games can then be shown according to that schedule.

### 7) Should the system compute placements automatically from game metrics?
**Answer:** Yes, but **after v1**. This requires configuring the ranking logic per game.

### 8) Should season data be importable/exportable between years?
**Answer:** Yes, but **after v1**. Import/export would let the organizer reuse last year’s games and adjust what changed.

### 9) Should ranking games support more advanced live/public display logic on the maxi-screen?
**Answer:** Yes, but **after v1**. During a live game, the desired future behavior is to show the team currently playing with its current score/penalties/other metrics, plus a small provisional ranking. When no game is running, the maxi-screen should rotate between leaderboard, current game, and recent results.

### 10) Should 1v1 matches support live score entry?
**Answer:** Yes, but **after v1**. v1 only records the winner of each match. Later versions should support **real-time 1v1 scoring** (for football, tennis, volleyball, etc.).

### 11) Should the app eventually support multiple years in the same database and long-term statistics?
**Answer:** Yes, but **well after v1**. The current database should store only **one year**. Multi-year history, statistics, predictions, and similar features belong to a later phase.

### 12) Should priorities inside >v1 already be fixed now?
**Answer:** No. The user prefers to decide the ordering of >v1 work later, rather than labeling it today as v2 / v3.

---

## Brief list of open questions

1. **Public wording for special states**
   - Final labels for the public-facing statuses are still open, especially the best name for “pending admin review”.

2. **Prepalio tie strategy per season**
   - The app should support a configurable strategy, but the exact yearly strategy still has to be chosen when setting up a season.

3. **Authentication details**
   - The permission model is clear, but the login approach (local accounts, password reset flow, first-user bootstrap, etc.) is still open.

4. **Exact v1 screen list and navigation**
   - The core flows are defined, but the exact screen map for admin, judge, public, and maxi-screen still needs to be formalized.

5. **Operational defaults for capability bundles**
   - Default Admin/Judge/Public bundles are defined, but the exact real-world assignment process for event staff is still open.

6. **Data migration from Excel**
   - Import/export is >v1, but there is still an open operational question about whether any one-time migration from the existing spreadsheets is needed before the first live season.
