# Runbook

## Purpose

Provide operational procedures for diagnosing, mitigating, and recovering from PalioBoard production issues.

This starter focuses on the highest-value v1 operational problems:
- app or reverse proxy outage;
- stale public visibility after authoritative changes;
- broken live ranking collaboration;
- failed deploy/migration;
- suspected standings mismatch.

## Usage rules

- Prefer the least risky mitigation first.
- Record what changed, who changed it, and why.
- If a step risks data loss or downtime, state that explicitly.
- Distinguish operational recovery from business-policy decisions.

## Contacts / ownership

Populate with the real team/person ownership.

| Area | Owner | Escalation |
|---|---|---|
| application | `<owner>` | `<path>` |
| database | `<owner>` | `<path>` |
| infrastructure | `<owner>` | `<path>` |
| event operations | `<owner>` | `<path>` |

## Incident severity guide

| Severity | Meaning | Typical response target |
|---|---|---|
| SEV-1 | Full outage or core event operation unavailable | immediate |
| SEV-2 | Major degraded behavior in a core workflow | urgent |
| SEV-3 | Limited issue or workaround exists | normal urgent |

## Runbook item index

| Runbook ID | Problem | Severity range | Owner |
|---|---|---|---|
| `RB-001` | Application unavailable or reverse proxy failure | SEV-1 | application / infra |
| `RB-002` | Public standings/results are stale after official change | SEV-2 | application |
| `RB-003` | Live ranking collaboration broken or conflict storm | SEV-2 | application |
| `RB-004` | Deploy or migration failure | SEV-1 to SEV-2 | application / database |
| `RB-005` | Suspected standings mismatch | SEV-2 | application / event operations |

---

## Active runbook items

### `RB-001` — Application unavailable or reverse proxy failure

- **Status:** `active`
- **Severity range:** `SEV-1`
- **Owner:** `application / infra`
- **Last reviewed:** `<date>`

#### Symptoms

- public, admin, and maxi routes fail to load;
- health endpoints fail or time out;
- operators cannot perform event workflows.

#### Detection

- **How to detect:**
  - user reports;
  - uptime/health failure;
  - Nginx or backend process alerts.
- **Dashboards/logs/tools:**
  - reverse proxy logs;
  - backend container logs;
  - VPS process/container status.

#### Likely causes

- backend container/process crashed;
- Nginx misconfiguration or failed restart;
- database connectivity failure causing backend startup failure.

#### Immediate safety checks

- [ ] Confirm whether the outage affects only admin, only public, or the whole system.
- [ ] Check whether the database is reachable before restarting repeatedly.
- [ ] Avoid ad hoc manual file edits on the VPS without recording them.

#### Mitigation steps

1. Check container/process status for Nginx, backend, and database dependencies.
2. Restart only the failed component first if the cause is obvious.
3. If the release caused the outage, consider rollback using `docs/ops/deploy.md`.

#### Recovery steps

1. Restore a healthy backend and reverse proxy state.
2. Re-verify public, admin, and maxi reachability.
3. Confirm at least one safe authenticated read path works.

#### Verification after recovery

- [ ] Public landing page loads.
- [ ] Admin login page loads.
- [ ] Backend health endpoint is healthy.
- [ ] Logs stop showing the original failure pattern.

#### Escalation

- **Escalate when:** repeated restarts do not restore service quickly, or DB access is implicated.
- **Escalate to:** application + database owner.

#### Communication

- **Who to notify:** operators, engineering, event leads if live.
- **What to communicate:** outage scope, current mitigation, estimated next decision point.
- **Update cadence:** every meaningful change during active incident.

#### Data / audit considerations

- restart actions are operational and not business-audit events;
- avoid manual DB edits unless explicitly authorized and recorded.

#### Follow-up work

- root-cause analysis;
- add missing monitoring/alerting;
- improve startup or health diagnostics if the cause was unclear.

### `RB-002` — Public standings/results are stale after official change

- **Status:** `active`
- **Severity range:** `SEV-2`
- **Owner:** `application`
- **Last reviewed:** `<date>`

#### Symptoms

- admin shows a completed or edited official result, but public/maxi still shows older data;
- standings or state badge appear inconsistent with the latest authoritative workflow.

#### Detection

- **How to detect:**
  - operator comparison between admin and public views;
  - smoke check after completion or review-state change.
- **Dashboards/logs/tools:**
  - backend logs around projection recompute and public-read refresh;
  - browser/network logs if realtime refresh is involved.

