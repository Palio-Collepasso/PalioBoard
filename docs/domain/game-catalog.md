# Game catalog

## Purpose

This document is a normalized implementation catalog for v1. It translates the 2025 regulation and the current product decisions into an operational per-game reference for product, engineering, and AI coding agents.

It is **not** the legal source of truth. When this catalog conflicts with the official regulation or later organizer clarifications, the regulation and explicit organizer decisions win.


## Global domain rules

### Competition contexts

The system supports exactly three competition contexts in v1:

- **Palio**: the main competition whose completed official game results feed the main standings.
- **Prepalio**: a separate competition made of subgames; its subgame points are aggregated into a final Prepalio ranking, and that final ranking contributes points to the main Palio standings.
- **Giocasport**: a separate youth competition with its own leaderboard only.

### Four-team assumptions

v1 assumes exactly **four teams / rioni** for the season. Every supported game format is normalized around those four teams.

### Default points logic

Unless a game or aggregate competition is explicitly configured otherwise, the default points table is:

- **1st place = 4**
- **2nd place = 3**
- **3rd place = 2**
- **4th place = 1**

Withdrawals and equivalent declassamenti should map to the **last-place points**.

### Ex aequo / tie handling

The regulation allows **ex aequo** points. In v1, ties should be represented through explicit placements such as `1,2,2,4`, with points computed automatically from the configured table. If a game’s native mechanics produce a tie but the official result cannot be represented cleanly with placements alone, admin review or manual override may be needed.

### Jolly rules

- Jolly exists only for **Palio** games.
- Each team can use Jolly **once** in the Palio season.
- Jolly must be declared **before** the relevant game.
- In v1 it is recorded as a **per-team official result flag** at result-entry time.
- Reuse must be rejected.
- The affected team’s points for that Palio game are **doubled**.
- Jolly is **never** allowed in Prepalio or Giocasport.

### Prepalio aggregate behavior

Prepalio subgames are stored as normal games inside the **Prepalio** competition. Their points are summed into a **Prepalio aggregate ranking**. That aggregate ranking is then mapped again through the default points table (normally `4,3,2,1`) and added to the main Palio standings.

This means **Prepalio is both**:
- its own competition area, and
- an input into the main Palio leaderboard through its final aggregate result.

### Giocasport separation

Giocasport has its **own standalone leaderboard** and does **not** assign points to the main Palio standings.

### Immutability after official result data exists

Once a game has any official result data in v1, every game property and relationship should be treated as **immutable**, including at least:
- competition
- format
- selected result fields
- points table
- other result-affecting setup

### Supported v1 formats only

v1 supports only these two normalized game formats:

- `ranking`
- `tournament_1v1`

Use `ranking` for games where judges ultimately enter one official placement per team.  
Use `tournament_1v1` for fixed 4-team bracket games that are effectively modeled as:
- semifinal 1
- semifinal 2
- final 3rd/4th
- final 1st/2nd

### Important v1 boundary

Many regulation clauses describe player counts, age bands, gender composition, weight limits, equipment, or eligibility rules. These are important operational notes, but v1 does **not** do player-level roster validation or eligibility enforcement. Treat such rules as **displayed notes / organizer guidance**, not as hard-enforced application logic, unless future scope expands.


## Prepalio

These entries represent the four Prepalio subgames defined by the regulation. For v1, the strongest reading is that they should use the fixed four-team `tournament_1v1` template, because the regulation explicitly says **semifinali e finali**, and the product model already reserves that format for this recurring 4-team bracket shape.

### Streetball misto

- **game name:** Streetball misto
- **competition:** Prepalio
- **likely v1 format:** `tournament_1v1`
- **source confidence:** high
- **regulation clues:** Art. 18 says the Prepalio streetball is played with **semifinali e finali**; the detailed game section also labels it **tipo quadrangolare**.
- **enabled result fields likely needed in v1:** `placement` (derived from bracket); `notes/text` optional. Match score is useful for display but not required for v1 winner-only tournament flow.
- **notes/text needed?:** Optional but useful for judge/admin notes.
- **Jolly allowed?:** No.
- **default points logic:** First compute the 1st–4th order from the tournament bracket; then award normal Prepalio subgame points from placements.
- **special constraints or caveats:** 2v2 plus reserve; first to 10; normal streetball foul logic. v1 does not need live score entry for this tournament.
- **suspended / ambiguous / manual admin setup confirmation:** Not suspended. Format mapping is clear enough for seeding.


### Bocce misto

