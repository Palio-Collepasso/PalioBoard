# Frontend Architecture

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
