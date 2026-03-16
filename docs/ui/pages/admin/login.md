# Login Page

## Route

Recommended route: `/login`

## Shell

Standalone auth surface. This page does not use the persistent `/admin` shell chrome from `../../layouts/admin-shell.md`.

## Purpose

Provide a single, minimal entry point for admin, judge, and superadmin users. The page should authenticate the user and hand off into the admin shell after success.

## Header

- small PalioBoard mark
- short title such as `Sign in`
- one-line support text

Do not add role switching, competition summaries, or public-site navigation.

## Layout

Use a centered auth card on the neutral app background.

1. full-height viewport with centered content
2. single card around the form
3. optional small help link below the card

## Main blocks

- email field
- password field
- primary `Sign in` button
- inline error area
- optional future placeholder for password reset link

## Actions

- `Sign in`

No secondary CTA should compete with the sign-in action.

## State handling

- invalid credentials show inline error text inside the card
- pending submission disables inputs and shows loading on the primary button
- authenticated users should redirect away from this page

## Responsive behavior

- keep the card narrow on desktop
- on mobile, let the card grow to near full width while preserving generous padding

## Implementation notes

- keep branding minimal
- use the same button, input, and alert primitives as the admin shell
- this page should visually lead into the admin shell without copying its sidebar/topbar
