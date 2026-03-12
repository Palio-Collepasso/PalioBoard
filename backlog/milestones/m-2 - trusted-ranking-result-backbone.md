---
id: m-2
title: "Trusted ranking result backbone"
---
## Description

Milestone: Trusted ranking result backbone

Depends on: m-1 Identity, authorization, and season setup.

Objective: deliver the first truly valuable end-to-end slice by recording an official ranking-game result, validating it, auditing it, recomputing standings, and exposing updated public reads.

Scope:
- Canonical official result persistence through `game_entries` and `game_entry_fields`.
- Ranking-game completion workflow for authoritative saves.
- Placement validation, required-field validation, and tie support such as `1,2,2,4`.
- Core points calculation from configured tables.
- Synchronous projection recompute for standings and related current read models.
- Audit logging for authoritative changes.
- Initial public read endpoints and pages for standings, results, and history.
- First critical E2E flow to complete a ranking game and verify the public update.

Exit criteria:
- A judge or admin can complete a ranking game with a structurally valid result.
- Invalid placements or missing required fields are blocked.
- Official writes, audit, and projection recompute succeed or fail atomically.
- Public pages show the updated official result and standings after completion.
- The critical ranking completion flow is covered by unit, integration, and E2E tests at the right depth.
