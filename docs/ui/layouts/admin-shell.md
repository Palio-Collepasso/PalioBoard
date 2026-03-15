# Admin Shell Layout

## Purpose

The `/admin` shell is the operational workspace for authenticated users. It must feel stable, dense enough for laptop work, and visibly structured around authoritative state rather than decorative dashboard metrics.

This shell covers routes such as:

- `/admin/competitions`
- `/admin/competitions/:competition`
- `/admin/season`
- `/admin/games/new`
- `/admin/games/:id`
- `/admin/reviews`
- `/admin/audit`
- `/admin/settings/users`

## Core principles

- Optimize for judges and admins working on laptops during the event.
- Show fixed domain constraints clearly: one season, three competitions, four rioni.
- Put game state, validation, and next actions ahead of summary fluff.
- Keep one dominant CTA per page area.
- Use shared primitives from `../components/shared-layout-primitives.md` instead of creating route-specific variants for basic cards, badges, tables, and banners.

Checklist anchors:

- `component_checklist.md` sections `2.1`, `2.3`, `3.1`, `3.2`, `8.2`, `8.3`, and `8.4`

## Persistent shell structure

### 1. Sidebar

Use a fixed left sidebar on desktop.

- Width: `size.sidebarWidth` (`264px`)
- Background: white surface with a subtle right border
- Top block: product mark and current season label
- Middle block: primary navigation
- Bottom block: current user, role, and account actions

Recommended primary entries:

- Competitions
- Reviews
- Season
- Audit
- Users

Rules:

- Keep the nav to `5-7` entries max.
- Highlight the active route with orange tint or solid orange treatment.
- Do not add competition cards or transient alerts to the sidebar.

### 2. Top bar

Use a fixed or sticky top bar above the main content.

- Height: `layout.admin.topbarHeight` (`72px`)
- Left side: page context or search
- Right side: utilities, notifications, context action, profile
- Surface: white with subtle bottom border

The top bar should not become a second navigation system. It supports the current task; it does not replace the sidebar.

### 3. Main content canvas

The main content area sits to the right of the sidebar and under the top bar.

- App background: soft neutral gray
- Content container: `layout.admin.containerMaxWidth` (`1440px`)
- Horizontal page padding: `space.pageX` (`40px`)
- Vertical spacing between sections: `space.sectionGap` (`32px`)
- Default layout grid: `layout.admin.columns` (`12`)

Base page stack:

1. Page header
2. Optional subtitle or policy hint
3. Context or KPI strip
4. Primary work area
5. Sticky action bar when the page is form-heavy or completion-sensitive

## Layout regions

### Page header region

Every page should open with:

- clear title
- one-line explanation
- right-aligned primary action if needed

Examples:

- `Create game`
- `Start game`
- `Complete game`
- `Create user`

Do not mix multiple orange actions in the header. Secondary actions should drop into the page body or overflow menus.

### Context strip

Use this row for small, high-value summaries:

- game state
- live count
- completed count
- under examination count
- immutable/locked warning

This region should be cards or chips, not chart-heavy analytics.

### Primary work area

Choose one of these patterns:

#### Full-width data card

Use for:

- competition game lists
- review queues
- audit tables

Structure:

- section header
- filter/action row
- main table or list

#### Split workbench

Use for:

- game operations
- review detail
- standings plus context

Recommended ratio:

- main area: `8 columns`
- context rail: `4 columns`

The right rail is for validation, quick standings context, or audit summary. It is not a second full page.

#### Form plus preview

Use for:

- game create/edit
- season setup

Recommended ratio:

- form: `7 columns`
- preview/help: `5 columns`

Keep save/cancel actions in a sticky footer or bottom action zone so they stay visible during long edits.

## Content block rules

### Tables and lists

- Prefer one bordered surface instead of many nested cards.
- Keep row height around `56-64px`.
- Make the first column more visually prominent.
- Keep row actions on the far right.
- Use badges inside state columns, not plain text.

### Right rail

Only include a right rail when it adds operational value:

- validation blockers
- quick leaderboard impact
- recent audit summary
- live collaboration cues

Do not use the right rail for decorative filler.

### Sticky actions

Use sticky action bars for:

- game completion
- save/cancel on long forms
- review approval or rejection

Primary action goes last and remains visually dominant.

## State presentation

The admin shell needs a strict, reusable state system.

- `draft`: neutral chip
- `in progress`: orange or blue live chip
- `completed`: green chip
- `pending admin review`: orange warning chip
- `under examination`: red chip
- `immutable`: gray lock chip or inline lock note

State rules:

- `pending admin review` still counts in standings
- `under examination` stays visible but is excluded from standings
- validation errors belong in visible panels, not hidden tooltips

## Responsive behavior

### Desktop and laptop

This is the primary target.

- Keep the fixed sidebar
- Keep `12-column` layouts
- Preserve sticky actions and right rails where useful

### Tablet or narrow laptop

Below roughly `1180px`:

- allow the sidebar to collapse to an icon rail or drawer
- convert `8/4` and `7/5` splits into stacked sections when the secondary rail stops being readable
- keep header actions visible without wrapping into multiple rows if possible

### Small screens

Admin is not mobile-first, but it should still degrade safely:

- sidebar becomes an overlay drawer
- tables become stacked cards only when necessary
- sticky actions move to the bottom edge

Do not redesign admin into a public-style mobile app.

## Components worth splitting

These deserve dedicated implementation components because they repeat across the shell:

- `AdminSidebar`
- `AdminTopbar`
- `PageHeader`
- `SummaryCard`
- `TableCard`
- `ContextRail`
- `ValidationPanel`
- `StickyActionBar`

Keep route-specific blocks, such as tournament brackets or ranking-entry grids, outside the shell layer.

## What to avoid

- Generic sports dashboard widgets like prize pools, player counts, or category filters
- More than one navigation model competing for attention
- Pages made mostly of detached mini-cards with no dominant work surface
- Dense charting that displaces state, validation, or workflow actions
