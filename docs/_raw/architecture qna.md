# PalioBoard - Architecture Q&A Decision Log

This document summarizes the architectural questions discussed so far and the resulting decisions, rewritten as explicit answers rather than short confirmations.

It captures the **current architecture direction** up to this point in the conversation.

---

## 1. System boundary and stack responsibilities

### 1. What is the boundary between Python and Supabase?
**Decision:** Python is the only application API and the only layer allowed to access application data. Supabase is used as the current hosted Postgres database and identity provider, but it is **not** exposed directly to Angular for business data access.

### 2. Who owns authentication in v1?
**Decision:** Supabase Auth owns identity in v1, while Python owns business APIs and authorization. Angular authenticates through Supabase Auth, sends the bearer token to Python, and Python validates the token and resolves the corresponding application user.

### 3. Where does authorization truth live?
**Decision:** Authorization lives in the application domain, not in Supabase JWT claims. Capabilities are checked in Python on each protected API entry point, and critical workflows still enforce domain invariants inside application services.

### 4. Should capabilities be dynamic data or fixed vocabulary?
**Decision:** Capabilities are part of the application vocabulary and are defined in code as a stable registry/enum. The database stores roles, role-capability mappings, and user-role assignments.

### 5. Is portability to plain Postgres a hard requirement?
**Decision:** Yes. The architecture must remain portable to self-hosted Postgres later, so Supabase-specific features must not become part of core business correctness.

### 6. Should the backend connect to Supabase through Supabase data APIs?
**Decision:** No. Python connects directly to Postgres using standard database connectivity and treats Supabase as a hosted Postgres instance.

### 7. Should runtime authorization depend on Postgres RLS or user-level DB identities?
**Decision:** No. Authorization stays in Python. The backend uses a single application DB user for runtime access rather than impersonating end users at the database level.

---

## 2. Authentication, users, roles, and provisioning

### 8. Should there be a separate application user model?
**Decision:** Yes. The system has an application user/profile model in the app database, linked 1:1 to the Supabase Auth user id. This app user is the source of truth for roles, effective permissions, and audit identity.

### 9. What is the authorization model?
**Decision:** The system is capability-based. Roles are predefined bundles of capabilities. The schema supports direct per-user capability grants for future evolution, but v1 will not expose or use that feature.

### 10. Are role definitions editable in v1?
**Decision:** No. In v1, roles, role-capability mappings, and default user-role assignments are seeded/static. If changes are needed, they will be made directly in the database as an operational action.

### 11. Is there a superadmin concept?
**Decision:** Yes. Superadmin is modeled as a role bundle/capability set, not as a special code path spread across the application. It includes admin capabilities plus user-management and future app-management capabilities.

### 12. How is the first superadmin bootstrapped?
**Decision:** The first superadmin is created through a seed/migration path, with manual DB intervention documented as a break-glass recovery procedure.

### 13. Should users self-register?
**Decision:** No. There is no public self-registration. Authenticated application users are provisioned explicitly.

### 14. Who is allowed to provision users in v1?
**Decision:** Only the superadmin can create users.

### 15. What user management exists in the app in v1?
**Decision:** v1 includes only a **minimal superadmin UI** for creating a user with an email, a password, and a seeded role. Users are active immediately on creation.

### 16. Does the minimal user UI also provision the identity-provider account?
**Decision:** Yes. The backend provisions the Auth identity and the linked application user in a single orchestrated workflow.

### 17. What login method is used in v1?
**Decision:** Email and password.

### 18. Is there email verification, invitation flow, or reset/set-password flow in v1?
**Decision:** No. v1 keeps provisioning extremely minimal: the superadmin creates the user with a password, and credentials are handed over manually offline.

### 19. How are cross-system provisioning failures handled?
**Decision:** User provisioning is treated as a two-step external workflow with best-effort compensation. The backend creates the identity-provider account first, then creates the application user. If the second step fails, the backend attempts to remove the identity-provider account and logs any unrecoverable partial failure clearly.

### 20. Should auth be abstracted for future SSO/custom identity?
**Decision:** Yes. Authentication and provisioning sit behind explicit identity-provider adapters so Supabase Auth can be replaced later without touching application/domain logic.

### 21. Should capabilities be cached in process as effective permissions?
**Decision:** No separate runtime cache of effective user permissions is introduced as an architectural requirement. The hardcoded part is only the capability vocabulary. Role/user assignments remain data-driven.

---