- **game name:** Bocce misto
- **competition:** Prepalio
- **likely v1 format:** `tournament_1v1`
- **source confidence:** high
- **regulation clues:** Art. 18 explicitly says bocce is played with **semifinali e finali** in Prepalio.
- **enabled result fields likely needed in v1:** `placement` (derived from bracket); `notes/text` optional.
- **notes/text needed?:** Optional but useful.
- **Jolly allowed?:** No.
- **default points logic:** Derived placements get normal Prepalio subgame points.
- **special constraints or caveats:** Mixed pair; age restriction before 31/12/1979 is informational only in v1. Source does not require per-shot stat tracking.
- **suspended / ambiguous / manual admin setup confirmation:** Not suspended. Format mapping is clear enough for seeding.


### Ping pong misto

- **game name:** Ping pong misto
- **competition:** Prepalio
- **likely v1 format:** `tournament_1v1`
- **source confidence:** high
- **regulation clues:** Art. 18 explicitly says ping pong misto is played with **semifinali e finali** in Prepalio.
- **enabled result fields likely needed in v1:** `placement` (derived from bracket); `notes/text` optional.
- **notes/text needed?:** Optional but useful.
- **Jolly allowed?:** No.
- **default points logic:** Derived placements get normal Prepalio subgame points.
- **special constraints or caveats:** Single-athlete team representation; detailed rules are just 'classiche', so the app should not attempt sport-specific validation.
- **suspended / ambiguous / manual admin setup confirmation:** Not suspended. Format mapping is clear enough for seeding.


### Calciotennis maschile

- **game name:** Calciotennis maschile
- **competition:** Prepalio
- **likely v1 format:** `tournament_1v1`
- **source confidence:** high
- **regulation clues:** Art. 18 explicitly says calcio tennis is played with **semifinali e finali**; detailed section says **tipo quadrangolare** and describes classic tie-break-like scoring.
- **enabled result fields likely needed in v1:** `placement` (derived from bracket); `notes/text` optional. Match score / set summary is optional, not required for v1.
- **notes/text needed?:** Optional but useful.
- **Jolly allowed?:** No.
- **default points logic:** Derived placements get normal Prepalio subgame points.
- **special constraints or caveats:** 3 players plus reserve; first to 11 wins a set, first to 2 sets wins the match. v1 can record winners only.
- **suspended / ambiguous / manual admin setup confirmation:** Not suspended. Format mapping is clear enough for seeding.



## Palio

These entries represent the main Palio games listed in the regulation. Most are normalized as `ranking`, because v1 uses ranking for all non-bracket games and does not attempt to derive placements automatically from raw time / score / penalty data. Where the wording suggests elimination brackets or direct head-to-head matches, the mapping is marked accordingly and any uncertainty is called out explicitly.

### Tiro alla fune — maschile

- **game name:** Tiro alla fune — maschile
- **competition:** Palio
- **likely v1 format:** `tournament_1v1`
- **source confidence:** medium
- **regulation clues:** The game title says **tipo quadrangolare**, but this section does not explicitly restate semifinal/final structure. Tug-of-war is inherently head-to-head, so a 4-team bracket is the most plausible v1 mapping.
- **enabled result fields likely needed in v1:** `placement` (derived from bracket if confirmed); `notes/text` recommended.
- **notes/text needed?:** Yes, for officiating notes or disputes.
- **Jolly allowed?:** Yes.
- **default points logic:** Normal Palio game points from final placements; Jolly may double a team’s points.
- **special constraints or caveats:** Weight-band and equipment rules are operational notes only in v1. Because bracket shape is inferred rather than restated here, do not auto-seed as tournament without organizer confirmation.
- **suspended / ambiguous / manual admin setup confirmation:** Ambiguous enough to require manual admin setup confirmation on format before season use.


### Tiro alla fune — femminile

- **game name:** Tiro alla fune — femminile
- **competition:** Palio
- **likely v1 format:** `tournament_1v1`
- **source confidence:** medium
- **regulation clues:** The title says **tipo quadrangolare** and references the same rules as the men’s version with different total team weight.
- **enabled result fields likely needed in v1:** `placement` (derived from bracket if confirmed); `notes/text` recommended.
- **notes/text needed?:** Yes, for officiating notes or disputes.
- **Jolly allowed?:** Yes.
- **default points logic:** Normal Palio game points from final placements; Jolly may double a team’s points.
- **special constraints or caveats:** Same ambiguity as the men’s version: likely head-to-head bracket, but the local section does not explicitly say semifinals/finals.
- **suspended / ambiguous / manual admin setup confirmation:** Ambiguous enough to require manual admin setup confirmation on format before season use.


