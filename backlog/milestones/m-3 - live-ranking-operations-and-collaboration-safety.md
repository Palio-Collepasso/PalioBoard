---
id: m-3
title: "Live ranking operations and collaboration safety"
---
## Description

Milestone: Live ranking operations and collaboration safety

Depends on: m-2 Trusted ranking result backbone.

Objective: upgrade ranking games from final official entry only to the real event workflow, including game start, in-progress team-by-team editing, and protection against concurrent editors.

Scope:
- `draft -> in_progress -> completed` ranking-game flow.
- Memory-first live draft state with persisted recovery snapshots.
- Field leases, optimistic revision checks, stale-write rejection, and reconnect recovery.
- WebSocket or SSE realtime contracts for live ranking entry and live game reads.
- Materialization of changed draft values into official result rows when leaving `in_progress`.
- Best-effort draft cleanup with `live_cycle` invalidation semantics.
- Critical tests for concurrent live editing behavior.

Exit criteria:
- A ranking game can be explicitly started and edited live by authorized users.
- Concurrent editors cannot silently overwrite each other.
- Restart or reconnect restores the latest draft snapshot correctly.
- Leaving `in_progress` materializes only the official changes and keeps standings unchanged until completion.
- The live conflict and lease behavior is covered by integration or realtime tests plus the agreed E2E flow.
