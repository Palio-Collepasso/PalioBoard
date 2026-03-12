---
id: m-5
title: "1v1 tournament workflow"
---
## Description

Milestone: 1v1 tournament workflow

Depends on: m-2 Trusted ranking result backbone and m-4 Advanced standings rules: Jolly, Prepalio, Giocasport, adjustments.

Objective: deliver the second game template end to end by managing semifinal pairings, recording match winners, exposing bracket progression, deriving the final ranking, and applying leaderboard impact only on completion.

Scope:
- Fixed four-team 1v1 tournament model.
- Pairing configuration before start.
- Match outcome entry for semifinals and finals.
- Immediate bracket progression updates.
- Automatic final ranking derivation from winners.
- Admin override of final official placements where needed.
- Materialization into the canonical official result surface.
- Leaderboard recompute only when the tournament or game is completed.
- Critical E2E flow for tournament progression and completion.

Exit criteria:
- Authorized users can set pairings and record winners.
- Bracket progression becomes visible immediately after each official match update.
- Final ranking is derived correctly and can be overridden by admin when necessary.
- The tournament affects standings only after game completion.
- Tournament workflow is covered by integration tests and the must-pass E2E slice.
