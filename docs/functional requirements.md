# Functional requirements

## 1. Season setup

The system shall allow admins to create one season in the UI.

The system shall support exactly 4 teams for the season, prefilled with default rioni but editable before results exist.

The system shall allow admins to create games belonging to exactly one competition:

* Palio
* Prepalio
* Giocasport

The system shall allow admins to configure, per game:

* name
* competition
* template type
* enabled optional result fields
* custom label for the quantity-like field
* points table, with default `4,3,2,1`

The system shall prevent deletion of any game that already has recorded results.

The system shall prevent editing of a game definition after results exist.

## 2. Permissions

The system shall use capability-based authorization.

The system shall support at least these capabilities:

* manage season config
* manage tournament pairings
* start game
* complete game
* mark under examination
* resolve under examination
* enter and edit results
* set Jolly usage
* apply manual standings adjustments
* view audit log
* review post-completion edits

The system shall provide default role bundles:

* Admin
* Judge
* Public

## 3. Game templates

The system shall support exactly two templates in v1.

### Ranking template

The system shall always store placement for all 4 rioni.

The system shall optionally store:

* time
* quantity-like metric
* penalties
* public notes

The UI shall show the configured label, not a generic internal field name.

### 1v1 template

The system shall model a fixed 4-rione tournament:

* semifinal 1
* semifinal 2
* final 3rd/4th
* final 1st/2nd

The system shall allow admin/judge to set semifinal pairings before start.

The system shall derive the final ranking automatically from the four match winners.

The system shall allow admin manual override of the computed ranking.

## 4. Game lifecycle

The system shall support these states:

* not started
* in progress
* completed
* pending admin review
* under examination

The system shall move a game to in progress only via explicit Start game.

The system shall move a game from in progress to completed only through Complete game.

If a judge edits results after completion, the system shall automatically move the game to pending admin review.

A pending admin review game shall still count in the leaderboard using the latest saved result.

A game under examination shall remain visible publicly but shall not count in leaderboard calculations.

Judges and admins shall be allowed to mark a game under examination and resolve it.

Only admins shall be allowed to move pending admin review back to completed.

## 5. Result entry

For ranking-template games, the system shall support partial live saves while the game is in progress.

The system shall not update the leaderboard from partial in-progress data.

The system shall require manual placement entry in v1.

The system shall validate placements including ties such as `1,2,2,4`.

The system shall block completion unless:

* all 4 rioni have placements
* placements are structurally valid
* enabled required fields are filled

## 6. Scoring engine

The system shall compute points automatically from placement using the configured table.

The default table shall be `4,3,2,1`, which matches the regulation for Palio and Giocasport. 

The system shall support ex aequo scoring from explicitly entered placements. The regulation states that ties are ex aequo. 

The system shall support Jolly only for Palio games, never Prepalio or Giocasport.

The system shall allow per-rione Jolly selection at game time.

The system shall reject Jolly if that rione has already used it in another Palio game.

The system shall double the points of the affected Palio game result for that rione. 

The system shall provide a Jolly summary view.

## 7. Prepalio

The system shall treat Prepalio games as normal games within the Prepalio competition.

The system shall compute a Prepalio aggregate ranking from the points earned in Prepalio subgames.

The system shall then map that final Prepalio ranking to a points table, default `4,3,2,1`, and add it to the main Palio standings. This matches Art. 18. 

The system shall support configurable ranking strategy for Prepalio aggregate ties.

The system shall allow admin manual override of the final Prepalio ranking.

## 8. Giocasport

The system shall maintain a separate Giocasport leaderboard.

Giocasport results shall not affect the main Palio standings. 

## 9. Manual standings adjustments

The system shall let admins create a leaderboard adjustment:

* competition
* rione
* signed point delta
* reason
* timestamp
* author

These adjustments shall affect the official standings immediately.

## 10. Public and maxi-screen views

The public interface shall be accessible without login.

The public interface shall have separate sections for:

* Palio
* Prepalio
* Giocasport

The public interface shall show:

* standings
* results
* notes
* history
* provisional status where relevant

The system shall provide a separate maxi-screen mode in v1.

Advanced maxi-screen live logic remains deferred.

## 11. Audit

The system shall log every material change to:

* results
* game state
* Jolly usage
* standings adjustments
* ranking overrides
* tournament pairings

Each audit record shall include:

* actor
* timestamp
* entity type
* entity id
* before snapshot
* after snapshot
* optional reason