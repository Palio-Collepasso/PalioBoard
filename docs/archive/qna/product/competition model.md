# Competition Model

## v1 — questions and improved answers
### 3) What must the system record for games in v1?
**Answer:** In v1 the app records results at **team level**, not player level. It must capture whatever is needed to determine the winner and standings:
- **placement** (most important)
- **time**, when relevant
- **quantity / score / points** as one configurable result field with a game-specific UI label
- **penalties**, when relevant
- **public notes**

### 4) How should games be modeled?
**Answer:** v1 uses only **two templates**:
1. **Ranking format** with optional fields (placement plus any needed time / quantity / penalties / notes)
2. **1v1 tournament format**

This avoids building a generic form builder.

### 9) Which result-entry model should the product support first?
**Answer:** The app must support **all games**, but in v1 it records them through the two fixed templates. For ranking-based games, player-level participation is deferred.

### 10) Can we assume a fixed 1v1 tournament structure?
**Answer:** Yes. A 1v1 tournament is always:
- semifinal
- final for 3rd/4th
- final for 1st/2nd

This is not only a v1 assumption, but a general modeling rule.

### 20) Does v1 need game order or scheduled datetime?
**Answer:** No. In v1, **order does not matter** and games do not need a scheduled datetime.

### 22) How should games be classified?
**Answer:** Every game belongs to exactly one competition type:
- **Palio**
- **Prepalio**
- **Giocasport**

### 29) How is the 1v1 final ranking produced?
**Answer:** The system should **derive the final ranking automatically** from the four match outcomes.

### 30) How are 1v1 semifinal pairings defined?
**Answer:** Pairings are **not part of season setup**. They are an operational action performed shortly before the tournament, usually after a random extraction. This should be handled via a dedicated permission/capability, not by broad season-setup rights.

### 37) Do normal games always involve all 4 teams?
**Answer:** Yes. In v1, normal games always include **all four teams**.