## 3. Backend structure and module boundaries

### 22. What backend architecture style should be used?
**Decision:** A Python **modular monolith** with explicit bounded modules.

### 23. How are module boundaries enforced?
**Decision:** Each module has strict ownership of its own tables and repositories. Other modules may only interact with it through explicit public interfaces/contracts, not by importing repositories or ORM models directly.

### 24. What coordinates cross-module workflows?
**Decision:** A dedicated application/use-case orchestration layer coordinates multi-module workflows and owns a single database transaction for each business use case.

### 25. How are transactions managed?
**Decision:** The system uses a **Unit of Work** pattern. The orchestrator owns the SQLAlchemy session/transaction, and repositories are session-bound rather than session-creating.

### 26. Where does business orchestration live?
**Decision:** Business orchestration lives in Python application services, not in database triggers. Postgres can enforce constraints and support queries, but domain workflows are not hidden in triggers.

### 27. How should commands and queries be split?
**Decision:** The monolith uses an internal CQRS-style split: write-side use cases/repositories for commands, and dedicated query services for read models/public screens.

### 28. How is persistence implemented?
**Decision:** Command/write flows use ORM-backed repositories. Read/query flows use explicit SQL or SQLAlchemy Core shaped for screens and projections.

### 29. Should adapters be used broadly?
**Decision:** Yes, but only for technical boundaries. Anything that is not business logic should sit behind an explicit adapter interface, such as identity, live-game state, clock, idempotency storage, and future notifications.

---

## 4. Write consistency, events, audit, and idempotency

### 30. Are writes synchronous or eventually consistent?
**Decision:** Business writes are synchronous. Result changes, state transitions, Jolly effects, audit persistence, and leaderboard updates all happen within one application transaction.

### 31. How are events used?
**Decision:** Events are collected during the workflow as structured domain/application facts, but they do not drive business consistency. They are translated into audit rows before commit, in the same transaction.

### 32. What is the leaderboard update strategy?
**Decision:** The current leaderboard/read model is updated on every standings-relevant write, but the recalculation strategy is **full recomputation of the affected scope**, not incremental delta math.

### 33. Where does leaderboard recomputation logic live?
**Decision:** In Python application services.

### 34. Are public projections versioned historically?
**Decision:** No. Projections are current-state only. Historical traceability comes from authoritative tables plus audit logs.

### 35. Should realtime notifications affect transaction success?
**Decision:** No. Realtime delivery is post-commit and best-effort. Notification failure must not invalidate or roll back a transaction.

### 36. How is idempotency handled?
**Decision:** Critical command endpoints support idempotency through a shared application-level facility. A route/dependency/decorator can expose it at the API boundary, but the guarantee is enforced transactionally through persisted idempotency records.

### 37. What does a repeated idempotent request return?
**Decision:** The system reconstructs the response from the persisted command outcome/reference rather than storing and replaying the raw original HTTP response.

### 38. What does the audit model include?
**Decision:** Audit captures meaningful business actions, not low-level transport noise. Draft/live-entry collaboration state is separated from official audited history.

---

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
**Decision:** The backend/database clock is authoritative for all business and collaboration timing, including lease expiry.

### 45. How are live drafts modeled in the final design?
**Decision:** Live-game state is **memory-first**. Active draft values, leases, connected editors, and live revision counters live in backend memory first. Persisted draft snapshots exist separately for restart recovery, but live collaboration is driven from memory.

### 46. Are live draft snapshots part of official audited business history?
**Decision:** No. Persisted draft snapshots are stored in a dedicated provisional draft area/table/module, clearly separate from official business state and audit history.

### 47. When are draft snapshots persisted?
**Decision:** On three triggers:
- periodically while editing (coarse cadence, not keystroke-level)
- when a field lease ends
- as a best-effort flush when the user leaves/closes the game

### 48. How is live state restored after backend restart?
**Decision:** On restart, the backend reloads the persisted provisional draft snapshots into memory. That hydrated in-memory state becomes the new live draft state, and reconnecting clients receive it.

### 49. Can multiple games be in progress simultaneously?
**Decision:** Yes. The architecture must support multiple in-progress games at once, especially for Prepalio scenarios.

---

## 6. Realtime architecture

### 50. Which transport is used for which interaction?
**Decision:**
- standard admin screens: polling where acceptable
- public/maxi-screen live updates: SSE
- admin live-entry collaboration: WebSockets

