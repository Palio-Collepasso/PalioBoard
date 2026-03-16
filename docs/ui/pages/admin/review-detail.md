# Review Detail

## Route

`/admin/reviews/:gameId`

## Shell

Use `../../layouts/admin-shell.md`.

## Purpose

Let an admin inspect a post-completion edit or disputed result in detail and decide whether to approve or reject it.

## Header

- game name
- competition
- current state badge
- last updated timestamp

## Layout

Use the split workbench pattern with a dominant diff view and a compact decision rail.

1. page header
2. top summary strip
3. before/after diff view
4. sticky or pinned decision box

Recommended split:

- diff view: `8 columns`
- decision rail: `4 columns`

## Main blocks

### Summary strip

- changed by
- changed at
- reason text
- current leaderboard effect

### Diff view

- placements before and after
- field values before and after
- Jolly before and after
- state changes if relevant

### Decision rail

- approve action
- reject or revert action
- short audit trail excerpt

## Actions

- `Approve`
- `Reject` or `Revert`

These actions should stay visible while the diff scrolls.

## State handling

- preserve the current counted or excluded meaning on screen while the admin reviews
- use clear visual diff treatment without introducing noisy code-review styling

## Responsive behavior

- stack the decision rail below the diff when width is limited
- keep the decision actions sticky near the viewport edge

## Implementation notes

- compare Palio-specific fields only
- avoid generic sports statistics or player-centric comparison blocks
