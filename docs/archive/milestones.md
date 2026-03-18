# Milestones

## m-0 — Delivery foundation and architecture skeleton

**Depends on:** none

**Objective**

Establish the project skeleton, delivery rails, and architectural guardrails so every later slice is built on the approved baseline rather than on throwaway scaffolding.

**Scope**

- Monorepo structure for `apps/api/`, `apps/web/`, `infra/`, `docs/`, and top-level tooling.
- FastAPI app skeleton with modular-monolith boundaries and per-module facades.
- Angular SPA skeleton with three shells: admin, public, maxi-screen.
- PostgreSQL, Alembic, and baseline migrations.
- Docker Compose, Nginx, health/version endpoints, env-based config.
- CI, pre-commit, lint/format/typecheck/test commands, OpenAPI export/generation workflow.
- Test harnesses for api unit/integration tests, frontend tests, and Playwright smoke setup.

**Exit criteria**

- The whole stack boots locally from documented commands.
- CI runs and enforces the agreed baseline checks.
- A baseline migration creates the empty schema successfully.
- Api/frontend shells are reachable and wired through the same-origin proxy.
- Architectural guardrails are in place enough to prevent obvious boundary violations.

**Risks**

- Spending too long on infrastructure before delivering business value.
- Encoding the wrong boundaries too early and paying refactor cost later.
- Letting “temporary” shortcuts become permanent.

**Why it should come before the others**

Every other milestone depends on stable repo structure, migrations, delivery commands, and boundary enforcement. Without this, later vertical slices either slow down or silently drift away from the approved architecture.

---

## m-1 — Identity, authorization, and season setup

**Depends on:** m-0

**Objective**

Make the application configurable and safe to access so admins can prepare a season and the system has the correct authorization vocabulary before any official result workflow exists.

**Scope**

- Supabase Auth integration at the api boundary.
- Application users, seeded roles, seeded capabilities, and policy checks.
- Minimal superadmin-only user provisioning flow.
- One-season setup flow in the UI.
- Team management for the four default rioni.
- Competition and game configuration.
- Static field-catalog selection per game.
- Per-game points-table configuration.
- Immutability/deletion guards on result-affecting setup, with tests.

**Exit criteria**

- A superadmin can create a user with one seeded role.
- Admin and judge access is enforced by api policy, not only by UI hiding.
- An admin can configure the season, teams, games, selected fields, and points tables from the UI.
- Attempts to perform unauthorized actions are rejected with structured errors.
- Setup immutability rules are implemented and covered by tests.

**Risks**

- Permission sprawl if capability checks are implemented inconsistently.
- Setup UX becoming too broad too early.
- Coupling the app too tightly to provider-specific auth details.

**Why it should come before the others**

Result entry is meaningless until there are users, permissions, teams, games, fields, and points configured. This milestone also locks in the capability model before operational flows begin to depend on it.

---

## m-2 — Trusted ranking result backbone

**Depends on:** m-1

**Objective**

Deliver the first truly valuable end-to-end slice: record an official ranking-game result, validate it, audit it, recompute standings, and expose updated public reads.

**Scope**

- Canonical official result persistence through `game_entries` and `game_entry_fields`.
- Ranking-game completion workflow for authoritative saves.
- Placement validation, required-field validation, and tie support such as `1,2,2,4`.
- Core points calculation from configured tables.
- Synchronous projection recompute for standings and related current read models.
- Audit logging for authoritative changes.
- Initial public read endpoints/pages for standings, results, and history.
- First critical E2E: complete a ranking game and verify public update.

**Exit criteria**

- A judge/admin can complete a ranking game with a structurally valid result.
- Invalid placements or missing required fields are blocked.
- Official writes, audit, and projection recompute succeed or fail atomically.
- Public pages show the updated official result and standings after completion.
- The critical ranking completion flow is covered by unit, integration, and E2E tests at the right depth.

**Risks**

- Incorrect standings logic damaging trust early.
- Letting projection tables or UI logic become accidental sources of truth.
- Underestimating audit requirements and needing invasive rework later.

**Why it should come before the others**

This is the smallest milestone that proves the core product promise: trusted official results with automatic standings and immediate visibility. It also validates the write model that later milestones reuse.

---

## m-3 — Live ranking operations and collaboration safety

**Depends on:** m-2

**Objective**

Upgrade ranking games from “enter final official result” to the real event workflow: start game, edit team-by-team while in progress, and protect concurrent editors.

**Scope**

- `draft -> in_progress -> completed` ranking-game flow.
- Memory-first live draft state with persisted recovery snapshots.
- Field leases, optimistic revision checks, stale-write rejection, and reconnect recovery.
- WebSocket/SSE realtime contracts for live ranking entry and live game reads.
- Materialization of changed draft values into official result rows when leaving `in_progress`.
- Best-effort draft cleanup with `live_cycle` invalidation semantics.
- Critical tests for concurrent live editing behavior.

**Exit criteria**

- A ranking game can be explicitly started and edited live by authorized users.
- Concurrent editors cannot silently overwrite each other.
- Restart/reconnect restores the latest draft snapshot correctly.
- Leaving `in_progress` materializes only the official changes and keeps standings unchanged until completion.
- The live conflict/lease behavior is covered by integration or realtime tests, plus the agreed E2E flow.

**Risks**

- Realtime complexity overwhelming the otherwise simple architecture.
- Confusing provisional draft state with official truth.
- Hard-to-reproduce concurrency bugs surfacing only late.

**Why it should come before the others**

Live ranking entry is one of the highest-risk and highest-value v1 workflows. It should be built on top of the already-proven official result backbone, not in parallel with it.

---

## m-4 — Advanced standings rules: Jolly, Prepalio, Giocasport, adjustments

**Depends on:** m-2

**Objective**

