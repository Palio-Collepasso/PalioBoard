# Game Catalog

## Purpose
This is the compact seeded game-setup reference for v1.
Use it when you need the expected competition, format, likely fields, Jolly applicability, and whether a game needs manual setup confirmation.

## Document boundary
This file owns **per-game setup reference data**.
It does **not** re-explain global competition rules or trust invariants:
- global scope and invariants live in `docs/domain/business-rules.md` and `docs/product/functional-requirements.md`
- event or regulation background lives in `docs/domain/palio-context.md`
- schema shape lives in `docs/domain/er-schema.md`

## Shared assumptions
- v1 supports exactly three competition contexts: Palio, Prepalio, Giocasport.
- v1 assumes exactly four teams.
- Supported formats are `ranking` and `tournament_1v1`.
- Jolly is Palio-only.
- Once official result data exists, game setup is immutable.
- Player-level eligibility, roster, age-band, and equipment checks are out of v1 application scope unless explicitly promoted elsewhere.

## How to use
1. Find the game by competition and name.
2. Use the listed format and likely fields as the default seed or setup baseline.
3. If the setup note says manual confirmation is required, do not auto-assume the ambiguous format.

## Prepalio

| Game | Format | Likely fields | Jolly | Confidence | Setup note |
|---|---|---|---|---|---|
| Streetball misto | `tournament_1v1` | placement (derived from bracket); notes/text optional. Match score is useful for display but not… | No. | high | Not suspended. Format mapping is clear enough for seeding. |
| Bocce misto | `tournament_1v1` | placement (derived from bracket); notes/text optional. | No. | high | Not suspended. Format mapping is clear enough for seeding. |
| Ping pong misto | `tournament_1v1` | placement (derived from bracket); notes/text optional. | No. | high | Not suspended. Format mapping is clear enough for seeding. |
| Calciotennis maschile | `tournament_1v1` | placement (derived from bracket); notes/text optional. Match score / set summary is optional, not… | No. | high | Not suspended. Format mapping is clear enough for seeding. |

Prepalio notes:
- Prepalio subgames feed a Prepalio aggregate ranking, which then contributes points to the main Palio standings.

## Palio

