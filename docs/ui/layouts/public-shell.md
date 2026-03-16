# Public Shell Layout

## Purpose

The `/public` shell covers the read-only audience experience. It should feel lighter than admin, but it still has to communicate trust, official state, and competition context clearly.

This shell covers routes such as:

- `/`
- `/competition/:competition`
- `/games/:id`

## Core principles

- Lead with standings, official results, and latest updates.
- Make provisional states explicit and easy to understand.
- Keep the visual language consistent with admin without inheriting admin density.
- Use larger content blocks and fewer controls.
- Reuse shared primitives from `../components/shared-layout-primitives.md`.

Checklist anchors:

- `component_checklist.md` sections `2.2`, `2.3`, `3.3`, and `8.5`

## Persistent shell structure

### 1. Top navigation

Use a simple top navigation bar instead of the admin sidebar.

- Height: `72px`
- Left: brand and event identity
- Center or right: competition switch or route tabs when useful
- Right: secondary utilities only if needed

Do not expose admin concepts or operational actions here.

### 2. Main content container

Use a centered wide container with more breathing room than admin.

- Max width: `layout.public.containerMaxWidth` (`1280px`)
- Horizontal padding: `24-32px`
- Vertical section gaps: `24-40px`, using `layout.public.heroGap` where the hero needs extra separation
- Background: same soft neutral app background as admin

Default composition:

1. hero or context block
2. competition navigation or state banner
3. primary standings/results surface
4. supporting history or secondary content
5. footer

### 3. Footer

Keep the footer quiet and informational.

- legal or support links
- event identity
- optional timestamp or update policy

It should not compete with the main content.

## Layout regions

### Hero or snapshot block

Use the first surface on a page to answer one of these questions:

- what competition is this?
- what is happening now?
- what is the latest official picture?

Home page example:

- event intro
- three competition cards
- small live snapshot

Competition page example:

- competition title
- short explanation
- state note if any games are provisional or excluded

### Competition switch

Competition context should be explicit and easy to change.

Recommended patterns:

- horizontal tabs for `Palio`, `Prepalio`, `Giocasport`
- segmented control for smaller screens

This switch belongs near the top of the page, not buried inside cards.

### Primary content surface

The main surface should usually be one of:

- standings card
- results list
- game detail card

Use one dominant card first, then supporting cards below or beside it.

### Secondary content rail

Use a secondary column only when it adds clear value.

Examples:

- latest updates
- explanation of provisional states
- recent history
- next or latest game

Recommended ratio on wide screens:

- main content: `8 columns`
- secondary rail: `4 columns`

If the secondary rail weakens readability, stack it below the main content.

## State presentation

The public shell is where trust messaging matters most.

Every relevant page should surface:

- current game or competition state
- last updated timestamp
- whether standings are official or provisional
- whether a game is visible but excluded from standings

Required semantics:

- `completed`: official and counted
- `pending admin review`: latest official result is visible and still counted
- `under examination`: latest official result is visible but excluded from standings

Use banners or inline explanation cards for these states. Do not assume the audience knows the workflow.

## Responsive behavior

### Desktop

- keep the hero/context block prominent
- allow `8/4` layouts for standings plus supporting context
- use larger typography than admin for headers and rankings

### Tablet

- tabs can remain horizontal if they still fit cleanly
- move the secondary rail below the main surface
- keep cards full-width

### Mobile

- stack the shell vertically
- convert competition tabs to a segmented control or horizontal scroller
- keep standings readable without shrinking the type too aggressively
- preserve banners and timestamps above the fold

Public is mobile-capable, but it should stay content-led rather than app-like.

## Components worth splitting

These are the useful reusable pieces for this shell:

- `PublicTopNav`
- `CompetitionTabs`
- `HeroCard`
- `StandingsCard`
- `ResultsListCard`
- `HistoryFeed`
- `StateBanner`
- `PublicFooter`

Do not split components just because a single page has a unique section. Split when the pattern repeats across home, competition, and game detail routes.

## What to avoid

- admin-style action density
- generic sports metaphors like player cards, prize pools, or global leagues
- dense KPI rows that feel like backoffice dashboards
- hiding provisional logic behind badges with no explanation