Complete the scoring rules that make the product faithful to the actual event instead of just a generic standings tracker.

**Scope**

- Jolly validation and application for Palio only.
- Jolly single-use-per-team enforcement and Jolly summary view.
- Separate Giocasport leaderboard.
- Prepalio subgame accumulation, aggregate ranking, and roll-up into the main Palio standings.
- Configurable Prepalio tie strategy and admin override for final Prepalio ranking when needed.
- Manual leaderboard adjustments with required reason and audit.
- Projection updates and read models for all affected competition contexts.

**Exit criteria**

- Jolly is accepted only where valid and rejected where forbidden or already used.
- Giocasport remains separate from Palio standings in every tested case.
- Prepalio subgames roll up into a final Prepalio ranking and then into Palio correctly.
- Manual adjustments change official standings immediately and are audited.
- Calculation rules are covered by focused unit tests plus integration tests for projection updates.

**Risks**

- Subtle scoring bugs across competition contexts.
- Prepalio tie handling becoming more complex than expected.
- Rule interactions making projections harder to reason about.

**Why it should come before the others**

These rules are central to business correctness and directly affect trust in the leaderboard. They should be stable before the specialized tournament workflow and before final public polish.

---

## m-5 — 1v1 tournament workflow

**Depends on:** m-2 and m-4

**Objective**

Deliver the second game template end to end: manage semifinal pairings, record match winners, expose bracket progression, derive final ranking, and apply leaderboard impact only on completion.

**Scope**

- Fixed four-team 1v1 tournament model.
- Pairing configuration before start.
- Match outcome entry for semifinals and finals.
- Immediate bracket progression updates.
- Automatic final ranking derivation from winners.
- Admin override of final official placements where needed.
- Materialization into the canonical official result surface.
- Leaderboard recompute only when the tournament/game is completed.
- Critical E2E flow for tournament progression and completion.

**Exit criteria**

- Authorized users can set pairings and record winners.
- Bracket progression becomes visible immediately after each official match update.
- Final ranking is derived correctly and can be overridden by admin when necessary.
- The tournament affects standings only after game completion.
- Tournament workflow is covered by integration tests and the must-pass E2E slice.

**Risks**

- Tournament-specific rules leaking into the generic ranking flow.
- Confusion between bracket-operational state and canonical official result truth.
- Edge cases around override behavior and completion timing.

**Why it should come before the others**

Tournament support is a distinct template, but still depends on the already-stable scoring, projection, and authorization backbone. It is important for v1, but less foundational than ranking-game correctness.

---

## m-6 — Trust and exception workflows

**Depends on:** m-2, m-3, m-4, and m-5

**Objective**

Complete the workflows that protect operational trust during the appeal window and after corrections: under examination, post-completion edits, admin review, and audit visibility.

**Scope**

- `completed -> pending_admin_review` flow on judge edits.
- Admin review and resolution back to `completed`.
- Marking and resolving `under_examination`.
- Projection rules where `pending_admin_review` still counts and `under_examination` does not.
- Audit browsing/read models for operational review.
- Structured reason capture where required.
- Critical E2E for post-completion edit and review behavior.

**Exit criteria**

- Editing a completed result creates a new authoritative write, records audit, and moves the game to `pending_admin_review`.
- `under_examination` keeps the result visible publicly while excluding it from standings.
- Admins can resolve review/examination flows correctly.
- Audit history is sufficient to understand what changed, by whom, and why.
- The exception workflows pass their dedicated integration and E2E tests.

**Risks**

- State-machine bugs causing standings to count the wrong results.
- Public confusion if provisional states are not expressed clearly.
- Revert/confirm workflows becoming destructive instead of append-only.

**Why it should come before the others**

These flows are required for the real event, but they depend on all primary result-entry paths already working. They should be added only after the normal workflows are stable enough to make exception handling precise.

---

## m-7 — Public/maxi completion and release hardening

**Depends on:** m-2, m-3, m-4, m-5, m-6

**Objective**

Turn the implemented core into a shippable v1 by completing read-only experiences, tightening observability and operations, and passing the full acceptance bar.

**Scope**

- Complete public sections for Palio, Prepalio, and Giocasport.
- Dedicated maxi-screen route/layout for v1.
- Public history/results/notes/provisional-state presentation.
- Final OpenAPI stabilization and frontend type generation workflow.
- Production deployment scripts, migration runbook, backups/logging checks, and readiness verification.
- Final pass on error envelopes, UX recovery messages, and non-happy-path behavior.
- Full regression run over all critical E2E flows.

**Exit criteria**

- Public users can see standings, results, notes, history, and provisional states for all competition contexts.
- Maxi-screen mode works as a specialized read-only presentation route.
- The documented deployment path works end to end in a staging-like environment.
- All must-pass v1 E2E flows pass together.
- The team can reasonably run the event without relying on Excel for live operations.

**Risks**

- Leaving public/maxi too late and discovering read-model gaps.
- Release-only operational issues surfacing after business work looks done.
- UX polish expanding into a never-ending finishing phase.

**Why it should come before launch, but after the others**

This milestone integrates and hardens everything already built. It should come last because it depends on nearly every write workflow and state rule being stable, but it must still happen before launch because public trust and operational readiness are part of the product promise.

---

## Notes on sequencing

- **m-2 is the first true product-value milestone.** Reach it as early as possible.
- **m-3 and m-4 can overlap slightly** once m-2 is stable, but m-3 should not change authoritative scoring rules and m-4 should not introduce live-collaboration shortcuts.
- **m-6 must not be skipped.** The PRD and functional requirements make trust, appeal-window visibility, auditability, and post-completion correction behavior part of v1, not polish.
- **m-7 is not “just UI”.** It is where deployment, read models, and acceptance-level confidence are finished.
