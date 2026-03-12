# 05_Prototype_Specification.md

## PalioBoard --- Prototype Specification

------------------------------------------------------------------------

# 1. Prototype Overview

This document defines the interaction model for the PalioBoard
interactive prototype.

The prototype represents the operational workflow used by admins and
judges during the Palio competition. The system prioritizes fast result
entry, clear game state transitions, and transparent leaderboard
updates.

Key prototype characteristics:

-   Navigation model: **Full page navigation**
-   Interaction density optimized for **laptop usage**
-   Data entry modeled as **spreadsheet-style editing**
-   Public UI updates via **websocket-style live updates**
-   Minimal animations (modal transitions only)

The prototype should simulate:

-   real game lifecycle transitions
-   leaderboard recalculation
-   audit-triggering edits
-   public UI real-time updates

------------------------------------------------------------------------

# 2. Navigation Graph

``` mermaid
flowchart TD

Login[Login]
Dashboard[Admin Dashboard]

Competitions[Competitions Overview]
GamesList[Games List]
GameDetail[Game Detail]
ResultEntry[Result Entry Workspace]
StartModal[Start Game Modal]
CompleteModal[Complete Game Modal]

Standings[Standings]
Jolly[Jolly Overview]
Audit[Audit Log]

PublicHome[Public Home]
PublicCompetition[Public Competition]
PublicGame[Public Game Detail]
MaxiScreen[Maxi Screen]

Login --> Dashboard
Login --> PublicHome

Dashboard --> Competitions
Dashboard --> GamesList
Dashboard --> Standings
Dashboard --> Jolly
Dashboard --> Audit

Competitions --> GamesList
GamesList --> GameDetail

GameDetail --> StartModal
StartModal --> ResultEntry
ResultEntry --> CompleteModal
CompleteModal --> Standings

Standings --> GameDetail

PublicHome --> PublicCompetition
PublicCompetition --> PublicGame
PublicCompetition --> MaxiScreen
```

------------------------------------------------------------------------

# 3. Interaction Table

  ---------------------------------------------------------------------------------
  Interaction   Trigger       Animation   Duration   Target Screen  State Change
  ------------- ------------- ----------- ---------- -------------- ---------------
  Login         Submit        None        0ms        Dashboard      User
                credentials                                         authenticated

  Open Game     Click game    None        0ms        Game Detail    Load game state
                row                                                 

  Start Game    Confirm modal Modal close 120ms      Result Entry   Game state → In
                                                                    Progress

  Save Draft    Click Save    Toast       100ms      Same screen    Partial results
                                                                    saved

  Complete Game Confirm       Modal close 120ms      Standings      Game state →
                completion                                          Completed

  Edit          Edit cell     Inline      100ms      Same screen    Game → Pending
  Completed                   highlight                             Admin Review
  Game                                                              

  Mark Under    Button click  Badge       100ms      Same screen    Game → Under
  Examination                 update                                Examination

  Resolve       Confirm       None        0ms        Standings      Game →
  Examination   action                                              Completed

  Apply Manual  Submit modal  Toast       100ms      Standings      Standings
  Adjustment                                                        recalculated

  Public Update Websocket     Row refresh 100ms      Public pages   Leaderboard
                event                                               updated
  ---------------------------------------------------------------------------------

------------------------------------------------------------------------

# 4. Game State Machine

``` mermaid
stateDiagram-v2

[*] --> Draft

Draft --> InProgress: Start Game

InProgress --> Completed: Complete Game

Completed --> PendingAdminReview: Judge edits result

PendingAdminReview --> Completed: Admin approves

Completed --> UnderExamination: Appeal filed

UnderExamination --> Completed: Dispute resolved

UnderExamination --> InProgress: Result invalidated
```

------------------------------------------------------------------------

# 5. Result Entry Interaction Model

Result entry behaves similarly to a spreadsheet.

### Keyboard Navigation

  Key          Action
  ------------ -------------------
  Tab          Move to next cell
  Shift+Tab    Previous cell
  Arrow keys   Navigate cells
  Enter        Confirm value
  Esc          Cancel edit