### 51. How are realtime channels scoped?
**Decision:** Realtime is scoped **per game**. There is one logical live collaboration/read stream per `game_id`, not a global current-game channel.

### 52. Is there special backend business logic for maxi-screen selection?
**Decision:** No. Maxi-screen pages are normal Angular pages designed for projector usage. There is no special backend “featured game” business state. A user with the frontend-only maxi-screen shortcut can simply open the page for a specific game.

### 53. Is the maxi-screen route protected by backend authorization?
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

---

## 7. API design and contracts

### 60. What API style is used?
**Decision:** REST with explicit command/query endpoints. The API surface is intent-oriented, not generic CRUD.

### 61. Is the API split into multiple surfaces?
**Decision:** Yes. The backend is explicitly split into:
- `/admin/...` for authenticated command/query operations
- `/public/...` for anonymous read models
- `/realtime/...` for SSE and WebSocket endpoints

### 62. What do public endpoints read from?
**Decision:** Public and maxi-screen endpoints read only from projection/read models, never directly from authoritative write tables.

### 63. How are contracts shared with Angular?
**Decision:** Python owns the OpenAPI schema. TypeScript types are generated from OpenAPI, but Angular data-access services remain hand-written.

### 64. What is the error contract?
**Decision:** Errors use a standardized machine-readable envelope with:
- consistent HTTP status usage
- stable error codes
- structured contextual data
- a request/correlation id
Angular translates error codes and data into user-friendly messages.

### 65. Is the API versioned formally in v1?
**Decision:** No. The API is treated as a first-party internal API evolving together with the frontend.

---

## 8. Frontend architecture

### 66. How many frontend apps are there?
**Decision:** One Angular SPA with three clearly separated route areas/shells:
- admin/judge shell
- public shell
- maxi-screen shell

### 67. Is SSR used?
**Decision:** No. The frontend is a pure Angular SPA.

### 68. How is frontend state managed?
**Decision:** State is mostly feature-local and service-based. There is no centralized app-wide store by default.

### 69. Are route areas isolated?
**Decision:** Yes. The three route areas are strictly lazy-loaded so public/maxi-screen bundles do not drag in admin code unnecessarily.

### 70. Should the Angular app itself respect internal architectural boundaries?
**Decision:** Yes. It should have explicit internal boundaries, using separate shell areas, features, and a single `shared/` root with subfolders such as `shared/ui` and `shared/api`.

### 71. How is frontend API access organized?
**Decision:** Separate Angular API service layers exist for each backend surface: admin, public, and realtime.

### 72. Is realtime handling global in the SPA?
**Decision:** No. Realtime handling is feature-scoped per shell/feature, not managed through one global application-wide store or bus.

### 73. How is authentication handled in the browser?
**Decision:** Angular uses the bearer-token model. It authenticates via Supabase Auth and sends the access token to Python. The authenticated admin/judge area uses a persisted browser session.

---

## 9. Database, migrations, and schema management

### 74. What owns schema evolution?
**Decision:** Alembic is the primary source of truth for schema evolution. Supabase is treated as a hosting platform, not the schema authority.

### 75. Are schema changes run automatically on backend startup?
**Decision:** No. Migrations are an explicit deployment step.

### 76. Are runtime and migration DB credentials separated?
**Decision:** Yes. Runtime DB credentials are restricted to normal app access, while migration/admin credentials are used for schema changes and operational maintenance.

### 77. Is the database split into separate schemas per module?
**Decision:** No. v1 uses one application schema in Postgres, with module ownership enforced in Python code rather than DB schema partitioning.

### 78. Are provisional draft snapshots stored in the same database?
**Decision:** The current direction is to store all persistent app data, including provisional draft snapshots, in the same Postgres database under clearly separated tables/modules. The final storage-table naming/details were still being discussed when this log was requested.

---

## 10. Deployment, environments, and infrastructure

### 79. What deployment target is optimized for?
**Decision:** A single VPS/VM deployment using Docker Compose.

### 80. How is traffic served?
**Decision:** Angular and Python are served behind a single reverse proxy and same public origin. One origin handles SPA routes plus `/api/...` and `/realtime/...` routing.

### 81. What reverse proxy is used?
**Decision:** Nginx.

### 82. Is one backend instance assumed in v1?
**Decision:** Yes. v1 assumes one backend instance, while still keeping correctness in DB-backed structures where needed and avoiding in-memory correctness dependencies where possible.

