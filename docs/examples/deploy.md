# Deploy

## Purpose

Describe the PalioBoard deployment model and the repeatable steps for releasing safely.

This starter reflects the approved v1 operational shape:
- single VPS;
- Docker Compose deployment;
- Nginx reverse proxy;
- one api instance;
- manual production deploys;
- planned downtime allowed.

## Scope

Covers release preparation, application deployment, migration handling, verification, rollback, and communication.

## Environments

| Environment | Purpose | Location | Owner | Notes |
|---|---|---|---|---|
| local | development | developer machine | engineering | Postgres in Docker, apps native |
| staging | optional pre-prod | `<fill if used>` | engineering | Use only if the repo actually has staging |
| production | live event system | single VPS | engineering / operators | Docker Compose + Nginx |

## Release principles

- Prefer boring, reversible releases.
- Treat authoritative-write correctness as more important than release speed.
- Review migration risk explicitly.
- Verify public/admin/core flows immediately after deploy.
- Do not pretend v1 is zero-downtime if it is not.

## Preconditions

- [ ] Target PRs are merged.
- [ ] Required checks are green.
- [ ] Documentation affected by the change is already updated.
- [ ] Migration impact was reviewed.
- [ ] Rollback plan exists.
- [ ] Someone is responsible for post-deploy verification.

## Release artifact / input

Document the actual release input used by your repo:
- git SHA or release tag;
- Docker image reference(s) if applicable;
- migration version(s);
- operator name;
- deploy timestamp.

## Standard deployment procedure

### 1. Prepare the release

1. Confirm the target commit/ref.
2. Review whether the release changes:
   - official result workflows;
   - standings/projection logic;
   - live ranking collaboration;
   - auth/capability behavior;
   - schema/migrations.
3. Announce planned downtime if the deployment affects active operators.
4. Ensure backup/restore expectations are known.

### 2. Build or fetch artifacts

1. Build or pull the Docker images/artifacts used by production.
2. Confirm configuration files and environment variables match the target release.

> Replace this section with the real repo-specific image/build commands.

### 3. Apply database migrations

1. Put the system into the intended deployment window.
2. Apply the release’s migrations.
3. Confirm migration success before exposing the new app version.

Important v1 rule:
- if migration fails, do not continue the application deploy.

### 4. Deploy application services

1. Update the running Docker Compose application on the VPS.
2. Restart or recreate services as required by the release.
3. Confirm Nginx and the api process are healthy.

### 5. Post-deploy verification

1. Verify the application is reachable.
2. Verify api health endpoints/logs.
3. Verify admin login works.
4. Verify public standings/results pages load.
5. Verify maxi-screen route loads.
6. Verify at least one authoritative-read path and one authoritative-write path.

### 6. Communicate completion

1. Record the deployed ref, operator, and result.
2. Communicate success or failure to the relevant team.
3. Link any follow-up issues discovered during verification.

## Verification checklist

- [ ] Nginx serves the application correctly.
- [ ] Api process is healthy.
- [ ] Database migrations completed successfully.
- [ ] Public standings page loads.
- [ ] Admin login works.
- [ ] A read-only public/maxi path works.
- [ ] At least one safe admin workflow smoke check passes.
- [ ] Logs do not show immediate auth, migration, or serialization failures.

## Deployment scenarios

### Standard application-only deploy

- **Use when:** code changes do not require schema change.
- **Extra checks:** smoke the touched admin/public flows.
- **Rollback profile:** relatively simple.

### Deploy with backward-compatible migration

- **Use when:** schema changes are additive or otherwise safe for the deploy order.
- **Extra checks:** verify both migration success and the changed workflow.
- **Rollback profile:** moderate; confirm whether app-only rollback remains valid.

### Deploy with risky migration

- **Use when:** schema changes are destructive, order-sensitive, or hard to reverse.
- **Extra checks:** require explicit operator sign-off and a rehearsed rollback/data plan.
- **Approval required from:** `<team/person>`
- **Notes:** avoid this near live event hours whenever possible.

## Rollback template

### `<Rollback scenario name>`

- **Trigger:** `<when to rollback>`
- **Risk:** `<what is impacted>`
- **Decision owner:** `<who decides>`
- **Rollback steps:**
  1. `<step>`
  2. `<step>`
- **Data considerations:**
  - `<consideration>`
- **Post-rollback verification:**
  - `<check>`
- **Follow-up actions:**
  - `<action>`

## Starter rollback scenarios

### Application deploy introduced regression, schema unchanged

- **Trigger:** public/admin flow is broken after deploy and no migration was involved.
- **Risk:** service degradation without data-shape change.
- **Decision owner:** on-call/release operator.
- **Rollback steps:**
  1. Redeploy the previous known-good application artifact.
  2. Restart affected services.
  3. Re-run smoke verification.
- **Data considerations:** authoritative data should remain valid because schema did not change.
- **Post-rollback verification:** verify login, public standings, and one admin read path.

### Migration succeeded but new app behavior is incorrect

- **Trigger:** the new version is unhealthy after a successful migration.
- **Risk:** old app version may not be compatible with the migrated schema.
- **Decision owner:** release operator plus engineering owner.
- **Rollback steps:**
  1. Determine whether app-only rollback is schema-compatible.
  2. If compatible, redeploy previous app version.
  3. If not compatible, follow the migration-specific recovery plan.
- **Data considerations:** do not guess; migration reversibility must be known before release.
- **Post-rollback verification:** verify both runtime health and domain-critical paths.

## Release history template

| Date | Ref | Environment | Operator | Result | Notes |
|---|---|---|---|---|---|
| `<date>` | `<ref>` | production | `<name>` | success | `<notes>` |

## Repo-specific TODOs

Replace placeholders with:
- exact VPS access method;
- exact Docker Compose commands;
- exact health-check endpoints;
- exact smoke-test sequence;
- exact backup/restore references if any.

## Incident handoff

If deployment fails or causes degraded service, continue in `docs/ops/runbook.md`.
