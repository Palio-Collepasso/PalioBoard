### `<error_code>`

- **Status:** `<http status>`
- **Category:** `<validation | auth | authz | lookup | domain | concurrency | internal>`
- **Retryable:** `<yes | no | depends>`
- **Client action:** `<what client should do>`
- **Meaning:** `<short stable meaning>`
- **When returned:**
  - `<condition 1>`
  - `<condition 2>`
- **Must not be used for:**
  - `<similar but different case>`
- **Payload details:**
  - `<field>`: `<meaning>`
  - `<field>`: `<meaning>`
- **Security/privacy notes:** `<what must not be leaked>`
- **Example response:**

```json
{
  "error": {
    "code": "<error_code>",
    "message": "<message>",
    "details": {},
    "request_id": "<request_id>"
  }
}
```

- **Related endpoints:**
  - `<method> <path>`
  - `<method> <path>`
- **Related domain rules:**
  - `<rule id>`
  - `<rule id>`
