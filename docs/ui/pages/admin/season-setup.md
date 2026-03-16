# Season Setup

## Route

`/admin/season`

## Shell

Use `../../layouts/admin-shell.md`.

## Purpose

Provide the minimal season configuration view for the active season, including season identity and the four fixed rioni.

## Header

- title: `Season setup`
- subtitle describing the single-season constraint
- no primary CTA in the header unless there is a season-level save action outside the form

## Layout

Use the form-plus-preview pattern from the admin shell.

1. page header
2. two-column main area
3. sticky bottom action bar when edits are allowed

Recommended split:

- left: main form and team table
- right: rules/help card and lock-state summary

## Main blocks

### Season identity card

- season year label
- season name

### Teams or rioni card

- exactly four rows
- rione name
- color token
- edit action
- lock state

### Rules/help card

- fixed competition contexts
- fixed number of rioni
- immutability after official results exist

## Actions

- `Save changes`
- row-level `Edit rione`

Use a modal or side panel for rione editing rather than navigating away.

## State handling

- when results exist, lock fields that would break official history
- show lock reasons inline, not only on submit
- if no season exists yet, keep the same layout and show empty defaults rather than a separate experience

## Responsive behavior

- desktop: `7/5` form-plus-preview split
- tablet: stack help below the editable content
- keep the sticky action bar visible whenever the page is editable

## Implementation notes

- the rioni table is part of this page, not a separate route
- keep the page narrow in scope; do not add global points configuration or generic catalog management here
