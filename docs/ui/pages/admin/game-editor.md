# Game Create or Edit

## Route

- `/admin/games/new`
- `/admin/games/:id/edit`

## Shell

Use `../../layouts/admin-shell.md`.

## Purpose

Provide one editor for both supported formats: ranking and fixed four-team `1v1 tournament`.

## Header

- title changes between `Create game` and `Edit game`
- subtitle explaining the competition and format choice
- back action to the relevant competition detail page

## Layout

Use the form-plus-preview pattern with a sticky footer.

1. page header
2. two-column content area
3. sticky save zone at the bottom

Recommended split:

- left: form cards
- right: points preview, rules, immutable warnings

## Main blocks

### Identity and placement card

- game name
- competition selector with only `Palio`, `Prepalio`, `Giocasport`
- format selector with only `ranking` and `1v1 tournament`

### Configured fields card

- seeded field catalog choices
- required-field visibility
- public notes inclusion if enabled

### Points mapping preview

- default `4,3,2,1` presentation
- ex aequo note
- competition-specific warnings

### Format help card

- ranking-specific help for field entry
- tournament-specific note that pairings are set in operations, not setup

## Actions

- `Save game`
- `Cancel`

## State handling

- if official result data exists, show immutable state immediately and disable result-affecting edits
- when editing a Palio game, keep Jolly messaging in the help or preview area, not as a setup field
- for tournament format, do not expose pairing entry here

## Responsive behavior

- desktop: `7/5` split
- tablet: stack preview below the form
- keep the save zone sticky even after the layout stacks

## Implementation notes

- this doc covers both create and edit because the layout is the same
- the editor configures a game definition; it does not handle live result entry
