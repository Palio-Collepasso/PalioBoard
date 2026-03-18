# Acceptance Scenarios

## Purpose
Turn product intent into business-facing, observable scenarios that are useful for thin slices and feature acceptance.

## Document boundary
This file owns **observable scenarios**.
It does **not** own:
- the full rule catalog — see `docs/domain/business-rules.md`
- automation cadence, fixture details, or test-layer policy — see `docs/testing/*`

Scenarios marked **[Must-pass E2E]** identify the small subset that should also stay visible in the browser-level protection set when the implementation is stable enough. Browser automation details still live in `docs/testing/critical-e2e-flows.md`.

Keep scenarios focused on observable behavior. When a source leaves room for interpretation, this document makes the smallest safe assumption and states it in a short note.

## Critical v1 scenarios

### `AS-001` — Complete a ranking game successfully **[Must-pass E2E]**
**Given** a ranking-format game is in progress and all four teams have final placements with all enabled required fields filled  
**When** a judge or admin completes the game  
**Then** the game becomes completed  
**And** the official result becomes visible in admin and public views  
**And** the affected standings update from that completed result

**Notes**
- Placements are entered manually in v1.
- Ties such as `1,2,2,4` are valid when structurally correct.

### `AS-002` — Block ranking-game completion when placements are invalid
**Given** a ranking-format game is in progress  
**And** at least one placement is missing, structurally invalid, or a required enabled field is missing  
**When** a judge or admin tries to complete the game  
**Then** completion is rejected with a clear error  
**And** the game remains in progress  
**And** standings do not change

### `AS-003` — Update public views after official result completion **[Must-pass E2E]**
**Given** a public user is viewing the relevant competition page  
**And** an official game result is completed or otherwise officially changed  
**When** that change is saved successfully  
**Then** the public results and standings reflect the new official state immediately  
**And** any provisional status that applies is shown

**Notes**
- Public reads are expected to show only committed official state.

### `AS-004` — Start a ranking game and initialize live draft correctly
**Given** a ranking-format game is still in draft  
**And** it already has the current official result state for its four teams  
**When** a judge or admin starts the game  
**Then** the game becomes in progress  
**And** the live entry screen is prefilled from the current official result state  
**And** standings do not change just because the game started

**Notes**
- The safe assumption is that "current official result state" may be empty or partial depending on prior official data, and the live draft mirrors that state rather than starting from a separate blank model.

### `AS-005` — Reject stale concurrent live-result writes **[Must-pass E2E]**
**Given** two judges are editing the same ranking-format game live  
**And** one judge has already saved a newer value for a field or team entry  
**When** the other judge tries to save a stale version  
**Then** the stale write is rejected with a clear conflict error  
**And** the latest server state is preserved  
**And** the user can refresh or resume from the latest state without a silent overwrite

### `AS-006` — Recover ranking live state after reconnect or restart
**Given** a ranking-format game is in progress and live updates were saved before a disconnect or backend restart  
**When** a judge reconnects and reopens that live game  
**Then** the latest saved in-progress state is restored  
**And** the user is informed when a conflict occurred  
**And** editing can continue from the restored server state

**Notes**
- After a backend restart, active field locks are not assumed to survive and must be reacquired.

### `AS-007` — Progress a 1v1 tournament and expose bracket progression **[Must-pass E2E]**
**Given** a fixed 4-team 1v1 tournament has valid semifinal pairings and is in progress  
**When** a judge or admin saves each match winner  
**Then** each saved winner becomes official immediately  
**And** the bracket progression becomes visible immediately  
**And** the resulting tournament ranking becomes visible as soon as it is derivable from the saved match outcomes

### `AS-008` — Complete a 1v1 tournament and update standings only at game completion **[Must-pass E2E]**
**Given** a fixed 4-team 1v1 tournament has all required match outcomes saved and a final ranking is derivable  
**When** a judge or admin completes the tournament game  
**Then** the tournament result counts in the leaderboard  
**And** the affected standings update at completion time  
**And** those standings were not updated earlier while the tournament was only in progress

### `AS-009` — Edit a completed result and move to pending admin review **[Must-pass E2E]**
**Given** a game is completed  
**When** a judge edits its official result  
**Then** the edited official result is saved and becomes the latest public result  
**And** the game moves to pending admin review  
**And** the edited result still counts in standings until an admin resolves the review

### `AS-010` — Mark a game under examination and exclude it from standings while keeping it visible
**Given** a game has an official result that is currently visible  
**When** a judge or admin marks the game under examination  
**Then** the latest official result remains visible publicly  
**And** the game is clearly labeled as under examination or provisional  
**And** the game is excluded from leaderboard calculations until resolved

## Important non-E2E scenarios

### `AS-011` — Apply Jolly correctly in Palio
**Given** a Palio game is being saved with a team marked as using Jolly for the first time  
**When** the result becomes official  
**Then** that team's points from that Palio game are doubled  
**And** the Jolly usage is visible in the official result and Jolly summary

**Notes**
- The sources say Jolly must be declared before the game, but in v1 it is recorded at result-entry time rather than through a separate pre-game workflow.
- Jolly is allowed only in Palio, never in Prepalio or Giocasport.

### `AS-012` — Reject Jolly reuse
**Given** a team has already used Jolly in another Palio game  
**When** a judge or admin tries to save Jolly for that same team again in a different Palio game  
**Then** the save is rejected with a clear reason  
**And** the second Jolly is not recorded  
**And** standings remain unchanged by the rejected attempt

### `AS-013` — Compute Prepalio aggregate ranking and feed the Palio standings
**Given** multiple Prepalio subgames have official results  
**When** the system recomputes the Prepalio competition  
**Then** it produces a Prepalio aggregate ranking from the subgame points  
**And** it maps that final Prepalio ranking to Prepalio award points  
**And** it adds those award points to the main Palio standings

**Notes**
- If the configured automatic tie strategy is not sufficient, admins can set the official final Prepalio placements manually.

### `AS-014` — Keep Giocasport standings separate
**Given** a Giocasport game result becomes official  
**When** standings are recomputed  
**Then** the Giocasport leaderboard reflects that result  
**And** the Palio leaderboard does not change because of that Giocasport result

### `AS-015` — Apply a manual standings adjustment with auditability
**Given** an admin enters a manual leaderboard adjustment with competition, team, signed point delta, and reason  
**When** the adjustment is saved  
**Then** the relevant competition standings update immediately  
**And** the adjustment remains traceable with author, timestamp, reason, and before/after history

### `AS-016` — Block game configuration changes after official result data exists
**Given** a game already has official result data  
**When** an admin tries to change result-affecting configuration such as competition, format, selected fields, points table, or other game relationships  
**Then** the change is rejected  
**And** the existing official result remains unchanged

**Notes**
- The safe assumption is that "official result data exists" includes 1v1 match outcomes that have already been saved officially, even if the overall tournament game is not yet completed.