### 83. Is extra infrastructure such as Redis or message brokers required in v1?
**Decision:** No. v1 intentionally avoids Redis, brokers, worker services, and other extra runtime components. Redis may become relevant later as an implementation of the live-state adapter.

### 84. Are background jobs allowed?
**Decision:** Only lightweight in-process background tasks are allowed in v1, and they must not be part of business correctness.

### 85. Is zero-downtime deployment required?
**Decision:** No. Short planned downtime is acceptable because the app is used only during a small time window and releases happen outside the event.

### 86. How many environments are supported?
**Decision:** Development and production only.

### 87. What is the release strategy?
**Decision:** Automated CI plus manual production deploy.

### 88. What quality gates run before commit and in CI?
**Decision:** Formatting and linting run before commit, and CI runs checks such as linting, typing, tests, and build validation.

### 89. How are backups handled in v1?
**Decision:** Managed database backups are considered sufficient in v1. No additional application-level snapshot/export workflow is required.

---

## 11. Configuration, observability, and local development

### 90. How is configuration managed?
**Decision:** Configuration and secrets are env-based. Python uses typed runtime settings from environment variables; Angular uses environment-based configuration as well.

### 91. What logging/observability style is used?
**Decision:** Structured JSON logs with request/correlation ids propagated through HTTP, realtime actions, and related persistence/audit operations.

### 92. What local development approach is used for identity?
**Decision:** Production uses the real identity-provider adapter, while local development can use a dev identity adapter or bypass mode so the team can work locally without depending on the real cloud identity service.

### 93. What test database is used?
**Decision:** Backend integration tests use a real local Postgres test database, not SQLite.

### 94. What repository strategy is used?
**Decision:** The whole project uses a monorepo containing frontend, backend, shared generated API types, migrations, and deployment configuration.

---

## 12. Backend stack, project structure, and developer tooling

### 95. What framework and core backend stack are standardized for v1?
**Decision:** Standardize on **FastAPI + Pydantic DTOs + SQLAlchemy 2.x + Alembic**. Keep API DTOs and persistence models separate so transport contracts do not leak into ORM internals.

### 96. What project structure should the monorepo use?
**Decision:** Use a single monorepo with `apps/backend`, `apps/web`, `infra`, `docs`, and a top-level `Makefile`. The backend keeps bounded modules with `facade/application/domain/infrastructure`; the frontend keeps three lazy shells, `features/`, and one `shared/` root with subfolders.

### 97. Should `event_operations` and `results` remain separate backend modules?
**Decision:** Yes. `event_operations` should own lifecycle/state transitions, while `results` owns canonical official result persistence. That boundary will stay useful as live draft and review flows grow.

### 98. What local development database/auth setup is preferred?
**Decision:** Use a plain local Postgres container plus the existing dev identity adapter. This keeps daily development light and avoids coupling local work to the full Supabase local stack.

### 99. How should apps run locally day to day?
**Decision:** Run Postgres in Docker, but run FastAPI and Angular natively with hot reload. Keep full Docker Compose runs for integration checks and production-like verification.

### 100. What repo/dev tooling is standardized?
**Decision:** Keep the monorepo tooling-light. Use **`uv` for Python**, **`npm` for the frontend**, and **`make`** as the stable top-level command surface.

### 101. What quality gates are standardized for Python?
**Decision:** Use **Ruff + Pyright + pytest + pre-commit**. This keeps formatting, linting, typing, and test entrypoints consistent locally and in CI.

### 102. What browser end-to-end flows are must-pass in v1?
**Decision:** Keep a small Playwright suite focused on the risky flows: completing a raning game, public update propagation, 1v1 progression/completion, post-completion edit behavior, and concurrent live-result locking/conflict behavior.

### 103. Should backend architectural boundaries be enforced automatically?
**Decision:** Yes. Add CI checks that fail when one backend module imports another module’s internals. Boundaries should be enforceable rules, not only code-review discipline.

### 104. Should frontend architectural boundaries also be enforced automatically?
**Decision:** Yes. Add CI checks so shells do not depend on each other casually, `shared/` stays generic, and feature imports respect the intended layering.

### 105. What minimal operational endpoints are exposed?
**Decision:** Expose **liveness**, **readiness**, and a small **build/version** endpoint. That is enough for a single-VPS setup without introducing heavier operational tooling.

### 106. Is external error monitoring required in v1?
**Decision:** No. Structured logs remain the only monitoring mechanism in v1, which keeps the operational stack intentionally small.

