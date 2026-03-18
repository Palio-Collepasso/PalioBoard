# System Boundaries

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

### 6. Should the api connect to Supabase through Supabase data APIs?
**Decision:** No. Python connects directly to Postgres using standard database connectivity and treats Supabase as a hosted Postgres instance.

### 7. Should runtime authorization depend on Postgres RLS or user-level DB identities?
**Decision:** No. Authorization stays in Python. The api uses a single application DB user for runtime access rather than impersonating end users at the database level.
