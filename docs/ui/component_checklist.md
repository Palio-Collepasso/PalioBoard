# PalioBoard UI Component Checklist

This checklist turns the extracted visual template into a reusable UI inventory.
It is organized for design/dev handoff.

---

## 1. Foundations

### 1.1 Color system
- [ ] Brand primary scale implemented: 50, 100, 500, 600
- [ ] Neutral scale implemented: app bg, surface, subtle, border, strong border, primary text, secondary text, tertiary text
- [ ] Semantic colors implemented: success, warning, danger, info
- [ ] Overlay color defined for dialogs/drawers
- [ ] Link color matches primary brand

### 1.2 Typography
- [ ] Sans family defined for all surfaces
- [ ] Text styles available: page title, section title, card title, body, label, caption, metric
- [ ] Caption/header style supports uppercase + wider tracking
- [ ] Numeric emphasis style available for stats, rankings, counters

### 1.3 Spacing and sizing
- [ ] 4px-based spacing scale implemented
- [ ] Standard paddings available: page, section, card, form group
- [ ] Height tokens available for buttons, inputs, search bar
- [ ] Sidebar and topbar dimensions standardized

### 1.4 Shape and elevation
- [ ] Radius tokens implemented: sm, md, lg, xl, pill
- [ ] Card shadow token implemented
- [ ] Floating shadow token implemented
- [ ] Dialog shadow token implemented

### 1.5 Motion and layering
- [ ] Standard motion durations available: fast, normal, slow
- [ ] Standard easing functions available
- [ ] Layering scale available: dropdown, sticky, overlay, modal, toast

---

## 2. Shells and layout primitives

### 2.1 Admin shell
- [ ] Fixed left sidebar
- [ ] Top navigation bar with search and right-side utilities
- [ ] Main content container with consistent max width
- [ ] 12-column content grid
- [ ] Bottom-pinned user/profile block in sidebar

### 2.2 Public shell
- [ ] Public top navigation / tabs
- [ ] Wider content container than admin cards layout
- [ ] Footer block for support/legal/help links
- [ ] Consistent hero/content spacing

### 2.3 Layout primitives
- [ ] Page header component
- [ ] Section block wrapper
- [ ] Card grid wrapper
- [ ] Split layout for detail pages (main content + side panel)
- [ ] Empty state wrapper
- [ ] Loading skeleton wrapper

---

## 3. Navigation components

### 3.1 Sidebar navigation
- [ ] Sidebar item with icon + label
- [ ] Active state using strong brand emphasis
- [ ] Hover and focus states
- [ ] Group label / nav section label
- [ ] Collapsible behavior defined or explicitly omitted

### 3.2 Topbar
- [ ] Global search field
- [ ] Icon action buttons
- [ ] Profile/avatar menu trigger
- [ ] Primary CTA slot on the right
- [ ] Context breadcrumb or page context area

### 3.3 Public navigation
- [ ] Brand/logo area
- [ ] Main tabs/links
- [ ] Current section state
- [ ] Mobile fallback behavior defined

---

## 4. Actions and inputs

### 4.1 Buttons
- [ ] Primary button
- [ ] Secondary button
- [ ] Ghost/text button
- [ ] Destructive button variant
- [ ] Compact icon button
- [ ] States defined: default, hover, active, focus, disabled, loading

### 4.2 Form controls
- [ ] Text input
- [ ] Search input
- [ ] Textarea
- [ ] Select / combobox
- [ ] Checkbox
- [ ] Radio group
- [ ] Switch / toggle
- [ ] Date / time input style
- [ ] File attachment row style if needed
- [ ] States defined: default, hover, focus, error, disabled, read-only

### 4.3 Form composition
- [ ] Label above field pattern
- [ ] Helper text below field pattern
- [ ] Error text pattern
- [ ] Required indicator pattern
- [ ] Inline action beside field
- [ ] Multi-column form layout rules

---

## 5. Information display

### 5.1 Cards
- [ ] Base card
- [ ] Metric/stat card
- [ ] Summary card with title + meta + actions
- [ ] Detail card with header/body/footer slots
- [ ] Highlight card using subtle brand tint

### 5.2 Badges and chips
- [ ] Neutral badge
- [ ] Success badge
- [ ] Warning badge
- [ ] Danger badge
- [ ] Info badge
- [ ] Selectable filter chip
- [ ] Team/context chip pattern