#### Likely causes

- projection/read-model recompute did not happen;
- transaction rolled back but operator misread partial UI state;
- public refresh/realtime path is broken.

#### Immediate safety checks

- [ ] Confirm the authoritative game state in admin/API first.
- [ ] Confirm whether the issue is stale read-model data or only a client refresh issue.
- [ ] Confirm whether the game is `pending_admin_review` or `under_examination`, since visibility and counting differ.

#### Mitigation steps

1. Verify whether the authoritative write committed successfully.
2. Verify whether the public read model was recomputed.
3. If the backend state is correct but clients are stale, force a safe refresh path.
4. If projections are actually stale, treat this as a correctness incident and escalate.

#### Recovery steps

1. Restore fresh public read-model visibility using the safest available supported mechanism.
2. Re-verify the affected game and standings on both admin and public sides.

#### Verification after recovery

- [ ] Public results match admin authoritative state.
- [ ] Counting/non-counting state matches the game state.
- [ ] No further stale-update reports appear for subsequent smoke checks.

#### Escalation

- **Escalate when:** authoritative and public states diverge or recompute appears broken.
- **Escalate to:** application owner and event operations owner.

#### Communication

- **Who to notify:** operators and engineering.
- **What to communicate:** whether the issue is visibility-only or a true correctness issue.
- **Update cadence:** on discovery, mitigation, and recovery.

#### Data / audit considerations

- do not “fix” public mismatch by editing projections manually unless there is an approved operational procedure;
- preserve evidence for root-cause analysis.

#### Follow-up work

- add or strengthen smoke checks around authoritative change → public visibility;
- improve instrumentation for recompute and public refresh.

### `RB-003` — Live ranking collaboration broken or conflict storm

- **Status:** `active`
- **Severity range:** `SEV-2`
- **Owner:** `application`
- **Last reviewed:** `<date>`

#### Symptoms

- editors cannot obtain leases;
- editors receive repeated stale-write or lock errors unexpectedly;
- live ranking sessions diverge badly after reconnect.

#### Detection

- **How to detect:**
  - judge/operator reports during an in-progress ranking game;
  - abnormal realtime error volume.
- **Dashboards/logs/tools:**
  - backend realtime logs;
  - client console/network traces;
  - current live-draft state inspection if available.

#### Likely causes

- stuck or stale leases;
- broken live revision handling;
- backend restart/reconnect path not restoring expected state.

#### Immediate safety checks

- [ ] Confirm the affected game is a ranking game in `in_progress`.
- [ ] Confirm authoritative official state is still intact.
- [ ] Avoid manual authoritative rewrites while diagnosing live collaboration.

#### Mitigation steps

1. Determine whether the issue affects one game or all live ranking games.
2. Have operators refresh to recover the latest server state if the issue is isolated client staleness.
3. If leases appear stuck, use only approved recovery procedures for clearing or expiring them.
4. If live collaboration remains unusable, decide whether to continue via a controlled manual workflow.

#### Recovery steps

1. Restore healthy live-edit behavior or shift temporarily to the approved fallback process.
2. Verify a full conflict/retry cycle with two sessions.
3. Verify completion still materializes the intended authoritative result correctly.

#### Verification after recovery

- [ ] Two sessions can reproduce correct lock/conflict behavior.
- [ ] No silent overwrite occurs.
- [ ] Completion still works after recovery.

#### Escalation

- **Escalate when:** multiple games are affected, or operators cannot continue the event safely.
- **Escalate to:** application owner and event lead.

#### Communication

- **Who to notify:** operators using live entry, engineering.
- **What to communicate:** affected games, workaround/fallback, expected operator behavior.
- **Update cadence:** whenever mitigation changes.

#### Data / audit considerations

- live draft state is not authoritative truth;
- if fallback requires direct official entry, keep the transition explicit and auditable.

#### Follow-up work

- reproduce with `FX-003` or equivalent fixture;
- add missing realtime integration coverage if the cause was not already protected.

### `RB-004` — Deploy or migration failure

- **Status:** `active`
- **Severity range:** `SEV-1 to SEV-2`
- **Owner:** `application / database`
- **Last reviewed:** `<date>`

#### Symptoms

- deploy process halts;
- application fails after migration;
- old version and new schema appear incompatible.

#### Detection

- **How to detect:**
  - deploy output and logs;
  - failed smoke checks immediately after deploy.
