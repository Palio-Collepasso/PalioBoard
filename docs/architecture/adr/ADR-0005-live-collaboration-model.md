# ADR-0005 — Live Collaboration Model for Ranking Games

- Status: Accepted
- Date: 2026-03-11

## Context

Ranking-template games need reactive collaboration and partial live updates, while official audited result state must remain clean.

The system must support:

- field-level collaboration
- reconnect conflict handling
- restart recovery
- multiple games in progress
- public/maxi live views

## Decision

Use a memory-first live collaboration subsystem for ranking-template games only.

Key rules:

- live state is in memory first
- field-level leases are in memory first
- persisted provisional snapshots exist only for restart/reconnect recovery
- draft snapshots are not official business history
- draft snapshots are whole-game JSON blobs
- snapshots are scoped by `(game_id, live_cycle)`
- stale data from previous cycles is ignored
- when a game enters `in_progress`, draft is prefilled from current official `game_entries`
- when a game leaves `in_progress`, changed draft values materialize into official rows
- draft cleanup is best-effort and must not affect business correctness

Realtime split:

- admin live entry: WebSocket per `game_id`
- public/maxi live view: SSE per `game_id`
- full per-game snapshots with monotonic revision numbers

1v1 exception:

- 1v1 bypasses this live-draft subsystem in v1

## Consequences

### Positive

- Clean separation between provisional collaboration and official audited state.
- Good UX for live editing and reconnect recovery.
- Easy future replacement of in-memory state with Redis via adapter.

### Negative

- Extra complexity compared with pure direct-save editing.
- Requires careful restart hydration and stale-cycle handling.

## Follow-ups

- Keep `LiveGameStateStore` behind an adapter interface.
- Revisit Redis only when scale or operational need justifies it.
