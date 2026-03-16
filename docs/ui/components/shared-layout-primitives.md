# Shared Layout Primitives

These rules are shared by the `/admin`, `/public`, and `/maxi` shells. Split them once here so the shell docs can stay focused on structure.

## Source of truth

When a shell doc gives a visual rule and `docs/ui/design_tokens.json` already defines a token for it, prefer the token file as the exact source of truth.

Useful token groups:

- colors: `color.*`
- typography: `font.textStyle.*`
- spacing: `space.*`
- fixed dimensions: `size.*`
- radius: `radius.*`
- shadow: `shadow.*`
- shared layout values: `layout.admin.*`, `layout.public.*`

Use `docs/ui/component_checklist.md` as the implementation checklist for these primitives.

## Visual baseline

Use the extracted template and token file as the common visual system.

- app background: `color.background.app`
- surface background: `color.background.surface`
- primary accent: `color.brand.primary.500`
- heading text: `color.text.primary`
- secondary text: `color.text.secondary`
- border: `color.border.default`
- standard card radius: `radius.lg`
- standard card padding: `space.cardPadding`

The system should read as white cards on a soft neutral canvas, with orange used as the single strong accent.

## Shared surfaces

### Primary surface card

Use for:

- main tables
- standings cards
- hero cards
- main work surfaces

Rules:

- white background
- subtle border
- large radius
- minimal shadow using `shadow.card`

### Context surface

Use for:

- summary cards
- secondary explanations
- quick state notes

Rules:

- can use very light tinted backgrounds
- must stay lighter than warning or error banners

### Alert or state surface

Use for:

- provisional messages
- under examination notes
- validation blockers

Rules:

- color tint must match the state semantics
- message should be short and explicit

## Shared content blocks

### Section header

Structure:

- title
- one-line explanation
- optional right-aligned action

Use across admin cards and public sections. On maxi, use a larger simplified variant.

### Summary card

Structure:

- short label
- prominent value
- optional icon or state chip

Use only for high-signal counts or status, not decorative analytics.

### Data card

Structure:

- card title row
- optional filters or controls
- table or list body

Use as the default wrapper for tables and repeatable lists.

### Standings card

Structure:

- title
- ranking rows
- optional note on provisional logic

This should be a first-class primitive because standings appear in admin, public, and maxi with different density.

## Shared status language

Keep state names and meaning identical across shells.

- `draft`: neutral, not yet active
- `in progress`: active live work
- `completed`: official and counted
- `pending admin review`: visible and counted, awaiting admin decision
- `under examination`: visible, not counted

Never change the wording by shell. Only change the density and emphasis.

## Shared badges and banners

### Badge

Use for inline state markers inside tables, cards, and headers.

Rules:

- pill shape
- semibold label
- compact padding
- tint background, do not rely on border alone

### Banner

Use when the state changes how the audience should interpret the content.

Examples:

- a public standings page is provisional because a game is under examination
- an admin game workbench has completion blockers
- a maxi screen needs to state that standings exclude a disputed game

## Shared interaction hierarchy

- one dominant CTA per region
- secondary actions stay neutral
- destructive actions must be visually separated

This matters most in admin, but it keeps public and maxi from becoming visually noisy too.

## Shared component split guidance

Split a component only when it is reused by more than one shell or by multiple routes inside the same shell.

Good shared candidates:

- status badge
- state banner
- section header
- summary card
- standings card base

Do not force shell-specific navigation or route-specific work surfaces into the shared layer.

## Checklist mapping

These checklist sections should be treated as directly covered by this document:

- `1.1` to `1.5` Foundations
- `2.3` Layout primitives
- `5.1` Cards
- `5.2` Badges and chips
- `6.1` Inline states
- `6.3` Empty/error/loading states
