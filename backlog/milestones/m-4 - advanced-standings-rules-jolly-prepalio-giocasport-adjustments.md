---
id: m-4
title: "Advanced standings rules: Jolly, Prepalio, Giocasport, adjustments"
---
## Description

Milestone: Advanced standings rules: Jolly, Prepalio, Giocasport, adjustments

Depends on: m-2 Trusted ranking result backbone.

Objective: complete the scoring rules that make the product faithful to the actual event instead of just a generic standings tracker.

Scope:
- Jolly validation and application for Palio only.
- Single-use-per-team Jolly enforcement and a Jolly summary view.
- Separate Giocasport leaderboard.
- Prepalio subgame accumulation, aggregate ranking, and roll-up into the main Palio standings.
- Configurable Prepalio tie strategy and admin override for final Prepalio ranking when needed.
- Manual leaderboard adjustments with required reason and audit.
- Projection updates and read models for all affected competition contexts.

Exit criteria:
- Jolly is accepted only where valid and rejected where forbidden or already used.
- Giocasport remains separate from Palio standings in every tested case.
- Prepalio subgames roll up into a final Prepalio ranking and then into Palio correctly.
- Manual adjustments change official standings immediately and are audited.
- Calculation rules are covered by focused unit tests plus integration tests for projection updates.
