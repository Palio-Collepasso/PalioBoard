# Open Questions

## Purpose

Keep only unresolved questions here.
This file is not a backlog and not a second product spec.
When a question is answered and the answer is stable, promote it into the authoritative document and remove it from this file.

## Current open questions

### OQ-001 — Public wording for special lifecycle states

**Question**
What public-facing labels should be used for:
- `pending_admin_review`
- `under_examination`

**Why it matters**
These states already have backend semantics, but public/admin UI wording affects operator clarity and public communication.

**Likely target doc once resolved**
- `docs/product/acceptance-scenarios.md`
- frontend copy source, if one is introduced

### OQ-002 — Prepalio tie strategy for the season

**Question**
Which tie strategy should the season use for the Prepalio aggregate ranking when automatic ranking is insufficient or ambiguous?

**Why it matters**
The app supports a configurable strategy, but the concrete seasonal choice affects operator workflow and possible override behavior.

**Likely target doc once resolved**
- `docs/product/functional-requirements.md`
- `docs/domain/business-rules.md`

### OQ-003 — One-time spreadsheet bootstrap or migration

**Question**
Before the first live season, is a one-time import from existing spreadsheets required, or will the first production season be entered directly in the app?

**Why it matters**
This changes whether import tooling or manual bootstrap scripts are part of the delivery scope.

**Likely target doc once resolved**
- `docs/product/prd.md`
- `docs/ops/deploy.md`
- implementation plan docs, if import is needed

### OQ-004 — Final v1 screen map and navigation

**Question**
What is the final v1 screen list and navigation structure for admin, judge, public, and maxi-screen shells?

**Why it matters**
Core flows are defined, but frontend implementation benefits from a settled screen map so agents do not invent competing IA structures.

**Likely target doc once resolved**
- `docs/product/acceptance-scenarios.md`
- frontend architecture docs

## Recently answered and removed from this file

These items are no longer open because they are already settled in authoritative docs:
- authentication approach for v1
- capability-based authorization model
- default seeded role bundles
- live draft recovery direction
- architecture boundary between frontend, backend, DB, and Supabase

See `docs/qna/recently-resolved.md` for the promotion map.