### Bandierina

- **game name:** Bandierina
- **competition:** Palio
- **likely v1 format:** `ranking`
- **source confidence:** medium
- **regulation clues:** Labeled **tipo quadrangolare**, but the detailed rules describe 21 numbered calls and infractions rather than a fixed semifinal/final bracket.
- **enabled result fields likely needed in v1:** `placement`; `score/quantity-like metric` recommended for round wins / successful calls if organizers want visibility; `notes/text` recommended.
- **notes/text needed?:** Yes.
- **Jolly allowed?:** Yes.
- **default points logic:** Normal Palio game points from the final team placements; Jolly may double points.
- **special constraints or caveats:** Because the regulation describes repeated calls rather than a clean 4-match bracket, `ranking` is the safer v1 normalization unless organizers explicitly want bracket handling.
- **suspended / ambiguous / manual admin setup confirmation:** Ambiguous on native mechanics; manual admin confirmation is recommended, but `ranking` is a workable default.


### Gimkana con la bici

- **game name:** Gimkana con la bici
- **competition:** Palio
- **likely v1 format:** `ranking`
- **source confidence:** high
- **regulation clues:** The winner is explicitly the team with the **minor tempo**, with explicit **5-second penalties** for listed infractions.
- **enabled result fields likely needed in v1:** `placement`; `time`; `penalties`; `notes/text` optional.
- **notes/text needed?:** Optional.
- **Jolly allowed?:** Yes.
- **default points logic:** Rank teams by official time after penalties, then map placements to Palio points; Jolly may double points.
- **special constraints or caveats:** Very clean ranking game for v1. Raw metric is time plus explicit penalty increments.
- **suspended / ambiguous / manual admin setup confirmation:** Not suspended and not materially ambiguous.


### Volpe zoppa e gatto cieco

- **game name:** Volpe zoppa e gatto cieco
- **competition:** Palio
- **likely v1 format:** `ranking`
- **source confidence:** high
- **regulation clues:** The winner is explicitly the team that bursts the last balloon in the **minor tempo**.
- **enabled result fields likely needed in v1:** `placement`; `time`; `notes/text` optional.
- **notes/text needed?:** Optional.
- **Jolly allowed?:** Yes.
- **default points logic:** Rank by fastest time, then assign normal Palio points; Jolly may double points.
- **special constraints or caveats:** No explicit numeric penalties beyond handling interruptions from external causes; notes may be useful for stoppages.
- **suspended / ambiguous / manual admin setup confirmation:** Not suspended and not materially ambiguous.


### Corsa con la carriola

- **game name:** Corsa con la carriola
- **competition:** Palio
- **likely v1 format:** `ranking`
- **source confidence:** high
- **regulation clues:** The winner is the team that transports **more water within 3 minutes**.
- **enabled result fields likely needed in v1:** `placement`; `score/quantity-like metric` (water carried); `notes/text` optional.
- **notes/text needed?:** Optional.
- **Jolly allowed?:** Yes.
- **default points logic:** Rank by official carried quantity, then assign Palio points; Jolly may double points.
- **special constraints or caveats:** Time is a cap, not the primary ranking metric. Treat the carried quantity as the decisive official value.
- **suspended / ambiguous / manual admin setup confirmation:** Not suspended and not materially ambiguous.


### Lancio delle uova

- **game name:** Lancio delle uova
- **competition:** Palio
- **likely v1 format:** `ranking`
- **source confidence:** high
- **regulation clues:** The winner is explicitly the team that makes the **longest valid throw**.
- **enabled result fields likely needed in v1:** `placement`; `score/quantity-like metric` (longest valid distance / round reached); `notes/text` optional.
- **notes/text needed?:** Optional.
- **Jolly allowed?:** Yes.
- **default points logic:** Rank by official longest valid result, then assign Palio points; Jolly may double points.
- **special constraints or caveats:** No need for sport-specific event modeling beyond the official longest valid outcome.
- **suspended / ambiguous / manual admin setup confirmation:** Not suspended and not materially ambiguous.


### Corsa staffetta

- **game name:** Corsa staffetta
- **competition:** Palio
- **likely v1 format:** `ranking`
- **source confidence:** high
- **regulation clues:** The winner is explicitly the team with the **miglior tempo**.
- **enabled result fields likely needed in v1:** `placement`; `time`; `notes/text` optional.
- **notes/text needed?:** Optional.
- **Jolly allowed?:** Yes.
- **default points logic:** Rank by fastest valid time, then assign Palio points; Jolly may double points.
- **special constraints or caveats:** Lane invasion causes exclusion / disqualification, so notes may help document official decisions.
- **suspended / ambiguous / manual admin setup confirmation:** Not suspended and not materially ambiguous.


