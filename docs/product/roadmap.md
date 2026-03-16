# Roadmap

## Purpose

Provide the maintained high-level roadmap summary for the active documentation set.

Use this document for:
- the current milestone order
- short milestone summaries
- links from onboarding and repo-level docs

Use `docs/_raw/milestones.md` as the long-form source record for detailed dependencies, exit criteria, and risks.

## Milestone Index

| Milestone | Title | Summary |
|---|---|---|
| `m-0` | Delivery foundation and architecture skeleton | Stand up the monorepo skeleton, schema and migrations, same-origin local stack, quality gates, and architectural guardrails. |
| `m-1` | Identity, authorization, and season setup | Add auth integration, roles and capabilities, user provisioning, and the season, team, and game setup flows. |
| `m-2` | Trusted ranking result backbone | Deliver authoritative ranking result entry, validation, audit, projection recompute, and initial public reads. |
| `m-3` | Live ranking operations and collaboration safety | Add in-progress ranking workflows, live drafts, leases, stale-write protection, and reconnect or restart recovery. |
| `m-4` | Advanced standings rules: Jolly, Prepalio, Giocasport, adjustments | Implement competition-specific scoring rules, Jolly constraints, Prepalio roll-up, Giocasport separation, and manual adjustments. |
| `m-5` | 1v1 tournament workflow | Deliver semifinal pairings, match progression, derived final ranking, override handling, and leaderboard impact on completion. |
| `m-6` | Trust and exception workflows | Add post-completion review, under-examination handling, audit visibility, and the related trust-protection flows. |
| `m-7` | Public or maxi completion and release hardening | Complete read-only experiences, tighten operations, and finish the acceptance-level release pass. |

## Source Note

Keep this summary concise. If milestone ordering, dependencies, exit criteria, or risks change materially, update the long-form source in `docs/_raw/milestones.md` and then refresh this summary.
