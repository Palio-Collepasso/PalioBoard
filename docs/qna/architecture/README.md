# Architecture Q&A

This directory contains architecture-level clarifications and decisions, about how the system should be built, how components interact, or how runtime guarantees must be enforced.

Use these files as follows:

- [`system boundaries.md`](system%20boundaries.md): system boundary, stack responsibilities, and what belongs to api, frontend, database, and infrastructure.
- [`authorization.md`](authorization.md): authentication, users, roles, capabilities, and provisioning.
- [`module boundaries.md`](module%20boundaries.md): api structure, module boundaries, project structure, and developer-facing organization.
- [`consistency and projections.md`](consistency%20and%20projections.md): write consistency, audit, projections, events, idempotency, and persistence conventions.
- [`realtime and live entry.md`](realtime%20and%20live%20entry.md): concurrency, leases, live entry, optimistic locking, realtime architecture, and live draft lifecycle/recovery.
- [`api and contracts.md`](api%20and%20contracts.md): API design, contracts, and runtime contract expectations.
- [`deployment and operations.md`](deployment%20and%20operations.md): deployment, environments, infrastructure, configuration, observability, local development, and operational concerns.

Cross-cutting topics:
- Database, migrations, and schema management are primarily in [`../data/schema and migrations.md`](../data/schema%20and%20migrations.md), with realtime persistence details in [`realtime and live entry.md`](realtime%20and%20live%20entry.md).
- Api stack and developer tooling are split between [`module boundaries.md`](module%20boundaries.md) and [`deployment and operations.md`](deployment%20and%20operations.md).
- Runtime consistency and persistence conventions span [`consistency and projections.md`](consistency%20and%20projections.md), [`api and contracts.md`](api%20and%20contracts.md), [`../data/schema and migrations.md`](../data/schema%20and%20migrations.md), [`realtime and live entry.md`](realtime%20and%20live%20entry.md), and [`deployment and operations.md`](deployment%20and%20operations.md).