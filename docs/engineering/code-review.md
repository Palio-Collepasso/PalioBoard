# Code review guide

This review guide keeps human and agent review focused on PalioBoard's highest-risk failure modes.

## Review checklist for every PR
- The scope matches the stated purpose.
- The change follows the nearest `AGENTS.md` instructions.
- The right tests exist at the right layer.
- The PR updates docs and contracts when their truth changed.
- No unrelated refactor is mixed into a risky change.
- Any unresolved ambiguity is called out explicitly.

## Critical-path review checklists

### 1. Official results and canonical materialization
Check that:
- canonical per-team result truth remains the source of truth
- placement, Jolly, and configured fields are written consistently
- completed, pending review, and under-examination semantics still match the product rules
- audit coverage remains correct for authoritative changes

### 2. Standings, scoring, Prepalio, and projections
Check that:
- standings are recomputed from authoritative truth only
- Jolly is allowed only where the domain rules allow it
- Prepalio and Giocasport behavior remains isolated correctly
- read models reflect official state, not transient client or draft state

### 3. Tournament progression
Check that:
- semifinal/final progression remains deterministic and correct
- canonical official team results stay synchronized with match outcomes
- leaderboard recomputation timing still matches the requirements

### 4. Live ranking entry and collaboration
Check that:
- in-progress draft behavior never becomes official truth by accident
- stale writes and conflicts are rejected clearly
- reconnect and recovery semantics remain safe
- live state is cleared or materialized at the correct lifecycle transitions

### 5. Authorization and identity
Check that:
- the api remains the authorization source of truth
- capabilities are enforced on the relevant actions
- no frontend-only gate is relied on for protection
- default role / user workflows stay constrained as intended

### 6. Migrations and schema changes
Check that:
- the migration is reversible or at least operationally safe
- the schema change matches the domain model and docs
- integration tests cover the changed DB-backed behavior
- data backfills are idempotent and not embedded in normal request logic

### 7. Infra, CI, and workflows
Check that:
- permissions remain least-privilege
- no deploy shortcut weakens protected-branch expectations
- secrets handling and release behavior did not change accidentally