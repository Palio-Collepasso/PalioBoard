# Edge cases

## Scoring and ranking

Two or more rioni tied in placement, for example `1,2,2,4`.

Invalid placements such as `1,2,2,3` must be rejected.

A rione marked as last due to delay or equivalent ruling should still be representable as a normal placement outcome. The regulation allows declassamento all’ultimo posto in delay scenarios. 

A standings tie in the final Palio ranking may need “more first places” as the deciding rule if you choose to expose winner logic in the app later, since that is the regulation’s rule for the final overall tie. 

## Jolly

A judge tries to set Jolly for a Prepalio or Giocasport game.

A judge tries to set Jolly twice for the same rione across two Palio games.

A judge forgets to set Jolly before a completed game and needs to correct the result afterward.

A Jolly game later goes under examination.

## Lifecycle

A completed game is edited by a judge and becomes pending admin review.

A game under examination is visible publicly but excluded from standings.

A game moves from under examination back to completed and must be re-included in standings.

A user tries to complete a game with missing required fields.

## 1v1

Semifinal pairings are missing but the tournament is started.

A 1v1 tournament has some winners entered but not all four matches.

An admin overrides the computed final ranking.

## Prepalio

Prepalio subgames are complete but the aggregate ranking ends in a tie under the configured strategy.

Admin manually overrides the aggregate final Prepalio ranking.

A Prepalio game is edited after completion and the Palio leaderboard must recompute because the Prepalio final ranking may change.

## Deletion and config safety

An admin attempts to delete a game with results.

An admin attempts to change a game definition after results exist.

A points table is changed after some games are already completed. Allow this only before any relevant result exists.

## Audit and trust

An admin reverts a judge’s edit using audit history.

Two judges edit the same completed game in quick succession.

A manual leaderboard adjustment is added and later reverted.
