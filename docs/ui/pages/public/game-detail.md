# Public Game Detail

## Route

`/games/:id`

## Shell

Use `../../layouts/public-shell.md`.

## Purpose

Provide the public detail page for one game, including metadata, official result, public notes, and current interpretation state.

## Header

Use the public shell top navigation plus a local page title block.

## Layout

Use a single-column public detail layout with an optional supporting history card below.

1. state banner
2. metadata card
3. official placements or result card
4. notes or change-history card

## Main blocks

### State banner

- completed
- pending admin review
- under examination

This banner should also explain counted vs excluded status when relevant.

### Metadata card

- game name
- competition
- format
- last updated
- link back to the competition page

### Result card

- official placements table
- configured public fields
- Jolly if relevant

### Notes or history card

- public notes
- recent change summary when appropriate

## Actions

- `Back to competition`

## State handling

- treat the state banner as mandatory, not optional chrome
- keep the official result visible even when under examination

## Responsive behavior

- keep the state banner above the fold
- preserve the result table readability on small screens with stacked rows if needed

## Implementation notes

- avoid exports or extra features that are not part of v1
- the page should reinforce trust through clarity, not through density
