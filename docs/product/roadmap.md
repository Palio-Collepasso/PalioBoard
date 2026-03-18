# Roadmap

## Purpose
Provide the maintained high-level roadmap summary for the active documentation set.

Use this document for:
- the current milestone order
- short milestone summaries
- links from onboarding and repo-level docs

This file is the active concise roadmap. Historical planning notes belong in archive or task-specific planning docs only when they are still useful.

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

## How to maintain
- Keep this file short.
- Update it when milestone order or milestone meaning changes.
- Put task-level execution detail, dependencies, and one-off planning notes outside the active roadmap surface.
