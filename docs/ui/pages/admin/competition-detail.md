# Competition Detail

## Route

`/admin/competitions/:competition`

## Shell

Use `../../layouts/admin-shell.md`.

## Purpose

Act as the main working page for a single competition. This page consolidates games, standings, history, and Jolly information without splitting them into separate top-level pages.

## Header

- competition name
- short competition-specific explanation
- right-aligned primary action: `Create game`

## Layout

Use the admin shell with a context strip and tabbed primary work area.

1. page header
2. KPI or context strip
3. tab row
4. tab content area
5. optional right rail for quick standings or review context

## Tabs

- `Games`
- `Standings`
- `History`
- `Jolly` for Palio only

## Main blocks

### Context strip

- total games
- in progress
- completed
- pending admin review
- under examination

### Games tab

- game table as the primary surface
- columns: name, format, state, last update, actions
- filters: state, format, mutable or immutable

### Standings tab

- main leaderboard card
- tie-break or ex aequo visibility
- note for games excluded due to under examination
- manual adjustment trigger

For Prepalio also show:

- subgame points leaderboard
- official final Prepalio ranking that feeds Palio

### History tab

- completed game timeline
- recent official changes
- public visibility notes

### Jolly tab

- one row per rione
- used or unused state
- game where used
- points doubled

## Actions

- `Create game`
- row-level `Open`, `Edit`, `Start`
- `Manual adjustment` from the standings tab

## State handling

- Palio-only Jolly tab
- under examination items remain visible but should be clearly marked as excluded from standings
- immutable games should show lock state in tables and row actions

## Responsive behavior

- keep tabs at the top of the work area
- on narrower screens, stack the right rail below the main content
- if tabs overflow, use a horizontal scroller rather than collapsing them into unrelated menus

## Implementation notes

- treat this as the main container page for most admin work
- keep each tab as a heavy primary surface rather than many fragmented cards
- avoid generic sports filters or categories
