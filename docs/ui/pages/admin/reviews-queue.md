# Reviews Queue

## Route

`/admin/reviews`

## Shell

Use `../../layouts/admin-shell.md`.

## Purpose

Provide the single queue for exceptional workflows: `pending admin review` and `under examination`.

## Header

- title: `Reviews`
- subtitle clarifying that this page handles disputed or exceptional result states

## Layout

Use a full-width data-card layout with tabs or segmented state filters.

1. page header
2. filter and state-tab row
3. queue table

## Main blocks

### State tabs

- `Pending admin review`
- `Under examination`

### Filter row

- competition filter
- state filter when useful
- search by game name if needed

### Queue table

Suggested columns:

- competition
- game
- current state
- leaderboard effect
- submitted or updated by
- timestamp
- primary action

## Actions

- row-level `Open review`

Keep actions focused. This page is for triage and queue management, not direct inline editing.

## State handling

- make the leaderboard effect explicit: counted vs excluded
- elevate the active state tab visually
- empty states should be state-specific, not generic

## Responsive behavior

- keep filters above the table on narrower widths
- collapse secondary columns before collapsing the primary action

## Implementation notes

- avoid generic appeals-management language that suggests a separate product area
- the page should feel like a queue, not like a dashboard
