### JOLLY_ALREADY_USED

* **Type**: `https://api.palioboard.local/problems/jolly-already-used`
* **Category**: `business_rule`
* **HTTP status**: `409`
* **Retry policy**: `never`
* **Safe to expose**: `true`
* **Translation key**: `errors.jollyAlreadyUsed`

#### Meaning

The selected team has already consumed its Jolly in a previous game, so the current result cannot be accepted as submitted.

#### Context schema

| Field              | Type   | Required | Notes                                         |
| ------------------ | ------ | -------: | --------------------------------------------- |
| `team_id`          | `uuid` |      yes | Team using the Jolly                          |
| `game_id`          | `uuid` |      yes | Current game being saved                      |
| `previous_game_id` | `uuid` |       no | Earlier game where the Jolly was already used |

#### Example

```json
{
  "type": "https://api.palioboard.local/problems/jolly-already-used",
  "code": "JOLLY_ALREADY_USED",
  "title": "Jolly already used",
  "status": 409,
  "context": {
    "team_id": "01956c9f-6f7e-7b42-a4b0-2d21d920c001",
    "game_id": "01956ca0-0c77-7b98-a328-39c9f8a31002",
    "previous_game_id": "01956ca0-53dd-7162-b78a-4bdb9368b003"
  }
}
```
