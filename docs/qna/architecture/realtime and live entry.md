# Realtime and Live Entry

## 5. Concurrency, leases, live entry, and optimistic locking
### 39. What consistency model is used for live editing?
**Decision:** A hybrid model is used: soft locking plus optimistic concurrency.

### 40. What form do locks take?
**Decision:** Locks are **field-level time-based leases**, not whole-game locks. A field remains leased while the user is actively typing plus a fixed timeout. If the lease expires, another editor can take control.

### 41. What happens on reconnect after conflict?
**Decision:** On reconnect, if the offline/local client state conflicts with the now-authoritative online state, the user is informed of the conflict, encouraged to copy their unsaved value if needed, and the field is restored to the current server state.

### 42. How is optimistic concurrency modeled?
**Decision:** Optimistic concurrency uses explicit integer version fields with a **two-level model**:
- a game aggregate version for lifecycle/state-changing commands
- a live-entry version for reactive draft/result editing

### 43. Where do leases live?
**Decision:** Field leases are stored in a dedicated database-backed lease table keyed by game and field, with holder, token, and expiration metadata.

### 44. What is the source of truth for time?
**Decision:** The api/database clock is authoritative for all business and collaboration timing, including lease expiry.

### 45. How are live drafts modeled in the final design?
**Decision:** Live-game state is **memory-first**. Active draft values, leases, connected editors, and live revision counters live in api memory first. Persisted draft snapshots exist separately for restart recovery, but live collaboration is driven from memory.

### 46. Are live draft snapshots part of official audited business history?
**Decision:** No. Persisted draft snapshots are stored in a dedicated provisional draft area/table/module, clearly separate from official business state and audit history.

### 47. When are draft snapshots persisted?
**Decision:** On three triggers:
- periodically while editing (coarse cadence, not keystroke-level)
- when a field lease ends
- as a best-effort flush when the user leaves/closes the game

### 48. How is live state restored after api restart?
**Decision:** On restart, the api reloads the persisted provisional draft snapshots into memory. That hydrated in-memory state becomes the new live draft state, and reconnecting clients receive it.

### 49. Can multiple games be in progress simultaneously?
**Decision:** Yes. The architecture must support multiple in-progress games at once, especially for Prepalio scenarios.


## 6. Realtime architecture
### 50. Which transport is used for which interaction?
**Decision:**
- standard admin screens: polling where acceptable
- public/maxi-screen live updates: SSE
- admin live-entry collaboration: WebSockets

### 51. How are realtime channels scoped?
**Decision:** Realtime is scoped **per game**. There is one logical live collaboration/read stream per `game_id`, not a global current-game channel.

### 52. Is there special api business logic for maxi-screen selection?
**Decision:** No. Maxi-screen pages are normal Angular pages designed for projector usage. There is no special api “featured game” business state. A user with the frontend-only maxi-screen shortcut can simply open the page for a specific game.

### 53. Is the maxi-screen route protected by api authorization?
**Decision:** No. Maxi-screen is a public route. The related capability exists only so the frontend can show or hide a shortcut/button.

### 54. What is sent over realtime channels?
**Decision:** Full per-game live snapshots, not fine-grained patches/deltas.

### 55. How are out-of-order messages handled?
**Decision:** Every live-game snapshot carries a server-generated monotonic revision number for that game. Clients ignore duplicate or stale snapshots.

### 56. Is the live revision persisted?
**Decision:** Yes. The latest live revision is persisted alongside draft snapshots so ordering continuity survives restart recovery.

### 57. How are live-game concerns abstracted?
**Decision:** The live collaboration layer sits behind an explicit `LiveGameStateStore`-style adapter. v1 uses an in-memory implementation; Redis remains a future-compatible replacement path.

### 58. How are WebSockets authorized?
**Decision:** Capabilities are checked at connection time. Per-action checks enforce domain rules such as lease ownership, version matching, valid state, and field validity.

### 59. Does realtime drive business correctness?
**Decision:** No. The database and projections remain the source of truth for business state. Realtime only delivers post-commit or live-collaboration updates to clients.


## 9. Database, migrations, and schema management
### 78. Are provisional draft snapshots stored in the same database?
**Decision:** The current direction is to store all persistent app data, including provisional draft snapshots, in the same Postgres database under clearly separated tables/modules. The final storage-table naming/details were still being discussed when this log was requested.


## 13. Runtime consistency, persistence conventions, and contracts
### 113. Where do active field leases live in the final design?
**Decision:** In the final live-draft design, active field leases are an **in-memory concern**, not durable business state. They must be reacquired after restart, which keeps the recovery model simpler and aligned with a future Redis-backed live-state adapter.

### 114. How are provisional live drafts persisted?
**Decision:** Persist **whole-game JSON draft blobs** keyed by game identity, together with revision metadata. This mirrors the memory-first live state much better than normalizing per-field draft rows.

### 115. How should live draft hydration behave across implementations?
**Decision:** Treat hydration strategy as an infrastructure detail behind the `LiveGameStateStore` adapter. In v1 it can lazy-hydrate from persisted snapshots on first access; a future Redis implementation can choose a different policy without changing business logic.

### 116. Where should provisional draft snapshots be stored in v1?
**Decision:** In the same Postgres database as the rest of the app, but in tables clearly separated from official business state. That keeps the system simple while still distinguishing recovery data from canonical data.

## 14. Live draft lifecycle and recovery
### 123. What happens if draft deletion fails when a game leaves `in_progress`?
**Decision:** Draft cleanup must not affect the business transaction. Introduce a technical `live_cycle` counter on the game so stale draft data from previous cycles becomes ignorable instead of dangerous.

### 124. When a game re-enters `in_progress`, how is the new live draft initialized?
**Decision:** Prefill it from the current official `game_entries`. That gives operators continuity and makes subsequent edits start from the already-official state rather than from an empty draft.

### 125. When leaving `in_progress`, should the system rewrite all official entries or only changed ones?
**Decision:** Only changed ones. Compare the draft with the current official state, then write and audit only the `game_entries` that actually changed.

### 126. How should live pages bootstrap their state?
**Decision:** Use an initial HTTP fetch followed by realtime subscription. Realtime keeps the page fresh, but it should not be responsible for delivering the first correct state.
