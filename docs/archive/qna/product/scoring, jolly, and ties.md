# Scoring, Jolly, and Ties

## v1 — questions and improved answers
### 5) Should points be computed automatically or entered manually?
**Answer:** Points must be **computed automatically**. The system must handle:
- placement-to-points mapping
- ties/ex aequo
- Jolly
- Prepalio roll-up into the main Palio leaderboard

Configuration should live in the **web app / database**, not in hardcoded values.

### 13) How should Jolly work?
**Answer:** Jolly is **not pre-assigned** during season setup. Each team decides **shortly before a Palio game** whether to use it and communicates that choice to the judges. Then the judge/admin records it inside the game result flow.

The system must:
- allow a **per-team Jolly flag** on Palio games
- ensure a team **cannot use Jolly more than once**
- block invalid reuse and show an error
- provide a **Jolly summary page** by team and game

### 15) Should the system compute placements automatically from metrics?
**Answer:** No. In v1, judges must **enter final placements manually**. Automatic ranking logic is postponed.

### 16) How should ties be entered?
**Answer:** Judges should enter placements explicitly, for example:
- `1,2,2,4`

The system validates the structure and computes points accordingly.

### 23) Should admins be able to adjust standings manually?
**Answer:** Yes. Admins need a way to apply **manual leaderboard adjustments** outside normal game results, with a reason and audit trail.

### 31) How should points tables be configured?
**Answer:** Points tables should be configurable **per game / competition item**, with sensible defaults.

### 32) What are the default points tables?
**Answer:** Default values are:
- **Palio game:** `4,3,2,1`
- **Giocasport game:** `4,3,2,1`
- **Prepalio final ranking:** `4,3,2,1`

### 35) Can admins override automatic rankings?
**Answer:** Yes. For **every automatically computed ranking**, admins must be able to apply a **manual override**. The system should retain both the computed version and the official overridden one, with audit history.