### 5.3 Tables and lists
- [ ] Standard data table
- [ ] Compact table
- [ ] Sortable header cell
- [ ] Status cell
- [ ] Action cell
- [ ] Sticky header behavior
- [ ] Empty table state
- [ ] Row hover state
- [ ] Mobile fallback strategy defined

### 5.4 Metric and ranking blocks
- [ ] Large metric value block
- [ ] Delta/trend indicator
- [ ] Ranking row with position marker
- [ ] Highlighted first/leading row treatment
- [ ] Team score / result strip

### 5.5 Media and illustration placeholders
- [ ] Icon container pattern
- [ ] Empty state illustration slot
- [ ] Hero/banner slot for public pages

---

## 6. Feedback and states

### 6.1 Inline states
- [ ] Success message block
- [ ] Warning message block
- [ ] Error message block
- [ ] Info message block
- [ ] Dismissible alert behavior

### 6.2 System feedback
- [ ] Toast pattern
- [ ] Confirmation dialog pattern
- [ ] Form submission pending state
- [ ] Page-level loading state
- [ ] Partial refresh state for cards/tables

### 6.3 Empty/error/loading states
- [ ] Empty state with title, explanation, CTA
- [ ] Error state with retry action
- [ ] Skeleton for cards
- [ ] Skeleton for tables
- [ ] Skeleton for detail pages

---

## 7. Overlays

### 7.1 Modal
- [ ] Standard centered modal
- [ ] Title, description, body, footer action zones
- [ ] Close affordance
- [ ] Escape / backdrop behavior defined
- [ ] Destructive confirmation modal variant

### 7.2 Drawer / side panel
- [ ] Optional right-side drawer for supporting detail/action flows
- [ ] Header/body/footer slots
- [ ] Overlay and close behavior

### 7.3 Menus and popovers
- [ ] Dropdown menu
- [ ] Action menu
- [ ] Tooltip
- [ ] Popover / filter popover

---

## 8. Page-level templates

### 8.1 Dashboard page template
- [ ] Page header with primary CTA
- [ ] Metric cards row
- [ ] Activity/recent updates block
- [ ] Secondary insights block
- [ ] Responsive stacking rules

### 8.2 Index/list page template
- [ ] Title + actions row
- [ ] Filters/search row
- [ ] Table or card list body
- [ ] Pagination or infinite loading pattern

### 8.3 Detail page template
- [ ] Page title + status badge + primary actions
- [ ] Main info card
- [ ] Secondary metadata side card
- [ ] Activity/history section
- [ ] Related items/results section

### 8.4 Create/edit page template
- [ ] Page title + back action
- [ ] Sectioned form cards
- [ ] Sticky footer or bottom action bar
- [ ] Validation summary pattern

### 8.5 Public standings/content template
- [ ] Header/title block
- [ ] Main standings card/table
- [ ] Supporting context/results blocks
- [ ] Highlighted leading team/result pattern

---

## 9. Interaction quality checks

- [ ] All clickable elements have visible hover state
- [ ] All interactive elements have visible keyboard focus state
- [ ] Disabled elements are distinguishable but still legible
- [ ] Color is not the only carrier of meaning
- [ ] Table rows and filters remain understandable on smaller screens
- [ ] Dialogs trap focus correctly
- [ ] Touch targets are large enough for compact actions

---

## 10. What should stay visually consistent across all pages

- [ ] Same app background and white surface pattern
- [ ] Same topbar/sidebar treatment in admin pages
- [ ] Same card border, radius, and shadow rules
- [ ] Same button hierarchy
- [ ] Same input styling and validation behavior
- [ ] Same table header/row language
- [ ] Same badge semantics
- [ ] Same typography hierarchy
- [ ] Same spacing rhythm
- [ ] Same modal structure and overlay treatment

---

## 11. Recommended minimum implementation order

- [ ] Foundations: color, type, spacing, radius, shadows
- [ ] Shells: admin shell, public shell, page header, section wrapper
- [ ] Inputs and buttons
- [ ] Cards and badges
- [ ] Tables and list patterns
- [ ] Modals and dropdowns
- [ ] Empty/loading/error states
- [ ] Page templates