### Passami la mela

- **game name:** Passami la mela
- **competition:** Palio
- **likely v1 format:** `ranking`
- **source confidence:** high
- **regulation clues:** The winner is the team that, within **3 minutes**, successfully transfers **7 apples** first / best; invalid drops are not counted.
- **enabled result fields likely needed in v1:** `placement`; `score/quantity-like metric` (valid apples transferred); `notes/text` optional.
- **notes/text needed?:** Optional.
- **Jolly allowed?:** Yes.
- **default points logic:** Rank by official valid quantity; if organizers need an explicit tie-break they must handle it operationally or via notes/admin decision.
- **special constraints or caveats:** The text implies a capped-quantity race inside a time limit, but does not define a secondary tie-break if multiple teams complete the target.
- **suspended / ambiguous / manual admin setup confirmation:** Slightly caveated but still workable as a normal ranking game.


### Tieni il ritmo misto

- **game name:** Tieni il ritmo misto
- **competition:** Palio
- **likely v1 format:** `ranking`
- **source confidence:** high
- **regulation clues:** The winner is explicitly the team that completes **more jumps in 3 minutes** without breaking rope rotation.
- **enabled result fields likely needed in v1:** `placement`; `score/quantity-like metric` (valid jumps); `notes/text` optional.
- **notes/text needed?:** Optional.
- **Jolly allowed?:** Yes.
- **default points logic:** Rank by official jump count, then assign Palio points; Jolly may double points.
- **special constraints or caveats:** Very clean quantity-based ranking game.
- **suspended / ambiguous / manual admin setup confirmation:** Not suspended and not materially ambiguous.


### Ti faresti guidare da un uomo

- **game name:** Ti faresti guidare da un uomo
- **competition:** Palio
- **likely v1 format:** `ranking`
- **source confidence:** high
- **regulation clues:** The winner is explicitly the team that completes the course in the **minor tempo**, with listed **5-second penalties** for some mistakes.
- **enabled result fields likely needed in v1:** `placement`; `time`; `penalties`; `notes/text` optional.
- **notes/text needed?:** Optional.
- **Jolly allowed?:** Yes.
- **default points logic:** Rank by official time after penalties, then assign Palio points; Jolly may double points.
- **special constraints or caveats:** Very clean ranking game for v1.
- **suspended / ambiguous / manual admin setup confirmation:** Not suspended and not materially ambiguous.


### Roverino

- **game name:** Roverino
- **competition:** Palio
- **likely v1 format:** `tournament_1v1`
- **source confidence:** medium
- **regulation clues:** The section describes a full team-vs-team match with goals, goalkeeper area, fouls, penalties, two halves, and match officiating. That strongly suggests a head-to-head tournament shape, but this section does not explicitly spell out the 4-team bracket.
- **enabled result fields likely needed in v1:** `placement` (derived from bracket if confirmed); `notes/text` recommended. Match score is useful but not required for v1.
- **notes/text needed?:** Yes, strongly recommended.
- **Jolly allowed?:** Yes.
- **default points logic:** Final placements should come from the bracket if organizers confirm tournament handling; then map to Palio points and Jolly as usual.
- **special constraints or caveats:** Because the regulation describes a sport match rather than a four-team simultaneous ranking test, `tournament_1v1` is the most plausible v1 mapping. Still, the bracket must be confirmed by admins before use.
- **suspended / ambiguous / manual admin setup confirmation:** Ambiguous enough to require manual admin setup confirmation on format before season use.


### Cameriera

- **game name:** Cameriera
- **competition:** Palio
- **likely v1 format:** `ranking`
- **source confidence:** high
- **regulation clues:** The winner is the team that transports **more water in 4 minutes**, with explicit weight-based penalties for mistakes.
- **enabled result fields likely needed in v1:** `placement`; `score/quantity-like metric` (water amount / weight); `penalties`; `notes/text` optional.
- **notes/text needed?:** Optional.
- **Jolly allowed?:** Yes.
- **default points logic:** Rank by official transported quantity after penalties, then assign Palio points; Jolly may double points.
- **special constraints or caveats:** The source gives clear penalty values in grams, so a ranking template with quantity plus penalties fits well.
- **suspended / ambiguous / manual admin setup confirmation:** Not suspended and not materially ambiguous.


### Corsa — staffetta con i sacchi

