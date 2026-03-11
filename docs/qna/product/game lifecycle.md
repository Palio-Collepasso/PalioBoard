# Game Lifecycle

## v1 — questions and improved answers
### 7) Who can change data after publication?
**Answer:** Distinguish between **game definition changes** and **result changes**:
- **Game definition** (name, format, enabled fields, etc.) can be changed **only by admins**, and only until results exist.
- **Results** can be entered and edited by judges.
- Every result change must be **fully audited**.

### 14) What counts as the moment a game starts?
**Answer:** A game starts only when a judge/admin explicitly clicks **Start game**.

### 27) What happens if a judge edits a completed game?
**Answer:** Editing a completed game result creates a distinct state: **pending admin review** (better naming can still be chosen). This is different from **under examination**, which is for appeals or disputes requiring a judge decision.

### 28) Does pending admin review still affect standings?
**Answer:** Yes. While in **pending admin review**, the game behaves like **completed** for standings and public visibility. The latest judge edit is shown publicly; the status is there to signal admins to review or revert the change through the audit trail.

### 38) When is a game allowed to be completed?
**Answer:** The system must block **Complete game** until the result is structurally valid, meaning:
- all 4 teams have placements
- placements form a valid ranking pattern
- all enabled required fields are filled
