# Public Competition Page

## Route

`/competition/:competition`

## Shell

Use `../../layouts/public-shell.md`.

## Purpose

Provide the public read-only view for a single competition, combining standings, results, history, and Jolly summary where relevant.

## Header

Use the public shell top navigation plus a competition title block.

## Layout

Use the public shell with tabs and one dominant content surface.

1. competition title or snapshot block
2. competition switch
3. tab row
4. primary card
5. optional supporting rail or stacked secondary content

## Tabs

- `Standings`
- `Results`
- `History`
- `Jolly` for Palio only

## Main blocks

### Standings tab

- official leaderboard
- provisional note when relevant
- note for excluded games under examination

### Results tab

- game list
- latest official state
- last updated timestamps

### History tab

- recent public-facing changes
- appeal or review outcomes if public

### Jolly tab

- Palio only
- one row per rione
- used or unused state

## Actions

- competition switch
- `Open game detail`

Public actions remain navigational, not operational.

## State handling

- `pending admin review` remains visible and counted
- `under examination` remains visible but excluded from standings
- explain state meaning directly in banners or helper text

## Responsive behavior

- keep the competition switch near the top
- move secondary content below the main card on narrower screens
- allow tabs to scroll horizontally if needed

## Implementation notes

- avoid generic sports widgets or player-centric modules
- the first screenful should make the official public picture clear
