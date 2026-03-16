# Deploy

## Purpose

Describe how changes move to deployed environments safely and repeatably.

## Scope

Covers build, migration, release, verification, rollback, and communication steps.

## Environments

| Environment | Purpose | URL/Location | Owner | Notes |
|---|---|---|---|---|
| local | dev | `http://127.0.0.1:8080` | repo contributors | Same-origin Docker Compose smoke stack |
| production | live | single VPS/VM, configured per operator | deployment owner | Docker Compose + Nginx, one backend instance, and planned downtime |

## Release Principles

- Prefer reversible, low-risk releases.
- Separate schema-risk from app-risk when possible.
- Validate before and after deployment.
- Keep rollback instructions explicit.

## Preconditions

- [ ] Required PRs merged
- [ ] Required checks passed
- [ ] Release notes prepared
- [ ] Migration impact reviewed
- [ ] Backward compatibility reviewed
- [ ] Rollback plan ready

## Release Input

> Record the release input used for each deployment:
- git SHA or release tag;
- Docker image reference(s) if applicable;
- migration version(s);
- operator name;
- deploy timestamp.

## Deployment Procedure

### 1. Prepare release

1. Confirm the change matches the current single-VPS, Docker Compose deployment baseline from `ADR-0008`.
2. Review whether the release changes migrations, env vars, proxy routes, or the OpenAPI contract.

### 2. Build artifacts

1. Build the backend and Nginx images from `infra/docker/`.
2. Confirm the committed `docs/api/openapi.yaml` and any generated frontend types are up to date if the release changed the contract.

### 3. Apply migrations

1. Run the explicit migration step before starting the new app version.
2. Do not hide migrations inside backend startup; the same explicit rule used in local smoke checks applies to deployment.

### 4. Deploy application

1. Update the Compose-managed backend and Nginx images on the target host.
2. Restart the stack in the smallest acceptable maintenance window for the single-instance v1 deployment model.

### 5. Post-deploy verification

1. Check `/healthz`, `/readyz`, and `/version`.
2. Verify the same-origin proxy still serves `/`, `/api/admin/health`, `/api/public/health`, and `/realtime/health`.

Future note:
- add admin, public, and maxi workflow smoke checks here when those surfaces expose stable business behavior beyond the current scaffold and health-path baseline

### 6. Communicate completion

1. Record the deployed ref, operator, and verification result.
2. Share any residual manual follow-up or rollback watch items with the operators.

## Verification Checklist

- [ ] Service is reachable
- [ ] Health checks pass
- [ ] Critical API endpoints respond correctly
- [ ] Critical user journey verified
- [ ] Logs/metrics look healthy
- [ ] No migration errors
- [ ] No unexpected permission/auth failures

## Rollback Scenarios

Template for each rollback scenario: `docs/templates/ops/deploy-rollback-scenario.template.md`

### Application or proxy deploy regression

- **Trigger:** Health endpoints fail, the same-origin shell smoke fails, or the API/proxy route split is broken after release.
- **Risk:** The single production stack is partially or fully unavailable.
- **Decision owner:** Deployment owner on duty
- **Rollback steps:**
  1. Revert to the previous known-good backend and Nginx image set.
  2. Restart the Compose-managed stack with the previous release ref.
- **Data considerations:**
  - If migrations already ran, confirm the schema remains backward-compatible before rolling back application code.
- **Post-rollback verification:**
  - Repeat the standard post-deploy verification checklist.
- **Follow-up actions:**
  - Capture the failure mode in `docs/ops/runbook.md` if it becomes a recurring operational issue.

---

## Deployment Scenarios

Template for each deployment scenario: `docs/templates/ops/deploy-scenario.template.md`

### Standard application-only deploy

- **Use when:** No schema change is required.
- **Procedure:** Build new images, deploy them during the planned window, and run the post-deploy checks.
- **Extra checks:** Confirm `/version` reports the expected build metadata.

### Deploy with backward-compatible migration

- **Use when:** The schema change can be applied before the app restart without breaking the previous version.
- **Procedure:** Run the explicit migration step first, then deploy the new images.
- **Extra checks:** Validate readiness after migrations and before traffic is considered healthy.

### Deploy with risky migration

- **Use when:** The schema or data move is not safely reversible or backward-compatible.
- **Procedure:** Treat as a planned maintenance event with an explicit rollback decision point before application restart.
- **Extra checks:** Require manual review of migration impact and follow the incident hooks if verification fails.
- **Approval required from:** Deployment owner and the maintainer responsible for the risky migration

## Release History

Template for each release-history row: `docs/templates/ops/deploy-release-history-row.template.md`

> The record in this section is illustrative only. Remove it as soon as the first real release-history row is documented here.

| Date | Version/Ref | Environment | Operator | Result | Notes |
|---|---|---|---|---|---|
| `2026-03-15` | `example-ref` | `production` | `example-operator` | success | Example row showing the expected release-history format. |


## Repo-specific TODOs

Replace placeholders with:
- exact VPS access method;
- exact Docker Compose commands;
- exact health-check endpoints;
- exact smoke-test sequence;
- exact backup/restore references if any.

## Incident Handoff

If deployment fails or causes degraded service, continue in `docs/ops/runbook.md`.
