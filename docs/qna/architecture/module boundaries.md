# Module Boundaries

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


## 12. Backend stack, project structure, and developer tooling
### 95. What framework and core backend stack are standardized for v1?
**Decision:** Standardize on **FastAPI + Pydantic DTOs + SQLAlchemy 2.x + Alembic**. Keep API DTOs and persistence models separate so transport contracts do not leak into ORM internals.

### 96. What project structure should the monorepo use?
**Decision:** Use a single monorepo with `apps/backend`, `apps/web`, `infra`, `docs`, `tools`, and a top-level `Makefile` plus `.github/workflows`. The backend keeps bounded modules with `facade/application/domain/infrastructure`; the frontend keeps three lazy shells, `features/`, and one `shared/` root with subfolders.

### 97. Should `event_operations` and `results` remain separate backend modules?
**Decision:** Yes. `event_operations` should own lifecycle/state transitions, while `results` owns canonical official result persistence. That boundary will stay useful as live draft and review flows grow.

### 103. Should backend architectural boundaries be enforced automatically?
**Decision:** Yes. Add CI checks that fail when one backend module imports another module’s internals. Boundaries should be enforceable rules, not only code-review discipline.

### 104. Should frontend architectural boundaries also be enforced automatically?
**Decision:** Yes. Add CI checks so shells do not depend on each other casually, `shared/` stays generic, and feature imports respect the intended layering.

## 13. Runtime consistency, persistence conventions, and contracts
### 112. How is dependency wiring handled inside the backend?
**Decision:** Keep wiring manual and explicit in the composition root. That is simpler than introducing a DI framework now, while still leaving room to adopt DI later if the graph grows.
