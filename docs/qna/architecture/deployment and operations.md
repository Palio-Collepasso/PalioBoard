# Deployment and Operations

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
**Decision:** The whole project uses a monorepo containing frontend, backend, committed API contract artifacts, frontend-generated API types, migrations, and deployment configuration.


## 12. Backend stack, project structure, and developer tooling
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

### 105. What minimal operational endpoints are exposed?
**Decision:** Expose **liveness**, **readiness**, and a small **build/version** endpoint. That is enough for a single-VPS setup without introducing heavier operational tooling.

### 106. Is external error monitoring required in v1?
**Decision:** No. Structured logs remain the only monitoring mechanism in v1, which keeps the operational stack intentionally small.

### 107. Is server-side data caching part of v1?
**Decision:** No. Read performance comes from DB-backed projections, not from a separate cache. Nginx only needs to cache static frontend assets.

## 13. Runtime consistency, persistence conventions, and contracts
### 122. Should v1 include background cleanup jobs for transient data?
**Decision:** No. There is no expectation of enough transient data to justify cleanup jobs in v1, and later infrastructure changes can revisit that decision.

## Related product clarification
### 19) Does v1 depend on local hosting or cloud hosting?
**Answer:** No strong product dependency was requested. v1 can be **deployment-agnostic**.
