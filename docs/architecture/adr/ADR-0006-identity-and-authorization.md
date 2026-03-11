# ADR-0006 — Identity, Application Users, and Capability-Based Authorization

- Status: Accepted
- Date: 2026-03-11

## Context

The system needs individual audit identity, capability-based authorization, and a future path to SSO or custom auth.

## Decision

Identity and authorization are split:

- Supabase Auth owns identity in v1
- the application database owns:
  - application users
  - roles
  - role-capability mappings
  - future direct user capability grants

Authorization model:

- capability-based
- roles are seeded bundles
- capability vocabulary is defined in code
- roles and mappings are seeded/static in v1
- no open self-registration

User provisioning:

- superadmin-only
- minimal in-app create-user UI in v1
- create identity-provider account + linked application user + seeded role
- best-effort compensation if cross-system provisioning partially fails

## Consequences

### Positive

- Clear split between external identity and internal authorization.
- Good portability to future SSO/custom auth.
- Clean audit actor model via app user id.

### Negative

- Provisioning spans two systems and is not one ACID transaction.
- Role editing is intentionally minimal in v1.

## Follow-ups

- Keep identity provider access behind explicit adapters.
- Add richer user lifecycle management only after v1.
