# Data Q&A

This directory contains clarifications about the data model, persistence rules, invariants, and schema evolution.

Use these files as follows:

- [`result model and invariants.md`](result%20model%20and%20invariants.md): official result model, tournament representation, audit simplification, official metrics, field catalog, and game immutability rules.
- [`schema and migrations.md`](schema%20and%20migrations.md): database schema management, migration strategy, and persistence-oriented structural decisions.

Related architecture material:
- Realtime persistence and live draft recovery details are in [`../architecture/realtime and live entry.md`](../architecture/realtime%20and%20live%20entry.md).
- Write consistency, projection updates, idempotency, and audit behavior are in [`../architecture/consistency and projections.md`](../architecture/consistency%20and%20projections.md).
- API-facing contracts that reflect persistence choices are in [`../architecture/api and contracts.md`](../architecture/api%20and%20contracts.md).