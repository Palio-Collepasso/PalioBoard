# Maxi Competition Screen

## Route

`/maxi/:competition`

## Shell

Use `../../layouts/maxi-shell.md`.

## Purpose

Provide the large-display presentation view for a competition, optimized for readability at distance.

## Header

Use the compact maxi header ribbon only.

## Layout

Use one dominant full-screen module with a supporting lower strip.

1. header ribbon
2. primary display board
3. secondary strip

## Main blocks

### Primary display board

Choose one mode at a time:

- standings-first board
- current-game board

Do not show both as equal peers.

### Secondary strip

- now playing
- up next
- short provisional note if needed

## Actions

There are no user-facing interactive actions in the normal presentation state.

## State handling

- if standings are provisional, show a high-visibility banner line
- if a game is under examination, explain exclusion directly
- use large readable state labels rather than small badges alone

## Responsive behavior

- target landscape presentation screens first
- preserve safe margins for projector and TV overscan
- remove secondary details before shrinking the primary content

## Implementation notes

- keep to the four rioni only
- avoid dense tables, filters, navigation chrome, or audit detail
- motion should be minimal and only support readability
