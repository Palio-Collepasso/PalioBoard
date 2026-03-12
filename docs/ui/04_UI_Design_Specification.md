# 04_UI_Design_Specification.md

## PalioBoard UI Design Specification

---

# 1. Design Principles

## Operations First

The interface prioritizes speed and clarity for judges and admins during live events.

## Clarity Over Decoration

Because results directly affect public standings, the UI must emphasize accuracy, readability, and auditability.

## Predictable Interfaces

Users should always understand:

- game state
- leaderboard impact
- validation feedback

## Compact Data-Dense Layout

Layouts are optimized for laptops and rapid scanning.

## Public Transparency

Public screens clearly communicate standings, provisional results, and disputes.

---

# 2. Design Tokens

## Color Palette

Team colors come from the database and are not defined in the design system.

Primary: #2563EB
Primary Hover: #1D4ED8
Background: #F9FAFB
Surface: #FFFFFF
Border: #E5E7EB
Text Primary: #111827
Text Secondary: #6B7280
Danger: #DC2626
Warning: #F59E0B
Success: #16A34A
Info: #2563EB

---

# 3. Typography

Font: Inter

Font stack:
Inter, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif

Type scale:

Display 32px
H1 24px
H2 20px
H3 18px
Body 14px
Small 12px
Table 13px

Weights:

400 body
500 labels
600 buttons
700 headings

---

# 4. Grid System

12-column grid.

Breakpoints:

Desktop ≥1280px
Tablet 768–1279px
Mobile ≤767px

Admin layout:

Sidebar 240px
Main content flexible.

---

# 5. Spacing System

Base unit: 4px

Scale:

4px
8px
12px
16px
24px
32px

---

# 6. Icon System

Icon set: Lucide

Common icons:

Play
Check
Pencil
Trash
History
AlertTriangle
Info
Search

Size: 16px or 20px.

---

# 7. Components

## Buttons

Primary
Secondary
Danger

States:

Default
Hover
Active
Disabled

Sizes:

Small 32px
Default 36px
Large 44px

---

## Tables

Row height: 36px.

Features:

sortable columns
sticky headers
compact density

---

## Status Badge

Used for:

Draft
In Progress
Completed
Pending Review
Under Examination

---

## Leaderboard Component

Columns:

Rank
Team
Points
First Places
Jolly Used

---

## Result Entry Table

Columns configurable:

Team
Placement
Metric
Time
Penalties
Jolly

Supports keyboard navigation and inline validation.

---

## Bracket Component

Displays semifinals and finals.

Supports:

winner selection
auto ranking
admin override

---

## Modal

Used for:

Start Game
Complete Game
Manual Adjustments
Appeals

Width: 480–640px.

---

## Alerts

Types:

Info
Success
Warning
Error

Displayed inline or as toast.

---

# 8. Form Styles

Input height: 36px.

States:

Default
Focus
Error
Disabled

Error includes red border and message.

---

# 9. Layout Templates

## Admin Layout

Top navigation
Sidebar navigation
Main content

Sidebar:

Dashboard
Competitions
Games
Standings
Season Setup
Audit

---

## Game Entry Workspace

Sections:

Game header
Results table
Validation panel

---

## Public Competition Layout

Sections:

Leaderboard
Recent Games
Game History
Jolly Summary

---

## Maxi Screen Layout

Full screen scoreboard with:

Event title
Leaderboard
Current game
Next game

---

# 10. Key Screens

Admin Dashboard
Competitions Overview
Season Setup
Games List
Game Detail — Ranking Entry
Game Detail — Tournament Entry
Standings
Jolly Overview
Audit Log
Public Home
Public Competition
Public Game Detail

---

# 11. Responsive Rules

Desktop: full admin UI
Tablet: collapsible sidebar
Mobile: public view optimized

---

# 12. Accessibility

WCAG 2.1 compliance.

Contrast ≥4.5:1

Keyboard navigation required.

Focus states visible.

Tables accessible to screen readers.

Leaderboard must not rely only on color.

---

End of document.