- **game name:** Corsa — staffetta con i sacchi
- **competition:** Palio
- **likely v1 format:** `ranking`
- **source confidence:** high
- **regulation clues:** The winner is explicitly the team with the **minor tempo**, but the heading also says the game is **sospeso per l’edizione 2025**.
- **enabled result fields likely needed in v1:** `placement`; `time`; `notes/text` optional.
- **notes/text needed?:** Optional.
- **Jolly allowed?:** Yes, in theory for Palio rules; operationally irrelevant if the game is not run in 2025.
- **default points logic:** If ever re-enabled, rank by fastest valid time and then assign Palio points.
- **special constraints or caveats:** Because the regulation says the game is suspended for 2025 and v1 has no active/visible toggle, it should not be auto-seeded as a playable 2025 game.
- **suspended / ambiguous / manual admin setup confirmation:** Suspended for the 2025 edition. Do not seed by default for the 2025 season.


### Gara di spaghetti

- **game name:** Gara di spaghetti
- **competition:** Palio
- **likely v1 format:** `ranking`
- **source confidence:** high
- **regulation clues:** All four teams compete simultaneously in separate men’s and women’s manches; the final ranking comes from the **sum of the two partial rankings** or, failing completion, the quantified residual spaghetti.
- **enabled result fields likely needed in v1:** `placement`; `score/quantity-like metric` recommended; `notes/text` recommended.
- **notes/text needed?:** Yes, because the official outcome may rely on partial rankings and measured leftovers.
- **Jolly allowed?:** Yes.
- **default points logic:** Use the organizers’ official final team order as the canonical truth; Jolly may double the resulting Palio points.
- **special constraints or caveats:** The native mechanics are multi-step and partly composite. v1 should avoid re-implementing food-weight logic unless organizers explicitly want it; manual placement entry is safer.
- **suspended / ambiguous / manual admin setup confirmation:** Operationally workable, but notes and official manual placement are recommended.


### Patata nel pagliaio

- **game name:** Patata nel pagliaio
- **competition:** Palio
- **likely v1 format:** `ranking`
- **source confidence:** high
- **regulation clues:** The final classification is explicitly based on the **total number of potatoes collected** across the men’s and women’s manches.
- **enabled result fields likely needed in v1:** `placement`; `score/quantity-like metric` (total potatoes); `notes/text` optional.
- **notes/text needed?:** Optional.
- **Jolly allowed?:** Yes.
- **default points logic:** Rank by total collected quantity, then assign Palio points; Jolly may double points.
- **special constraints or caveats:** Straightforward aggregate quantity game; player-age wording remains documentary only in v1.
- **suspended / ambiguous / manual admin setup confirmation:** Not suspended and not materially ambiguous.


### Gioco degli anelli

- **game name:** Gioco degli anelli
- **competition:** Palio
- **likely v1 format:** `ranking`
- **source confidence:** high
- **regulation clues:** The winner is explicitly the team with the **highest total points** across all age categories / attempts.
- **enabled result fields likely needed in v1:** `placement`; `score/quantity-like metric` (total points); `notes/text` optional.
- **notes/text needed?:** Optional.
- **Jolly allowed?:** Yes.
- **default points logic:** Rank by total official points, then assign Palio points; Jolly may double points.
- **special constraints or caveats:** Age-banded participants are informational only in v1. No need to model per-throw detail unless later requested.
- **suspended / ambiguous / manual admin setup confirmation:** Not suspended and not materially ambiguous.


### La catapulta

- **game name:** La catapulta
- **competition:** Palio
- **likely v1 format:** `tournament_1v1`
- **source confidence:** high
- **regulation clues:** The text explicitly says **eliminazione diretta**, with **2 semifinali**, a **finale 3°/4°**, and a **finale 1°/2°**.
- **enabled result fields likely needed in v1:** `placement` (derived from bracket); `notes/text` recommended. Match-level score/quantity is optional, not required for v1.
- **notes/text needed?:** Yes.
- **Jolly allowed?:** Yes.
- **default points logic:** Final placements derive from the bracket, then Palio points are assigned and Jolly may double a team’s points.
- **special constraints or caveats:** This is the clearest Palio-side `tournament_1v1` game in the regulation. Match tiebreak is lower time when deposited-ball count is tied.
- **suspended / ambiguous / manual admin setup confirmation:** Not suspended. Format mapping is clear enough for seeding.


### Vasi comunicanti

