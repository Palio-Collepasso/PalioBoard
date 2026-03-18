# Palio Context

## Purpose

This document gives agents the minimum real-world context needed to understand the product and domain language.
It is not the official seasonal regulation and it is not a second source of business truth.
Use it for vocabulary and event framing, then rely on authoritative product/domain docs for software behavior.

## Event summary

Palio is a town event in Collepasso where four teams (`rioni`) compete across a set of games.
The event is run as a points-based competition: each game produces a ranked result, that result maps to points, and the sum of those points determines standings.

The four teams are:
- Bosco
- Tafuri
- Carrozzini
- Castello

The event is divided into three competition contexts used by the software:
- `palio`
- `prepalio`
- `giocasport`

## Why this matters to the software

Agents should keep these practical implications in mind:
- the team count is fixed in v1
- the competition context affects rules such as Jolly and aggregate scoring
- games may be ranking games or fixed 1v1 tournaments
- some public wording comes from event language (`rione`, `Palio`, `Prepalio`, `Giocasport`), but implementation rules live elsewhere

In v1 the software assumes exactly one active season per database, exactly four teams, and exactly these three competition contexts.

## Vocabulary

| Term | Meaning in the event | Software meaning |
|---|---|---|
| `rione` | one of the four town teams | `team` record in the current season |
| Palio | main event competition | competition type `palio` |
| Prepalio | preliminary set of competitions | competition type `prepalio` plus aggregate ranking contribution |
| Giocasport | youth/children competition area | competition type `giocasport` |
| Jolly | one game chosen by a team for doubled points | per-team official flag on Palio games only |
| under examination | a disputed/suspended result state | visible publicly but excluded from standings |
| pending admin review | a post-edit control state | latest official result still counts |

## External regulation summary relevant to v1

The official regulation contains much more detail than the software models directly.
Only these parts materially affect the v1 domain shape:

### Team belonging and participation
The regulation defines how athletes belong to a `rione`, when exceptions are allowed, and participation constraints.
The v1 dashboard does not model full athlete registration or eligibility workflows as core business objects.
Treat those rules as external operational context unless a later requirement brings them into the app.

### Game schedule and catalog
The yearly regulation defines the concrete list of games for the season.
In the app, games are configured in season setup and can use seeded field-catalog entries.
The regulation is a source for what the organizers want to configure, not a direct substitute for app configuration.

### Points and standings
The regulation uses ranked outcomes that map to points.
In the app, the points table is configured per game and official standings are derived from canonical per-team results plus adjustments.

### Jolly
Each team may designate one Palio game as Jolly, doubling the points earned in that game.
In software terms:
- Jolly is only valid for `palio`
- it is stored on the canonical official team result
- a team may use it at most once across Palio games

### Tie handling
The regulation may define or allow tie-handling behavior in some contexts.
The software supports explicitly entered tied placements and a configurable Prepalio tie strategy.
Season-specific tie policy should be defined in authoritative product/domain docs, not inferred from this summary.

### Disputes and review
The real event allows disputes, review, and organizer judgment.
The software models this through lifecycle states such as `under_examination` and `pending_admin_review`, with distinct leaderboard effects.

## What this document does not define

This file does not define:
- the official yearly rule text
- exact screen behavior
- exact API behavior
- scoring formulas beyond what authoritative docs say
- athlete registration, rostering, or eligibility workflows
- detailed schedule or per-game real-world instructions

## Where authoritative software truth lives

Use these files for implementation:
- `docs/product/prd.md` — scope and non-goals
- `docs/product/functional-requirements.md` — required software behavior
- `docs/domain/business-rules.md` — stable domain rule catalog
- `docs/domain/er-schema.md` — structural model
- `docs/architecture/architecture.md` — source of truth, invariants, lifecycle, boundaries

## Source materials

This summary was derived from the event description and the 2025 regulation.
Keep the raw regulation or detailed seasonal notes in archive/ material rather than turning this file into a long transcript.
