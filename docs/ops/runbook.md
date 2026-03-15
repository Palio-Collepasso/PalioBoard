# Runbook

## Purpose

Provide operational procedures for diagnosing, mitigating, and recovering from production or environment issues.

## Usage Rules

- Prefer the least risky mitigation first.
- Record what happened, what was changed, and why.
- If a step risks data loss or downtime, state that explicitly.
- Link incidents back to follow-up fixes and tests.

## Contacts / Ownership

| Area | Owner | Escalation |
|---|---|---|
| application | task owner / repo maintainer | open follow-up work and notify the current deployment owner |
| database | task owner / repo maintainer | escalate when readiness or migration recovery is blocked |
| infrastructure | task owner / repo maintainer | escalate when Compose, Nginx, or VPS-level recovery is needed |

## Incident Severity Guide

| Severity | Meaning | Typical response target |
|---|---|---|
| SEV-1 | Full production outage or data-risk incident during the event window | immediate |
| SEV-2 | Major degraded behavior with a workaround | same working session |
| SEV-3 | Limited or local-environment issue with low user impact | next available maintainer |

## Runbook Item Index

| Runbook ID | Problem | Severity range | Owner |
|---|---|---|---|
| `RB-001` | Readiness or health checks fail after a stack change | SEV-1 to SEV-2 | application/infrastructure |
| `RB-002` | Explicit migration step fails or was skipped | SEV-1 to SEV-2 | database/application |

---

## Runbook Items

Template for each runbook item: `docs/templates/ops/runbook-item.template.md`

### `RB-001` — Readiness or health checks fail after a stack change

- **Status:** active
- **Severity range:** `SEV-1 | SEV-2`
- **Owner:** application/infrastructure
- **Last reviewed:** `2026-03-15`

#### Symptoms

- `/readyz` returns `503`
- `/healthz` or same-origin proxy health routes fail after deploy or local stack restart

#### Detection

- **How to detect:**
  - curl `/healthz`, `/readyz`, `/api/admin/health`, and `/api/public/health`
  - review backend and Nginx logs for startup or proxy failures
- **Dashboards/logs/tools:**
  - Docker Compose logs
  - backend JSON request/application logs

#### Likely causes

- runtime DB is unavailable or misconfigured
- Nginx or backend container did not start with the expected image/config

#### Immediate safety checks

- [ ] Confirm whether the failure is local-only or production-facing
- [ ] Confirm whether the database is reachable
- [ ] Confirm whether the latest migration step completed

#### Mitigation steps

1. Check the current container status and logs.
2. Verify DB connectivity and the runtime env vars.
3. If the failure began immediately after release, consider rolling back to the previous image set.

#### Recovery steps

1. Restore the last known-good backend/proxy configuration.
2. Re-run the health checks and same-origin smoke paths.
3. Record the root cause and required follow-up.

#### Verification after recovery

- [ ] `/healthz` succeeds
- [ ] `/readyz` succeeds
- [ ] `/`, `/api/admin/health`, and `/api/public/health` behave normally

#### Escalation

- **Escalate when:**
  - recovery requires host-level intervention
  - there is uncertainty about rollback safety
- **Escalate to:** deployment owner and the maintainer responsible for the changed stack surface

#### Communication

- **Who to notify:** operators, reviewers, and affected stakeholders
- **What to communicate:** start time, impact, current mitigation, and rollback status
- **Update cadence:** at each mitigation milestone until service is healthy

#### Data / audit considerations

- Health-check failures alone should not mutate official business data.
- If readiness failed because migrations partially ran, capture the exact migration state before further action.

#### Follow-up work

- Add automated coverage if the failure exposed a missing smoke check.
- Update `docs/ops/deploy.md` or `docs/ops/local-dev.md` if the recovery procedure changed the standard workflow.

#### Related items

- **Deploy procedure:** `docs/ops/deploy.md`
- **Local reproduction guide:** `docs/ops/local-dev.md`
- **Business rules:** `docs/domain/business-rules.md`
- **Critical E2E flows:** `docs/testing/critical-e2e-flows.md`

### `RB-002` — Explicit migration step fails or was skipped

- **Status:** active
- **Severity range:** `SEV-1 | SEV-2`
- **Owner:** database/application
- **Last reviewed:** `2026-03-15`

#### Symptoms

- startup or readiness checks fail after schema changes
- application errors show missing schema objects or mismatched revision state

#### Detection

- **How to detect:**
  - inspect the migration command output
  - confirm the expected Alembic revision and schema exist
- **Dashboards/logs/tools:**
  - `alembic` output
  - backend logs
  - Postgres inspection queries

#### Likely causes

- the explicit migration step was never run
- the migration failed partway through or targeted the wrong database URL

#### Immediate safety checks

- [ ] Confirm which database was targeted
- [ ] Confirm whether partial schema changes were applied
- [ ] Confirm whether application traffic is still hitting the affected environment

#### Mitigation steps

1. Stop further rollout until the target database state is understood.
2. Re-run or repair the migration only after confirming the correct DB URL and revision state.
3. Roll back the application deploy if the release is not backward-compatible with the current schema state.

#### Recovery steps

1. Bring the schema to a known-good revision state.
2. Restart the application or stack if needed.
3. Re-run readiness and smoke verification.

#### Verification after recovery

- [ ] Expected schema exists
- [ ] Expected Alembic revision exists
- [ ] `/readyz` and the same-origin proxy checks succeed

#### Escalation

- **Escalate when:**
  - manual SQL intervention may be required
  - rollback safety is unclear because of partial data changes
- **Escalate to:** deployment owner and the maintainer responsible for persistence changes

#### Communication

- **Who to notify:** operators and reviewers for the release
- **What to communicate:** target DB, migration state, mitigation, and expected recovery time
- **Update cadence:** whenever migration state or rollback status changes

#### Data / audit considerations

- Record the exact revision state before applying manual fixes.
- Do not conceal partial migration failures behind automatic app restarts.

#### Follow-up work

- Add or tighten migration validation coverage when a failure mode becomes repeatable.
- Update local/deploy docs if the migration workflow changes.

#### Related items

- **Deploy procedure:** `docs/ops/deploy.md`
- **Local reproduction guide:** `docs/ops/local-dev.md`
- **Business rules:** `docs/domain/business-rules.md`
- **Critical E2E flows:** `docs/testing/critical-e2e-flows.md`

---

## Standard Incident Timeline

Template for each incident timeline: `docs/templates/ops/incident-timeline.template.md`

> The record in this section is illustrative only. Remove it as soon as the first real incident timeline is documented here.

- **Start time:** `<timestamp>`
- **Detection time:** `<timestamp>`
- **First mitigation:** `<timestamp>`
- **Recovery time:** `<timestamp>`
- **Resolved by:** `<name>`
- **Summary:** `<summary>`

## Post-Incident Reviews

Template for each post-incident review: `docs/templates/ops/post-incident-review.template.md`

> The record in this section is illustrative only. Remove it as soon as the first real post-incident review is documented here.

### `Example incident review`

- **Date:** `2026-03-15`
- **Severity:** `SEV-3`
- **Impact:** Example-only placeholder showing the expected review format.
- **Root cause:** Example-only placeholder.
- **What worked well:**
  - The issue was detected quickly.
- **What did not work well:**
  - No real incident data exists yet.
- **Action items:**
  - Replace this example with the first real post-incident review when available.
