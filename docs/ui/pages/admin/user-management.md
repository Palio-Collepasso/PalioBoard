# User Management

## Route

`/admin/settings/users`

## Shell

Use `../../layouts/admin-shell.md`.

## Purpose

Provide the minimal superadmin-only user provisioning surface for v1.

## Header

- title: `Users`
- subtitle clarifying that only seeded roles are assignable in v1
- primary action: `Create user`

## Layout

Use a list-page pattern with one dominant table card.

1. page header
2. optional policy note
3. users table
4. create-user modal or drawer

## Main blocks

### Users table

Suggested columns:

- email
- role
- status
- created date

### Create-user flow

Fields:

- email
- password
- seeded role

## Actions

- `Create user`
- optional row-level status actions only if supported later

## State handling

- if this is the first user, use an empty state with the same `Create user` action
- do not suggest full RBAC editing or self-service account management

## Responsive behavior

- keep the table as the primary surface
- use a modal or drawer for creation instead of a separate full page

## Implementation notes

- keep the surface narrow and administrative
- this page is intentionally minimal in v1
