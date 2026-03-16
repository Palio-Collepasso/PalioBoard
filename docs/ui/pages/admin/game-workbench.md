# Game Workbench

## Route

`/admin/games/:id`

## Shell

Use `../../layouts/admin-shell.md`.

## Purpose

Provide the single operational page for live result entry, tournament progression, completion, and exception-state handling.

## Header

- game name
- competition
- format
- state badge
- last updated timestamp

Right-aligned actions:

- `Start game`
- `Complete game`
- `Mark under examination`
- `Resolve`
- `View audit`

## Layout

Use the split workbench pattern.

1. rich page header
2. optional state or warning banner
3. main work surface
4. context rail with validation and impact
5. sticky completion/action bar when needed

Recommended split:

- main work surface: `8 columns`
- context rail: `4 columns`

## Main blocks

### Ranking mode

Use a full-width entry grid with one row per rione.

Columns can include:

- rione
- Jolly for Palio only
- placement
- configured fields
- public notes
- collaboration or lock cues

### Tournament mode

Use a bracket-centered layout.

Blocks:

- semifinal pairings area before start
- tournament bracket after start
- derived placements preview
- override area only where allowed

### Context rail

- validation blockers
- quick standings impact
- state notes
- audit summary

## Actions

- start and completion actions in the header or sticky footer
- row-level save behavior for ranking edits if live saving is supported
- tournament winner entry actions inside match cards

## State handling

- ranking mode shows stale revision and field lock cues
- tournament match saves are official immediately, but standings update only when the whole game is completed
- under examination keeps the result visible but excluded from standings
- pending admin review remains counted

## Responsive behavior

- on narrow screens, move the context rail below the main work surface
- preserve the bracket readability before collapsing to stacked match cards
- keep completion actions sticky even when the workbench stacks

## Implementation notes

- this is the highest-density page in the app and should still have one dominant work surface
- do not treat ranking and tournament as separate route-level pages; they are two modes of one workbench
