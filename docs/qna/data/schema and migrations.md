# Schema and Migrations

## 9. Database, migrations, and schema management
### 74. What owns schema evolution?
**Decision:** Alembic is the primary source of truth for schema evolution. Supabase is treated as a hosting platform, not the schema authority.

### 75. Are schema changes run automatically on backend startup?
**Decision:** No. Migrations are an explicit deployment step.

### 76. Are runtime and migration DB credentials separated?
**Decision:** Yes. Runtime DB credentials are restricted to normal app access, while migration/admin credentials are used for schema changes and operational maintenance.

### 77. Is the database split into separate schemas per module?
**Decision:** No. v1 uses one application schema in Postgres, with module ownership enforced in Python code rather than DB schema partitioning.

## 13. Runtime consistency, persistence conventions, and contracts
### 109. What ID strategy is used across the schema?
**Decision:** Use **UUIDv7** for aggregate roots and composite primary keys for pure join/helper tables. This keeps aggregate identity explicit and avoids fake surrogate ids where relational identity is already enough.

### 110. What deletion strategy is used?
**Decision:** Avoid a generic soft-delete model. Use hard delete only where the business explicitly allows it, and rely on explicit domain states everywhere else.

### 111. Where should UUIDv7 values be generated?
**Decision:** Generate them in Python, not in the database. Application-side generation keeps the system portable to plain Postgres and avoids coupling aggregate creation to DB-specific functions.

### 117. How should static/reference data be seeded?
**Decision:** Use idempotent scripts or queries outside normal app startup. Alembic owns schema evolution; seed commands own roles, role-capability mappings, bootstrap users, and other reference data.

### 121. How should enums and timestamps be stored?
**Decision:** Persist enums as text columns enforced by DB check constraints, and store all timestamps in UTC. Convert to Europe/Rome only at the presentation boundary.
