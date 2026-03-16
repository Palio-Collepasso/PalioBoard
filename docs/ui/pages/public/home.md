# Public Home

## Route

`/`

## Shell

Use `../../layouts/public-shell.md`.

## Purpose

Provide the public entry point into the event, with quick access to the three competition contexts and a small live snapshot.

## Header

Handled by the public shell top navigation.

## Layout

Use the public shell with a hero-first composition.

1. hero or intro block
2. three competition cards
3. live snapshot card
4. footer

## Main blocks

### Hero block

- event title
- short explanation
- note that the site shows official public results

### Competition cards

- Palio
- Prepalio
- Giocasport

Each card should include:

- short description
- small standings or status hint
- `Open competition` action

### Live snapshot

- current Palio standings or latest official updates
- last updated timestamp

## Actions

- `Open competition`

## State handling

- if there are no results yet, keep the competition cards and show a neutral pre-event message
- if public data is provisional, explain why in the snapshot block

## Responsive behavior

- desktop: hero first, then cards in a row, then snapshot
- mobile: stack cards vertically and keep the live snapshot close to the top

## Implementation notes

- keep the page content-led, not tool-like
- do not leak admin concepts or workflow actions into the public home
