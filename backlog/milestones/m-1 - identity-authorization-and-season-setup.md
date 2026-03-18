---
id: m-1
title: Identity, authorization, and season setup
---
## Description

Milestone: Identity, authorization, and season setup

Depends on: m-1 Delivery foundation and architecture skeleton.

Objective: make the application configurable and safe to access so admins can prepare a season and the system has the correct authorization vocabulary before any official result workflow exists.

Scope:
- Supabase Auth integration at the api boundary.
- Application users, seeded roles, seeded capabilities, and policy checks.
- Minimal superadmin-only user provisioning flow.
- One-season setup flow in the UI.
- Team management for the four default rioni.
- Competition and game configuration.
- Static field-catalog selection per game.
- Per-game points-table configuration.
- Immutability/deletion guards on result-affecting setup, with tests.

Exit criteria:
- A superadmin can create a user with one seeded role.
- Admin and judge access is enforced by api policy, not only by UI hiding.
- An admin can configure the season, teams, games, selected fields, and points tables from the UI.
- Attempts to perform unauthorized actions are rejected with structured errors.
- Setup immutability rules are implemented and covered by tests.
