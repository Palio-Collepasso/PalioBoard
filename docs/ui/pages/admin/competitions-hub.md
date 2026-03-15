# Competitions Hub

## Route

`/admin/competitions`

## Shell

Use `../../layouts/admin-shell.md`.

## Purpose

Provide the operational landing page for authenticated users. This is the first admin page after login and the main entry point into the three fixed competition contexts.

## Header

- title: `Competitions`
- subtitle explaining that the page is the season control hub
- no generic dashboard analytics

Optional right-aligned action:

- `Season setup` or another season-level shortcut if needed

## Layout

Use a full-width admin page with one dominant card row followed by one attention surface.

1. page header
2. compact season context strip
3. three competition cards in a single row on desktop
4. review and under-examination attention strip below

## Main blocks

### Season context strip

- current season name or year
- fixed count of competitions
- small note that the system operates on one active season

### Competition cards

One card each for:

- Palio
- Prepalio
- Giocasport

Each card should contain:

- competition name
- short description
- total games
- in progress count
- completed count
- under examination count
- primary `Open competition` action

### Attention strip

Show only high-signal alerts:

- pending admin review count
- under examination count
- optional shortcut to `/admin/reviews`

## Actions

- `Open competition`
- `Open reviews`

Do not place `Create competition` here. Competition contexts are fixed.

## State handling

- if there are no games yet, cards still exist and show an empty-state message
- if review counts are non-zero, elevate the attention strip visually
- use the shared state badge language for live or disputed counts

## Responsive behavior

- desktop: 3 equal cards in one row
- narrow laptop/tablet: cards stack to `2 + 1` or one per row
- keep the attention strip below the cards rather than moving it into the sidebar

## Implementation notes

- this page is a hub, not a metrics dashboard
- the three cards should be fixed in order and always visible
- keep the first click path obvious: enter one competition and start working
