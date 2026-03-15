# Audit Log

## Route

`/admin/audit`

## Shell

Use `../../layouts/admin-shell.md`.

## Purpose

Provide authoritative history for result changes, game state changes, Jolly changes, tournament match updates, manual standings adjustments, and user creation.

## Header

- title: `Audit log`
- subtitle emphasizing authoritative history and traceability

## Layout

Use a full-width data-card pattern.

1. page header
2. filter bar
3. expandable audit table

## Main blocks

### Filter bar

- entity type
- game
- actor
- date range
- action type

### Audit table

Suggested columns:

- timestamp
- actor
- entity
- action
- correlation id
- expand control

Expanded state can show:

- before and after summary
- diff payload
- related identifiers

## Actions

- filter
- expand row

There is no page-level primary CTA here.

## State handling

- keep row density readable even with many entries
- expanded rows should remain inside the table card instead of opening a new route by default

## Responsive behavior

- stack filters above the table on smaller widths
- preserve timestamp, entity, and action before dropping lower-priority columns

## Implementation notes

- remove generic infrastructure or unrelated platform audit concepts
- this page should feel operational and forensic, not administrative or marketing-oriented