### 107. Is server-side data caching part of v1?
**Decision:** No. Read performance comes from DB-backed projections, not from a separate cache. Nginx only needs to cache static frontend assets.

## 13. Runtime consistency, persistence conventions, and contracts

### 108. What DB/runtime consistency settings are standardized?
**Decision:** Use Postgres **`READ COMMITTED`** by default, add **`SELECT ... FOR UPDATE`** on critical game workflows, and keep optimistic versions for stale-data detection in user-facing flows.

### 109. What ID strategy is used across the schema?
**Decision:** Use **UUIDv7** for aggregate roots and composite primary keys for pure join/helper tables. This keeps aggregate identity explicit and avoids fake surrogate ids where relational identity is already enough.

### 110. What deletion strategy is used?
**Decision:** Avoid a generic soft-delete model. Use hard delete only where the business explicitly allows it, and rely on explicit domain states everywhere else.

### 111. Where should UUIDv7 values be generated?
**Decision:** Generate them in Python, not in the database. Application-side generation keeps the system portable to plain Postgres and avoids coupling aggregate creation to DB-specific functions.

### 112. How is dependency wiring handled inside the backend?
**Decision:** Keep wiring manual and explicit in the composition root. That is simpler than introducing a DI framework now, while still leaving room to adopt DI later if the graph grows.

### 113. Where do active field leases live in the final design?
**Decision:** In the final live-draft design, active field leases are an **in-memory concern**, not durable business state. They must be reacquired after restart, which keeps the recovery model simpler and aligned with a future Redis-backed live-state adapter.

### 114. How are provisional live drafts persisted?
**Decision:** Persist **whole-game JSON draft blobs** keyed by game identity, together with revision metadata. This mirrors the memory-first live state much better than normalizing per-field draft rows.

### 115. How should live draft hydration behave across implementations?
**Decision:** Treat hydration strategy as an infrastructure detail behind the `LiveGameStateStore` adapter. In v1 it can lazy-hydrate from persisted snapshots on first access; a future Redis implementation can choose a different policy without changing business logic.

### 116. Where should provisional draft snapshots be stored in v1?
**Decision:** In the same Postgres database as the rest of the app, but in tables clearly separated from official business state. That keeps the system simple while still distinguishing recovery data from canonical data.

### 117. How should static/reference data be seeded?
**Decision:** Use idempotent scripts or queries outside normal app startup. Alembic owns schema evolution; seed commands own roles, role-capability mappings, bootstrap users, and other reference data.

### 118. How should OpenAPI contracts be managed in the repo?
**Decision:** Commit the OpenAPI spec as a versioned artifact and generate TypeScript types from that file. Do not make the frontend depend on a running backend just to regenerate types.

### 119. Should generated TypeScript types be committed?
**Decision:** No. Commit only the OpenAPI spec; regenerate TS types locally or in CI through `make`. That keeps review noise down and makes the spec the single committed contract artifact.

### 120. How should audit identify the actor in v1?
**Decision:** Store only `actor_user_id`. It is the leanest model and is acceptable because user management is tightly controlled in v1.

### 121. How should enums and timestamps be stored?
**Decision:** Persist enums as text columns enforced by DB check constraints, and store all timestamps in UTC. Convert to Europe/Rome only at the presentation boundary.

### 122. Should v1 include background cleanup jobs for transient data?
**Decision:** No. There is no expectation of enough transient data to justify cleanup jobs in v1, and later infrastructure changes can revisit that decision.

## 14. Live draft lifecycle and recovery

### 123. What happens if draft deletion fails when a game leaves `in_progress`?
**Decision:** Draft cleanup must not affect the business transaction. Introduce a technical `live_cycle` counter on the game so stale draft data from previous cycles becomes ignorable instead of dangerous.

### 124. When a game re-enters `in_progress`, how is the new live draft initialized?
**Decision:** Prefill it from the current official `game_entries`. That gives operators continuity and makes subsequent edits start from the already-official state rather than from an empty draft.

### 125. When leaving `in_progress`, should the system rewrite all official entries or only changed ones?
**Decision:** Only changed ones. Compare the draft with the current official state, then write and audit only the `game_entries` that actually changed.

### 126. How should live pages bootstrap their state?
**Decision:** Use an initial HTTP fetch followed by realtime subscription. Realtime keeps the page fresh, but it should not be responsible for delivering the first correct state.

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