- **game name:** Vasi comunicanti
- **competition:** Palio
- **likely v1 format:** `ranking`
- **source confidence:** high
- **regulation clues:** The winner is the team that deposits **more water**; if tied, the winner is the one with the **minor time**.
- **enabled result fields likely needed in v1:** `placement`; `score/quantity-like metric` (water deposited); `time` for tie-break visibility; `notes/text` optional.
- **notes/text needed?:** Optional.
- **Jolly allowed?:** Yes.
- **default points logic:** Rank by official deposited quantity, using time as tie-break where needed; then assign Palio points and Jolly if applicable.
- **special constraints or caveats:** Very suitable for ranking plus a visible tie-break metric.
- **suspended / ambiguous / manual admin setup confirmation:** Not suspended and not materially ambiguous.


### Gioco a sorpresa n.1

- **game name:** Gioco a sorpresa n.1
- **competition:** Palio
- **likely v1 format:** `ranking`
- **source confidence:** low
- **regulation clues:** The regulation lists the game by name only and gives no mechanics in this document.
- **enabled result fields likely needed in v1:** `placement` at minimum; likely `notes/text` required. Any extra field selection must be confirmed manually.
- **notes/text needed?:** Yes, required.
- **Jolly allowed?:** Yes.
- **default points logic:** Use normal Palio points from manual placements once the organizers define the actual rules.
- **special constraints or caveats:** The app cannot infer native scoring, tie-breaks, or even whether ranking is the right fit. `ranking` is only a fallback normalization because v1 needs one of the two supported formats.
- **suspended / ambiguous / manual admin setup confirmation:** Highly ambiguous. Manual admin setup confirmation is required before use.


### Gioco a sorpresa n.2

- **game name:** Gioco a sorpresa n.2
- **competition:** Palio
- **likely v1 format:** `ranking`
- **source confidence:** low
- **regulation clues:** The regulation lists the game by name only and gives no mechanics in this document.
- **enabled result fields likely needed in v1:** `placement` at minimum; likely `notes/text` required. Any extra field selection must be confirmed manually.
- **notes/text needed?:** Yes, required.
- **Jolly allowed?:** Yes.
- **default points logic:** Use normal Palio points from manual placements once the organizers define the actual rules.
- **special constraints or caveats:** Same caveat as surprise game n.1.
- **suspended / ambiguous / manual admin setup confirmation:** Highly ambiguous. Manual admin setup confirmation is required before use.


### Mamanet

- **game name:** Mamanet
- **competition:** Palio
- **likely v1 format:** `tournament_1v1`
- **source confidence:** low
- **regulation clues:** The regulation lists only the name, age restriction, and says the **regolamento verrà inviato successivamente**.
- **enabled result fields likely needed in v1:** `placement` only if confirmed as a bracket game; `notes/text` required until rules exist.
- **notes/text needed?:** Yes, required.
- **Jolly allowed?:** Yes.
- **default points logic:** Cannot be relied on until the actual rules are supplied; if later confirmed as a normal Palio game, its final placements map to normal Palio points and Jolly rules.
- **special constraints or caveats:** The chosen format is only a weak inference from the sport identity, not from the supplied rules. Do not seed automatically as playable without organizer confirmation.
- **suspended / ambiguous / manual admin setup confirmation:** Highly ambiguous and pending later regulation. Manual admin setup confirmation is required.


### Riempi la damigiana

- **game name:** Riempi la damigiana
- **competition:** Palio
- **likely v1 format:** `ranking`
- **source confidence:** high
- **regulation clues:** The winner is explicitly the team that fills the damigiana in the **minor tempo**.
- **enabled result fields likely needed in v1:** `placement`; `time`; `notes/text` optional.
- **notes/text needed?:** Optional.
- **Jolly allowed?:** Yes.
- **default points logic:** Rank by fastest valid time, then assign Palio points; Jolly may double points.
- **special constraints or caveats:** Rule text is clean enough for standard ranking handling.
- **suspended / ambiguous / manual admin setup confirmation:** Not suspended and not materially ambiguous.


### Canzonissima

- **game name:** Canzonissima
- **competition:** Palio
- **likely v1 format:** `ranking`
- **source confidence:** high
- **regulation clues:** The winner is explicitly the team with the **highest points total**, with positive and negative scoring per answer.
- **enabled result fields likely needed in v1:** `placement`; `score/quantity-like metric` (total points); `notes/text` optional.
- **notes/text needed?:** Optional.
- **Jolly allowed?:** Yes.
- **default points logic:** Rank by total official points, then assign Palio points; Jolly may double points.
- **special constraints or caveats:** Two competitors per team alternate by song; no need to model per-song detail in v1.
- **suspended / ambiguous / manual admin setup confirmation:** Not suspended and not materially ambiguous.



