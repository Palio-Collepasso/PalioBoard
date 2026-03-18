# Future Considerations

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