| Game | Format | Likely fields | Jolly | Confidence | Setup note |
|---|---|---|---|---|---|
| Tiro alla fune — maschile | `tournament_1v1` | placement (derived from bracket if confirmed); notes/text recommended. | Yes. | medium | Ambiguous enough to require manual admin setup confirmation on format before season use. |
| Tiro alla fune — femminile | `tournament_1v1` | placement (derived from bracket if confirmed); notes/text recommended. | Yes. | medium | Ambiguous enough to require manual admin setup confirmation on format before season use. |
| Bandierina | `ranking` | placement; score/quantity-like metric recommended for round wins / successful calls if organizers… | Yes. | medium | Ambiguous on native mechanics; manual admin confirmation is recommended, but ranking is a workable… |
| Gimkana con la bici | `ranking` | placement; time; penalties; notes/text optional. | Yes. | high | Not suspended and not materially ambiguous. |
| Volpe zoppa e gatto cieco | `ranking` | placement; time; notes/text optional. | Yes. | high | Not suspended and not materially ambiguous. |
| Corsa con la carriola | `ranking` | placement; score/quantity-like metric (water carried); notes/text optional. | Yes. | high | Not suspended and not materially ambiguous. |
| Lancio delle uova | `ranking` | placement; score/quantity-like metric (longest valid distance / round reached); notes/text optional. | Yes. | high | Not suspended and not materially ambiguous. |
| Corsa staffetta | `ranking` | placement; time; notes/text optional. | Yes. | high | Not suspended and not materially ambiguous. |
| Passami la mela | `ranking` | placement; score/quantity-like metric (valid apples transferred); notes/text optional. | Yes. | high | Slightly caveated but still workable as a normal ranking game. |
| Tieni il ritmo misto | `ranking` | placement; score/quantity-like metric (valid jumps); notes/text optional. | Yes. | high | Not suspended and not materially ambiguous. |
| Ti faresti guidare da un uomo | `ranking` | placement; time; penalties; notes/text optional. | Yes. | high | Not suspended and not materially ambiguous. |
| Roverino | `tournament_1v1` | placement (derived from bracket if confirmed); notes/text recommended. Match score is useful but… | Yes. | medium | Ambiguous enough to require manual admin setup confirmation on format before season use. |
| Cameriera | `ranking` | placement; score/quantity-like metric (water amount / weight); penalties; notes/text optional. | Yes. | high | Not suspended and not materially ambiguous. |
| Corsa — staffetta con i sacchi | `ranking` | placement; time; notes/text optional. | Yes, in theory… | high | Suspended for the 2025 edition. Do not seed by default for the 2025 season. |
| Gara di spaghetti | `ranking` | placement; score/quantity-like metric recommended; notes/text recommended. | Yes. | high | Operationally workable, but notes and official manual placement are recommended. |
| Patata nel pagliaio | `ranking` | placement; score/quantity-like metric (total potatoes); notes/text optional. | Yes. | high | Not suspended and not materially ambiguous. |
| Gioco degli anelli | `ranking` | placement; score/quantity-like metric (total points); notes/text optional. | Yes. | high | Not suspended and not materially ambiguous. |
| La catapulta | `tournament_1v1` | placement (derived from bracket); notes/text recommended. Match-level score/quantity is optional,… | Yes. | high | Not suspended. Format mapping is clear enough for seeding. |
| Vasi comunicanti | `ranking` | placement; score/quantity-like metric (water deposited); time for tie-break visibility; notes/text… | Yes. | high | Not suspended and not materially ambiguous. |
| Gioco a sorpresa n.1 | `ranking` | placement at minimum; likely notes/text required. Any extra field selection must be confirmed… | Yes. | low | Highly ambiguous. Manual admin setup confirmation is required before use. |
| Gioco a sorpresa n.2 | `ranking` | placement at minimum; likely notes/text required. Any extra field selection must be confirmed… | Yes. | low | Highly ambiguous. Manual admin setup confirmation is required before use. |
| Mamanet | `tournament_1v1` | placement only if confirmed as a bracket game; notes/text required until rules exist. | Yes. | low | Highly ambiguous and pending later regulation. Manual admin setup confirmation is required. |
| Riempi la damigiana | `ranking` | placement; time; notes/text optional. | Yes. | high | Not suspended and not materially ambiguous. |
| Canzonissima | `ranking` | placement; score/quantity-like metric (total points); notes/text optional. | Yes. | high | Not suspended and not materially ambiguous. |

Palio notes:
- Most non-bracket Palio games use `ranking`; ambiguous quadrangolare-style games may require organizer confirmation.

## Giocasport

| Game | Format | Likely fields | Jolly | Confidence | Setup note |
|---|---|---|---|---|---|
| Percorso misto | `ranking` | placement; time; penalties; notes/text optional. | No. | high | Not suspended and not materially ambiguous. |
| Tunnel col pallone | `ranking` | placement; time; notes/text optional. | No. | high | Not suspended and not materially ambiguous. |
| Bandierina | `ranking` | placement; score/quantity-like metric recommended if organizers want visibility into successful… | No. | medium | Ambiguous on native mechanics; manual admin confirmation is recommended, but ranking is a workable… |
| Pulisci il tuo campo | `ranking` | placement; score/quantity-like metric (ending count of balls); notes/text optional. | No. | high | Not suspended and not materially ambiguous. |
| Piedi neri | `ranking` | placement; score/quantity-like metric (valid finished players); notes/text optional. | No. | high | Not suspended and not materially ambiguous. |
| Staffetta mista 6x30 | `ranking` | placement; time; notes/text optional. | No. | high | Not suspended and not materially ambiguous. |
| Tieni il ritmo | `ranking` | placement; score/quantity-like metric (valid jumps); notes/text optional. | No. | high | Not suspended and not materially ambiguous. |
| Gioco a sorpresa | `ranking` | placement at minimum; notes/text required until rules are known. | No. | low | Highly ambiguous. Manual admin setup confirmation is required before use. |
| Gioco a sorpresa (dall’anno 2021) | `ranking` | placement at minimum; notes/text required until rules are known. | No. | low | Highly ambiguous. Manual admin setup confirmation is required before use. |

Giocasport notes:
- Giocasport standings stay separate from the main Palio standings.