### Inline Editing

-   Click cell → input appears
-   Value validated on blur
-   Invalid values highlighted in red
-   Errors shown below row

### Jolly Selection

Jolly must be declared in **Start Game modal**.

Interaction:

Trigger: select rione for Jolly\
Animation: none\
Duration: 0ms\
State Change: Jolly flag assigned to rione for that game

------------------------------------------------------------------------

# 6. Standings Update Behavior

When a game is completed:

1.  Result validated
2.  Completion confirmed
3.  Standings engine recalculates rankings
4.  Leaderboard refreshed

Prototype interaction:

Trigger: Confirm Complete Game\
Animation: None\
Duration: Instant\
State change:

-   leaderboard recalculated
-   public websocket event broadcast

------------------------------------------------------------------------

# 7. Under Examination Behavior

When a game enters **Under Examination**:

-   result remains visible publicly
-   leaderboard excludes its points
-   UI badge displayed

Prototype behavior:

  Element       Visual
  ------------- --------------------
  Game row      yellow badge
  Leaderboard   points removed
  Public page   provisional banner

------------------------------------------------------------------------

# 8. Data Entry Behavior

  Action            System Behavior
  ----------------- ------------------------------
  Enter placement   Validate tie structure
  Missing team      Block completion
  Invalid ranking   Show error
  Partial save      Allowed
  Completion        Requires all required fields

------------------------------------------------------------------------

# 9. Error Handling

### Validation Errors

Shown inline in the result table.

Examples:

-   invalid placements
-   missing teams
-   required fields empty

### System Errors

Displayed as toast alerts.

  Error                    Message
  ------------------------ -------------------------------------
  Network failure          "Save failed. Retry."
  Standings engine error   "Leaderboard recalculation failed."

------------------------------------------------------------------------

# 10. Public Real-Time Update Model

Public pages subscribe to leaderboard updates via **websocket events**.

Prototype simulation:

``` mermaid
sequenceDiagram

Judge->>Server: Complete Game
Server->>StandingsEngine: Recalculate leaderboard
StandingsEngine-->>Server: Updated ranking
Server->>PublicClients: Websocket update
PublicClients->>UI: Refresh leaderboard
```

------------------------------------------------------------------------

# 11. Maxi Screen Interaction

Maxi-screen auto-rotates between three views.

Rotation cycle:

1.  Leaderboard
2.  Current Game
3.  Next Game

Rotation duration: **10 seconds per screen**

Animation: none (instant switch)

State changes triggered by:

-   game start
-   game completion

------------------------------------------------------------------------

# 12. Microinteraction Guidelines

Minimal operational UI.

  Interaction         Feedback
  ------------------- --------------------
  Save action         toast confirmation
  Validation error    red input border
  Completion          success toast
  Jolly used          icon highlight
  Pending review      orange badge
  Under examination   yellow badge

------------------------------------------------------------------------

# 13. Animation Guidelines

Animations are intentionally minimal.

  Element           Animation      Duration
  ----------------- -------------- ----------
  Modal open        Fade + scale   120ms
  Modal close       Fade           120ms
  Table update      Instant        0ms
  Page navigation   None           0ms

Reason: operational speed and clarity.

------------------------------------------------------------------------

# 14. Prototype Data Simulation

Prototype should include:

### Sample Teams

-   Bosco
-   Tafuri
-   Carrozzini
-   Castello

### Sample Games

-   Streetball (1v1 tournament)
-   Gimkana con la bici (ranking)
-   Bandierina (ranking)

### Sample States

-   Draft
-   In Progress
-   Completed
-   Under Examination

------------------------------------------------------------------------

# 15. Prototype Success Criteria

The prototype is considered valid if:

-   judges can simulate full result entry workflow
-   game state transitions are clear
-   leaderboard updates instantly
-   Jolly usage is validated
-   public screens update automatically
-   dispute workflow is understandable

------------------------------------------------------------------------

End of document.
