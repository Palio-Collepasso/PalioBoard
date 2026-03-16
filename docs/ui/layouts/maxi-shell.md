# Maxi Shell Layout

## Purpose

The `/maxi` shell is a presentation surface for large displays. It is not a normal page with normal chrome. Its job is to be legible from distance and communicate one current message extremely clearly.

This shell covers routes such as:

- `/maxi/:competition`

## Core principles

- Optimize for distance readability first.
- Keep the layout almost free of chrome.
- Show only the information needed in the current moment.
- Avoid dense tables unless every row remains readable from afar.
- Reuse shared color, badge, and surface rules from `../components/shared-layout-primitives.md`, but scale typography and spacing specifically for presentation screens.

Checklist anchors:

- `component_checklist.md` sections `2.3`, `5.4`, `5.5`, and `8.5`

## Persistent shell structure

### 1. Full-screen canvas

Use the entire viewport as the presentation area.

- No sidebar
- No standard top nav
- No footer navigation
- Very low chrome

Base canvas:

- soft neutral or darkened neutral backdrop depending on contrast needs
- large white or tinted content panels
- strong orange reserved for highlights and urgent state labels

### 2. Header ribbon

Keep a compact header zone at the top.

Contents:

- competition name
- current state badge if needed
- optional timestamp

This region should stay small enough that it does not steal space from the main message.

### 3. Primary display area

The center of the screen should carry one dominant module:

- standings board
- current game board
- next game board

The layout should make it obvious which module is primary.

### 4. Secondary strip

Reserve the lower third or bottom strip for supportive context only.

Examples:

- now playing
- up next
- short explanatory note

Do not add a second full data table here.

## Layout variants

### Standings-first variant

Use when the main goal is to show the live competition order.

Structure:

1. top ribbon
2. large leaderboard panel
3. bottom strip with current or next game

Rules:

- keep to the four rioni only
- make ranking numbers visually dominant
- highlight state labels without breaking readability

### Current-game variant

Use when the event needs to focus attention on a specific game.

Structure:

1. top ribbon
2. current game card or matchup block
3. smaller standings snapshot or upcoming block below

Rules:

- only show the most relevant metadata
- avoid small notes or audit-like detail
- use one supporting message, not many

## Typography and spacing

The maxi shell needs its own scale.

- page-level title or competition name: `56-80px`
- leaderboard values or rankings: `64-96px`
- section labels: `24-32px`
- supporting text: `20-28px`

Spacing rules:

- larger outer margins than admin/public
- strong separation between the primary panel and secondary strip
- minimum `24px` internal spacing, often `32-40px`

## State presentation

States still matter, but they must be readable instantly.

Recommended treatments:

- `completed`: calm green or neutral-success tag
- `pending admin review`: orange or amber high-visibility tag
- `under examination`: red high-contrast tag plus short explanation if standings are shown

When standings are provisional because of an excluded game, say it directly in a single banner line. Do not rely on tiny footnotes.

## Screen behavior

### Primary target

Design first for landscape presentation screens.

- minimum practical layout target: `1366x768`
- preferred target: `1920x1080`

### Adaptation rules

- keep major content within safe margins so projectors and TVs do not crop edges
- avoid more than one dense column of detail
- if space becomes tight, remove secondary details before shrinking the main type

This shell does not need a mobile version. It needs a stable presentation version.

## Components worth splitting

These are the reusable shell-level pieces:

- `MaxiHeaderRibbon`
- `LeaderboardBoard`
- `NowPlayingPanel`
- `UpNextStrip`
- `FullScreenStateBanner`

Animations, if any, should be slow and purposeful. Avoid dashboard-like motion noise.

## What to avoid

- standard website navigation chrome
- audit detail, forms, filters, or dense result tables
- multiple competing panels with equal visual weight
- decorative effects that reduce contrast or readability