## Giocasport

These entries represent the Giocasport games listed in the regulation. They belong to a separate competition area and leaderboard. Jolly never applies here. Most are best normalized as `ranking`, with manual placements entered from the judges’ official outcome.

### Percorso misto

- **game name:** Percorso misto
- **competition:** Giocasport
- **likely v1 format:** `ranking`
- **source confidence:** high
- **regulation clues:** The winner is explicitly the team that completes the course in the **minor tempo**, with explicit **1-second penalties**.
- **enabled result fields likely needed in v1:** `placement`; `time`; `penalties`; `notes/text` optional.
- **notes/text needed?:** Optional.
- **Jolly allowed?:** No.
- **default points logic:** Rank by official time after penalties, then assign Giocasport points only.
- **special constraints or caveats:** Very clean ranking game for v1.
- **suspended / ambiguous / manual admin setup confirmation:** Not suspended and not materially ambiguous.


### Tunnel col pallone

- **game name:** Tunnel col pallone
- **competition:** Giocasport
- **likely v1 format:** `ranking`
- **source confidence:** high
- **regulation clues:** The winner is explicitly the team that completes **5 rounds** in the **minor tempo**.
- **enabled result fields likely needed in v1:** `placement`; `time`; `notes/text` optional.
- **notes/text needed?:** Optional.
- **Jolly allowed?:** No.
- **default points logic:** Rank by fastest valid time, then assign Giocasport points only.
- **special constraints or caveats:** If the ball touches the ground, the attempt restarts from the capofila; no need for deeper game-state modeling in v1.
- **suspended / ambiguous / manual admin setup confirmation:** Not suspended and not materially ambiguous.


### Bandierina

- **game name:** Bandierina
- **competition:** Giocasport
- **likely v1 format:** `ranking`
- **source confidence:** medium
- **regulation clues:** Like the adult version, the text describes numbered calls and infractions rather than a clean fixed bracket.
- **enabled result fields likely needed in v1:** `placement`; `score/quantity-like metric` recommended if organizers want visibility into successful calls; `notes/text` recommended.
- **notes/text needed?:** Yes.
- **Jolly allowed?:** No.
- **default points logic:** Use the official final placements for Giocasport points only.
- **special constraints or caveats:** Same ambiguity pattern as adult Bandierina: repeated duels exist, but a `ranking` normalization is the safest v1 default.
- **suspended / ambiguous / manual admin setup confirmation:** Ambiguous on native mechanics; manual admin confirmation is recommended, but `ranking` is a workable default.


### Pulisci il tuo campo

- **game name:** Pulisci il tuo campo
- **competition:** Giocasport
- **likely v1 format:** `ranking`
- **source confidence:** high
- **regulation clues:** The winner is explicitly the team that ends the 2-minute game with **fewer balls in its own field**.
- **enabled result fields likely needed in v1:** `placement`; `score/quantity-like metric` (ending count of balls); `notes/text` optional.
- **notes/text needed?:** Optional.
- **Jolly allowed?:** No.
- **default points logic:** Rank by official end-state quantity, then assign Giocasport points only.
- **special constraints or caveats:** This is a quantity-based ranking game even though the native play is simultaneous.
- **suspended / ambiguous / manual admin setup confirmation:** Not suspended and not materially ambiguous.


### Piedi neri

- **game name:** Piedi neri
- **competition:** Giocasport
- **likely v1 format:** `ranking`
- **source confidence:** high
- **regulation clues:** The winner is the team that, within **3 minutes**, gets **more players** back with shoes correctly worn and tied.
- **enabled result fields likely needed in v1:** `placement`; `score/quantity-like metric` (valid finished players); `notes/text` optional.
- **notes/text needed?:** Optional.
- **Jolly allowed?:** No.
- **default points logic:** Rank by the official valid quantity, then assign Giocasport points only.
- **special constraints or caveats:** Time is a cap, not the primary ranking metric.
- **suspended / ambiguous / manual admin setup confirmation:** Not suspended and not materially ambiguous.


### Staffetta mista 6x30

- **game name:** Staffetta mista 6x30
- **competition:** Giocasport
- **likely v1 format:** `ranking`
- **source confidence:** high
- **regulation clues:** The winner is explicitly the team with the **minor tempo**; lane invasion can disqualify the team.
- **enabled result fields likely needed in v1:** `placement`; `time`; `notes/text` optional.
- **notes/text needed?:** Optional.
- **Jolly allowed?:** No.
- **default points logic:** Rank by fastest valid time, then assign Giocasport points only.
- **special constraints or caveats:** Disqualifications may need notes.
- **suspended / ambiguous / manual admin setup confirmation:** Not suspended and not materially ambiguous.


