# Result Model and Invariants

## 15. Official result model, tournaments, and audit simplification
### 127. What is the canonical official result surface for a game?
**Decision:** `game_entries` is the single canonical official per-team result surface for every format. Keep nullable `placement` and `is_jolly = false` by default, and store extra configured values in `game_entry_fields`.

### 128. How are 1v1 tournaments represented in v1?
**Decision:** `tournament_matches` is the canonical operational record for bracket flow, while official per-team consequences still materialize into `game_entries`. This keeps downstream scoring and projections mostly format-agnostic.

### 129. Does 1v1 use the live-draft subsystem in v1?
**Decision:** No. In v1, 1v1 bypasses live draft entirely: each match outcome is written and audited immediately, and only future richer match scoring would justify draft handling there.

### 130. When do 1v1 games affect the leaderboard?
**Decision:** Official match outcomes update tournament progress immediately, but the leaderboard is recomputed only when the whole tournament/game is completed. This avoids partial bracket progress leaking into standings.

### 131. Do we need separate `computed_rankings` / `ranking_overrides` tables?
**Decision:** No. Store the current official placement directly on `game_entries` and rely on the append-only audit log to explain whether a value came from automatic computation or a later manual override.

### 132. What shape should the audit log have after this simplification?
**Decision:** Keep one generic append-only audit table, write one row per changed business entity, and link related rows with a shared correlation id. Projection and read-model churn stays out of audit.

## 16. Official metrics, field catalog, and game immutability
### 133. How should official result metrics be modeled?
**Decision:** Keep the current ER direction: `game_entries` stores canonical official placement and Jolly, while `game_entry_fields` stores the typed extra values linked through the seeded field catalog.

### 134. Is the field catalog runtime-managed in v1?
**Decision:** No. The field catalog is seeded/static in v1; admins only choose which catalog fields a game uses. This keeps labels, types, and meaning stable across the season.

### 135. Can a game’s field configuration change after official result data exists?
**Decision:** No. Once a game has official result data, its `game_fields` configuration becomes immutable to preserve the meaning of saved `game_entry_fields` and audits.

### 136. Can a game’s points table change after official result data exists?
**Decision:** No. Points-table configuration also becomes immutable once official result data exists, so scoring semantics do not silently change under recomputation.

### 137. Can any other game property or relationship still change after official result data exists?
**Decision:** No. The final rule is stronger: every game property and relationship becomes immutable once the game has official result data.