- **Dashboards/logs/tools:**
  - deploy logs;
  - migration logs;
  - backend startup logs.

#### Likely causes

- failed migration;
- missing configuration;
- schema-app incompatibility;
- incomplete or incorrect release artifact.

#### Immediate safety checks

- [ ] Stop and assess before repeated partial retries.
- [ ] Determine whether the database schema changed already.
- [ ] Determine whether app-only rollback is safe.

#### Mitigation steps

1. Halt further rollout until the state is understood.
2. Decide between fixing forward and rollback based on schema compatibility.
3. Follow the rollback or recovery procedure from `docs/ops/deploy.md`.

#### Recovery steps

1. Restore a known-good deploy state.
2. Re-run smoke verification.
3. Record exactly what failed and at what step.

#### Verification after recovery

- [ ] App is reachable.
- [ ] Health checks pass.
- [ ] Public/admin smoke flows succeed.
- [ ] Migration state is understood and documented.

#### Escalation

- **Escalate when:** migration compatibility is unclear or data safety is at risk.
- **Escalate to:** database owner and engineering lead.

#### Communication

- **Who to notify:** engineering and operators.
- **What to communicate:** whether the system is down, degraded, or rolled back.
- **Update cadence:** at each deploy decision point.

#### Data / audit considerations

- document any manual data/schema intervention explicitly;
- do not improvise destructive rollback steps.

#### Follow-up work

- improve deploy rehearsal and migration notes;
- add missing smoke or precondition checks.

### `RB-005` — Suspected standings mismatch

- **Status:** `active`
- **Severity range:** `SEV-2`
- **Owner:** `application / event operations`
- **Last reviewed:** `<date>`

#### Symptoms

- operators or judges believe the displayed standings do not match official results;
- public standings differ from expected manual calculation.

#### Detection

- **How to detect:**
  - operator report;
  - failed verification after an authoritative workflow.
- **Dashboards/logs/tools:**
  - admin result view;
  - projection/read-model inspection tools;
  - audit trail for recent authoritative changes.

#### Likely causes

- misunderstanding of counting semantics (`pending_admin_review` vs `under_examination`);
- Jolly or manual adjustment not accounted for as expected;
- true projection bug or stale read model.

#### Immediate safety checks

- [ ] Verify the game states of all recently changed games.
- [ ] Verify whether any affected game is under examination.
- [ ] Verify Jolly usage and manual adjustments explicitly.

#### Mitigation steps

1. Reconstruct the expected standings from authoritative inputs only:
   - completed games;
   - pending-admin-review games;
   - valid Jolly inputs;
   - manual adjustments;
   - Prepalio aggregate contribution where relevant.
2. Compare the reconstruction with the displayed projection.
3. Decide whether the issue is misunderstanding, stale read-model data, or a true calculation bug.

#### Recovery steps

1. If it is a misunderstanding, document and communicate the correct interpretation.
2. If it is stale visibility, recover the public/read-model freshness.
3. If it is a true calculation issue, treat it as a correctness incident and involve engineering immediately.

#### Verification after recovery

- [ ] Recomputed understanding matches displayed standings.
- [ ] Public/admin projections agree.
- [ ] No hidden manual adjustment or Jolly discrepancy remains unexplained.

#### Escalation

- **Escalate when:** the mismatch cannot be explained from authoritative inputs.
- **Escalate to:** engineering owner plus event operations owner.

#### Communication

- **Who to notify:** operators, engineering, event leads if live.
- **What to communicate:** whether the issue was visibility, interpretation, or actual correctness.
- **Update cadence:** after diagnosis and after resolution.

#### Data / audit considerations

- use audit records and authoritative entities as evidence;
- do not mutate projection tables manually as a first response.

#### Follow-up work

- add a regression test for the scenario;
- improve operator guidance for counting-state semantics if the issue was interpretive.

## Standard incident timeline template

- **Start time:** `<timestamp>`
- **Detection time:** `<timestamp>`
- **First mitigation:** `<timestamp>`
- **Recovery time:** `<timestamp>`
- **Resolved by:** `<name>`
- **Summary:** `<summary>`

## Post-incident review template

### `<Incident title>`

- **Date:** `<date>`
- **Severity:** `<severity>`
- **Impact:** `<impact>`
- **Root cause:** `<cause>`
- **What worked well:**
  - `<item>`
- **What did not work well:**
  - `<item>`
- **Action items:**
  - `<item>`