### Tieni il ritmo

- **game name:** Tieni il ritmo
- **competition:** Giocasport
- **likely v1 format:** `ranking`
- **source confidence:** high
- **regulation clues:** The winner is explicitly the team that completes **more jumps in 2 minutes** without interrupting rotation.
- **enabled result fields likely needed in v1:** `placement`; `score/quantity-like metric` (valid jumps); `notes/text` optional.
- **notes/text needed?:** Optional.
- **Jolly allowed?:** No.
- **default points logic:** Rank by official jump count, then assign Giocasport points only.
- **special constraints or caveats:** Very clean quantity-based ranking game.
- **suspended / ambiguous / manual admin setup confirmation:** Not suspended and not materially ambiguous.


### Gioco a sorpresa

- **game name:** Gioco a sorpresa
- **competition:** Giocasport
- **likely v1 format:** `ranking`
- **source confidence:** low
- **regulation clues:** The regulation lists the game by name only and provides no mechanics.
- **enabled result fields likely needed in v1:** `placement` at minimum; `notes/text` required until rules are known.
- **notes/text needed?:** Yes, required.
- **Jolly allowed?:** No.
- **default points logic:** Use normal Giocasport points from manual placements once organizers define the rules.
- **special constraints or caveats:** The app cannot infer native scoring or tie-break logic. `ranking` is only a fallback normalization.
- **suspended / ambiguous / manual admin setup confirmation:** Highly ambiguous. Manual admin setup confirmation is required before use.


### Gioco a sorpresa (dall’anno 2021)

- **game name:** Gioco a sorpresa (dall’anno 2021)
- **competition:** Giocasport
- **likely v1 format:** `ranking`
- **source confidence:** low
- **regulation clues:** The regulation lists the game by name only and provides no mechanics.
- **enabled result fields likely needed in v1:** `placement` at minimum; `notes/text` required until rules are known.
- **notes/text needed?:** Yes, required.
- **Jolly allowed?:** No.
- **default points logic:** Use normal Giocasport points from manual placements once organizers define the rules.
- **special constraints or caveats:** Same caveat as the other Giocasport surprise game.
- **suspended / ambiguous / manual admin setup confirmation:** Highly ambiguous. Manual admin setup confirmation is required before use.



## Implementation notes for v1

1. **Seed the catalog, but not blindly.**  
   Games with clear format and outcome signals can be seeded directly. Games marked as ambiguous, suspended, or awaiting later rules should require explicit admin confirmation before becoming part of a playable season setup.

2. **Treat suggested fields as defaults, not hard constraints.**  
   The catalog should drive sensible default field selection per game, but admins may still need to tune notes visibility or optional metrics before results exist.

3. **Do not derive rankings from raw mechanics in v1.**  
   Even when the regulation defines times, penalties, points, or quantities, v1 should usually rely on:
   - official metric entry for visibility, and
   - explicit official placements for the canonical scoring result  
   The important exception is `tournament_1v1`, where final placements are derived from official match winners.

4. **Model Prepalio aggregate as a separate calculated competition item.**  
   It should not be confused with an extra regulation game. The regulation games are the four Prepalio subgames; the aggregate ranking is a derived competition result built from them.

5. **Keep surprise / missing-rule games operationally safe.**  
   For surprise games and Mamanet, the safest v1 behavior is:
   - require admin confirmation of format
   - require notes/text
   - avoid pre-assuming tie-break logic
   - rely on manual placements unless later rules justify more structure

6. **Do not auto-seed the suspended sacks relay for 2025.**  
   Because v1 has no active/visible toggle, the cleanest operational choice is to omit it from the default 2025 playable catalog or seed it only in non-playable admin draft setup.

7. **Roster and eligibility rules stay outside hard enforcement.**  
   Age bands, gender balance, weight caps, and participant counts should be kept as descriptive notes in v1. They are important for organizers but outside the planned enforcement scope.

8. **Use manual admin confirmation especially for these entries:**
   - adult and Giocasport **Bandierina**
   - **Tiro alla fune** (both variants)
   - **Roverino**
   - **Mamanet**
   - all **Gioco a sorpresa** entries
   - any game whose native mechanics later change by organizer clarification

9. **Public-facing terminology should mirror the regulation.**  
   Even when the backend normalizes a game to `ranking` or `tournament_1v1`, the UI should still show the actual regulation-facing game name and any important organizer notes.
