# Consistency and Projections

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


## 13. Runtime consistency, persistence conventions, and contracts
### 108. What DB/runtime consistency settings are standardized?
**Decision:** Use Postgres **`READ COMMITTED`** by default, add **`SELECT ... FOR UPDATE`** on critical game workflows, and keep optimistic versions for stale-data detection in user-facing flows.

### 120. How should audit identify the actor in v1?
**Decision:** Store only `actor_user_id`. It is the leanest model and is acceptable because user management is tightly controlled in v1.
