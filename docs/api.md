# Protagons API Reference

**Base URL:** `https://api.usaw.ai/api/v1`

The Protagons API lets you generate, validate, deploy, and browse portable AI character identities (`.protagon.json` files) programmatically.

- [Schema specification](../schema/v1/protagon.schema.json)
- [Dimension reference](dimensions.md)

---

## Quickstart

### 1. Get an API key

Sign in at [protagons.com](https://protagons.com) and create an API key in Account Settings. Keys use the `pg-` prefix.

### 2. Generate a Protagon

Generation is asynchronous — start a job, then poll for the result.

**curl:**

```bash
# Start generation
curl -X POST https://api.usaw.ai/api/v1/generate \
  -H "Authorization: Bearer pg-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Dr. Eleanor Voss",
    "description": "A quantum physicist who explains complex theories through cooking metaphors. Warm but precise, with a habit of turning every conversation into a teaching moment.",
    "google_api_key": "AIza..."
  }'

# Poll for completion
curl https://api.usaw.ai/api/v1/jobs/job_abc123...
```

**Python:**

```python
import requests, time

# Start generation (~2-3 minutes)
job = requests.post("https://api.usaw.ai/api/v1/generate",
    headers={"Authorization": "Bearer pg-your-api-key"},
    json={
        "name": "Dr. Eleanor Voss",
        "description": "A quantum physicist who explains complex theories through cooking metaphors. Warm but precise.",
        "google_api_key": "your-gemini-api-key"
    }
).json()

# Poll for completion
while True:
    status = requests.get(
        f"https://api.usaw.ai/api/v1/jobs/{job['job_id']}",
        headers={"Authorization": "Bearer pg-your-api-key"}
    ).json()
    if status["status"] == "completed":
        protagon = status["result"]
        break
    if status["status"] == "failed":
        raise Exception(status.get("error"))
    print(f"  {status['progress']['agents_completed']}/{status['progress']['agents_total']} agents...")
    time.sleep(5)

# Save it
import json
with open("dr-eleanor-voss.protagon.json", "w") as f:
    json.dump(protagon, f, indent=2)
```

### 3. Use a library Protagon

Fetch a pre-built Protagon and feed its synthesized prompt to any LLM:

```bash
# Fetch a Protagon
curl https://api.usaw.ai/api/v1/library/eager-assistant -o protagon.json

# Extract the prompt and use it with any LLM
jq -r '.synthesized_prompt.content' protagon.json
```

```python
import requests
from openai import OpenAI

# Fetch from library
protagon = requests.get("https://api.usaw.ai/api/v1/library/eager-assistant").json()

# Use with any LLM
client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": protagon["synthesized_prompt"]["content"]},
        {"role": "user", "content": "Help me write a cover letter."}
    ]
)
```

---

## Authentication

The Protagons API uses API keys with the `pg-` prefix (64 hex characters after the prefix).

Include your key via either header:

```
Authorization: Bearer pg-your-api-key
```

```
x-api-key: pg-your-api-key
```

### Auth requirements by endpoint

| Endpoint | Auth Required |
|----------|:------------:|
| `POST /generate` | Yes |
| `POST /generate/from-text` | Yes |
| `POST /recompile` | Yes |
| `POST /chat` | Yes |
| `GET /jobs/:id` | Optional (owner-only access when authenticated) |
| `GET /jobs/:id/stream` | Optional (owner-only access when authenticated) |
| `GET /library` | No |
| `GET /library/:slug` | No |
| `GET /library/:slug/soul.md` | No |
| `POST /validate` | No |
| `POST /deploy` | Yes |
| `POST /deploy/elevenlabs` | Yes |

> **Note:** JWT session tokens (`iss: 'protagons'`) are used by the web app and are not relevant for API consumers. Use API keys for all programmatic access.

---

## BYOK (Bring Your Own Key)

Generation, recompile, and chat endpoints require a Google/Gemini API key. You provide it per-request — Protagons never makes LLM calls on your behalf without your key.

Get a key at [aistudio.google.com/apikey](https://aistudio.google.com/apikey).

### Two modes

**1. Explicit key** — pass the key directly in the request body:

```json
{
  "google_api_key": "AIza...",
  ...
}
```

**2. Stored key** — use a key you've saved in Account Settings (encrypted with AES-256-GCM):

```json
{
  "use_stored_key": true,
  ...
}
```

### Which endpoints use BYOK?

| Endpoint | BYOK Required |
|----------|:------------:|
| `POST /generate` | Yes |
| `POST /generate/from-text` | Yes |
| `POST /recompile` | Yes |
| `POST /chat` | Yes |

### Security

- **Explicit keys** are used for the duration of the request and never stored or logged.
- **Stored keys** are encrypted at rest with AES-256-GCM and decrypted only during request processing.

---

## Supported Models

| Model | Notes |
|-------|-------|
| `gemini-3.1-pro-preview` | Latest |
| `gemini-3.1-pro-preview` | |
| `gemini-3-flash-preview` | |
| `gemini-2.5-pro` | **Default** |
| `gemini-2.5-flash` | Faster, slightly less depth |

- `gemini-2.5-flash-lite` is **rejected** for generation — it lacks the reasoning depth needed for 28-dimension extraction.
- The `/chat` endpoint uses `gemini-2.5-flash` internally and has no model minimum requirement.

---

## Rate Limits

| Scope | Limit | Applies To |
|-------|-------|------------|
| Authenticated requests | 10 req/min per account (or IP) | All auth-required endpoints |
| Public requests | 30 req/min per IP | Library, validate, sitemap |
| Generation capacity | 10 generations/hour per account | `/generate`, `/generate/from-text` |

BYOK generation is **permanently free**. There is one tier with no paid upgrades.

### Rate limit error (per-minute)

```json
{
  "error": "rate_limit_exceeded",
  "message": "Too many requests. Please try again in a minute.",
  "retryAfter": 60
}
```

Rate limit headers (`RateLimit-*`) are included in all responses per the IETF draft standard.

### Generation capacity error (per-hour)

```json
{
  "error": "rate_limit",
  "message": "Rate limit reached (10/hour). Resets at 2026-02-27T03:00:00.000Z.",
  "reset_at": "2026-02-27T03:00:00.000Z",
  "used": 10,
  "limit": 10
}
```

---

## Generation

### POST /generate

Generate a Protagon from a text description. Async — returns a job ID immediately (HTTP 202).

**Auth:** Required | **Rate limit:** 10 req/min | **Generation capacity:** 10/hour

**Request:**

```json
{
  "name": "Dr. Eleanor Voss",
  "description": "A quantum physicist who explains complex theories through cooking metaphors. Warm but precise, with a habit of turning every conversation into a teaching moment.",
  "google_api_key": "AIza...",
  "model": "gemini-2.5-pro",
  "options": {
    "content_tier": "standard"
  },
  "webhook_url": "https://your-server.com/webhook"
}
```

| Field | Type | Required | Description |
|-------|------|:--------:|-------------|
| `name` | string | Yes | Character name (1-200 chars) |
| `description` | string | Yes | Character description (20-50,000 chars) |
| `google_api_key` | string | Conditional | Your Google/Gemini API key. Required unless `use_stored_key` is true. |
| `use_stored_key` | boolean | Conditional | Use your saved encrypted key instead of `google_api_key`. |
| `model` | string | No | Gemini model to use. Default: `gemini-2.5-pro`. See [Supported Models](#supported-models). |
| `options` | object | No | `content_tier`: `"standard"` (default), `"dark"`, or `"adversarial"` |
| `webhook_url` | string | No | HTTPS URL called on job completion or failure. |

**Response (202 Accepted):**

```json
{
  "job_id": "job_a1b2c3d4e5f6...",
  "status": "queued",
  "poll_url": "/api/v1/jobs/job_a1b2c3d4e5f6...",
  "stream_url": "/api/v1/jobs/job_a1b2c3d4e5f6.../stream"
}
```

**Errors:**

| Code | Status | Cause |
|------|--------|-------|
| `validation_error` | 400 | Missing/invalid `name`, `description`, or `webhook_url` |
| `invalid_api_key` | 400 | Google API key is invalid, lacks permission, or quota exceeded |
| `model_insufficient` | 400 | Requested model is too weak (e.g. `gemini-2.5-flash-lite`) |
| `authentication_required` | 401 | Missing or invalid Protagons API key |
| `rate_limit` | 429 | Generation capacity exceeded (10/hour) |
| `rate_limit_exceeded` | 429 | Too many requests per minute |
| `server_error` | 500 | Internal error |

**curl:**

```bash
curl -X POST https://api.usaw.ai/api/v1/generate \
  -H "Authorization: Bearer pg-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Dr. Eleanor Voss",
    "description": "A quantum physicist who explains complex theories through cooking metaphors. Warm but precise, with a habit of turning every conversation into a teaching moment.",
    "google_api_key": "AIza..."
  }'
```

---

### POST /generate/from-text

Generate a Protagon from writing samples (linguistic analysis). Async — returns a job ID (HTTP 202).

**Alias:** `POST /generate/from-samples`

**Auth:** Required | **Rate limit:** 10 req/min | **Generation capacity:** 10/hour

**Request:**

```json
{
  "name": "Author Voice",
  "writing_samples": [
    "First writing sample — a few paragraphs of the author's actual prose...",
    "Second writing sample — different context, same voice..."
  ],
  "google_api_key": "AIza...",
  "model": "gemini-2.5-pro",
  "options": {
    "content_tier": "standard"
  },
  "webhook_url": "https://your-server.com/webhook"
}
```

| Field | Type | Required | Description |
|-------|------|:--------:|-------------|
| `writing_samples` | string[] | Yes | 1-20 writing samples. Must total at least 100 words. |
| `name` | string | No | Voice name (max 200 chars). Defaults to "Analyzed Voice". |
| `google_api_key` | string | Conditional | Your Google/Gemini API key. Required unless `use_stored_key` is true. |
| `use_stored_key` | boolean | Conditional | Use your saved encrypted key instead of `google_api_key`. |
| `model` | string | No | Gemini model. Default: `gemini-2.5-pro`. |
| `options` | object | No | `content_tier`: `"standard"`, `"dark"`, or `"adversarial"` |
| `webhook_url` | string | No | HTTPS URL called on job completion or failure. |

**Response:** Same 202 shape as `/generate`.

**Errors:** Same as `/generate`, plus:

| Code | Status | Cause |
|------|--------|-------|
| `validation_error` | 400 | `writing_samples` not an array, empty, >20 entries, non-string elements, or <100 total words |

**curl:**

```bash
curl -X POST https://api.usaw.ai/api/v1/generate/from-text \
  -H "Authorization: Bearer pg-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "writing_samples": ["The rain hammered the windows like a debt collector..."],
    "google_api_key": "AIza..."
  }'
```

---

### POST /recompile

Recompile the `synthesized_prompt` from a modified `.protagon.json`. Use this after manually editing dimension values. Async — returns a job ID (HTTP 202).

**Alias:** `POST /compile`

**Auth:** Required | **Rate limit:** 10 req/min

**Request:**

```json
{
  "protagon_json": {
    "name": "Dr. Eleanor Voss",
    "dimensions": { ... },
    "prose_description": "...",
    "...": "..."
  },
  "google_api_key": "AIza..."
}
```

| Field | Type | Required | Description |
|-------|------|:--------:|-------------|
| `protagon_json` | object | Yes | The full or partial `.protagon.json` to recompile. |
| `google_api_key` | string | Conditional | Your Google/Gemini API key. Required unless `use_stored_key` is true. |
| `use_stored_key` | boolean | Conditional | Use your saved encrypted key. |

**Response (202 Accepted):**

```json
{
  "job_id": "job_a1b2c3d4e5f6...",
  "status": "queued",
  "poll_url": "/api/v1/jobs/job_a1b2c3d4e5f6...",
  "stream_url": "/api/v1/jobs/job_a1b2c3d4e5f6.../stream"
}
```

Recompile jobs are faster (~10-30 seconds) since they only regenerate the synthesized prompt, not the full 28-dimension extraction.

**Errors:**

| Code | Status | Cause |
|------|--------|-------|
| `validation_error` | 400 | `protagon_json` missing or not an object |
| `invalid_api_key` | 400 | Google API key invalid |
| `authentication_required` | 401 | Missing Protagons API key |
| `server_error` | 500 | Internal error |

**curl:**

```bash
curl -X POST https://api.usaw.ai/api/v1/recompile \
  -H "Authorization: Bearer pg-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "protagon_json": { "name": "Dr. Voss", "dimensions": {} },
    "google_api_key": "AIza..."
  }'
```

---

### POST /chat

Stateless single-turn chat with a Protagon persona. Synchronous — returns the response directly (HTTP 200). BYOK required.

**Auth:** Required | **Rate limit:** 10 req/min

**Request:**

```json
{
  "protagon_json": {
    "name": "Dr. Eleanor Voss",
    "synthesized_prompt": {
      "content": "You ARE Dr. Eleanor Voss..."
    }
  },
  "message": "Explain quantum entanglement like I'm five.",
  "google_api_key": "AIza..."
}
```

| Field | Type | Required | Description |
|-------|------|:--------:|-------------|
| `protagon_json` | object | Yes | A `.protagon.json` object. Must include `name` (string). Uses `synthesized_prompt.content` if available, otherwise builds prompt from `prose_description`, `signature_patterns`, `replication_recommendations`. |
| `message` | string | Yes | User message (1-10,000 chars). |
| `google_api_key` | string | Conditional | Your Google/Gemini API key. Required unless `use_stored_key` is true. |
| `use_stored_key` | boolean | Conditional | Use your saved encrypted key. |

**Response (200):**

```json
{
  "response": "Oh, quantum entanglement! Think of it like making two cookies from the same dough...",
  "voice_name": "Dr. Eleanor Voss",
  "model": "gemini-2.5-flash"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `response` | string | The persona's reply. |
| `voice_name` | string | Name from the provided `protagon_json`. |
| `model` | string | Gemini model used (always `gemini-2.5-flash`). |

Chat uses `gemini-2.5-flash` internally. There is no model minimum — even `flash-lite` keys work for chat.

**Errors:**

| Code | Status | Cause |
|------|--------|-------|
| `validation_error` | 400 | Missing `protagon_json`, `protagon_json.name`, or `message`; message >10,000 chars |
| `invalid_api_key` | 400 | Google API key invalid |
| `authentication_required` | 401 | Missing Protagons API key |
| `quota_exceeded` | 429 | Google API key quota exceeded |
| `llm_error` | 502 | No response from language model |
| `server_error` | 500 | Internal error |

**curl:**

```bash
curl -X POST https://api.usaw.ai/api/v1/chat \
  -H "Authorization: Bearer pg-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "protagon_json": {
      "name": "Dr. Eleanor Voss",
      "synthesized_prompt": { "content": "You ARE Dr. Eleanor Voss..." }
    },
    "message": "Explain quantum entanglement like I'\''m five.",
    "google_api_key": "AIza..."
  }'
```

---

## Job Status

### GET /jobs/:id

Poll job status. Returns progress for in-flight jobs and the full result on completion.

**Auth:** Optional (owner-only when authenticated) | **Rate limit:** 10 req/min

**Response (200) — processing:**

```json
{
  "job_id": "job_a1b2c3d4e5f6...",
  "status": "processing",
  "progress": {
    "status": "processing",
    "agents_completed": 14,
    "agents_total": 30,
    "current_agent": "emotional_architecture",
    "fields_extracted": 156,
    "estimated_seconds_remaining": 70
  },
  "created_at": "2026-02-27T01:23:45.000Z",
  "completed_at": null
}
```

**Response (200) — completed:**

```json
{
  "job_id": "job_a1b2c3d4e5f6...",
  "status": "completed",
  "progress": {
    "status": "completed",
    "agents_completed": 30,
    "agents_total": 30,
    "fields_extracted": 287,
    "estimated_seconds_remaining": 0
  },
  "created_at": "2026-02-27T01:23:45.000Z",
  "completed_at": "2026-02-27T01:26:12.000Z",
  "result": { ... }
}
```

The `result` field contains the full `.protagon.json` when status is `completed`.

**Response (200) — failed:**

```json
{
  "job_id": "job_a1b2c3d4e5f6...",
  "status": "failed",
  "progress": { "status": "failed", "error": "..." },
  "created_at": "2026-02-27T01:23:45.000Z",
  "completed_at": "2026-02-27T01:24:01.000Z",
  "error": "Generation failed"
}
```

**Status values:** `queued` → `processing` → `completed` | `failed`

**Errors:**

| Code | Status | Cause |
|------|--------|-------|
| `not_found` | 404 | Job ID does not exist |
| `forbidden` | 403 | Authenticated user is not the job owner |
| `server_error` | 500 | Internal error |

**curl:**

```bash
curl https://api.usaw.ai/api/v1/jobs/job_a1b2c3d4e5f6... \
  -H "Authorization: Bearer pg-your-api-key"
```

---

### GET /jobs/:id/stream

SSE (Server-Sent Events) endpoint for real-time job progress. Keeps the connection open and sends progress events as the job runs.

**Auth:** Optional (owner-only when authenticated)

Events are JSON objects in the same shape as the `progress` field from polling:

```
data: {"status":"processing","agents_completed":14,"agents_total":30,"current_agent":"emotional_architecture","fields_extracted":156,"estimated_seconds_remaining":70}

data: {"status":"processing","agents_completed":20,"agents_total":30,"current_agent":"identity_construction","fields_extracted":210,"estimated_seconds_remaining":40}

data: {"status":"completed","agents_completed":30,"agents_total":30,"estimated_seconds_remaining":0}
```

A keepalive comment (`: keepalive`) is sent every 15 seconds.

If the job is already completed or failed when you connect, a single event is sent and the connection closes.

**JavaScript:**

```javascript
const es = new EventSource("https://api.usaw.ai/api/v1/jobs/job_a1b2c3d4e5f6.../stream");

es.onmessage = (event) => {
  const progress = JSON.parse(event.data);
  console.log(`${progress.agents_completed}/${progress.agents_total} agents`);

  if (progress.status === "completed" || progress.status === "failed") {
    es.close();
    // Fetch the full result via polling endpoint
    fetch(`https://api.usaw.ai/api/v1/jobs/job_a1b2c3d4e5f6...`)
      .then(r => r.json())
      .then(job => console.log(job.result));
  }
};
```

**Errors:**

| Code | Status | Cause |
|------|--------|-------|
| `not_found` | 404 | Job ID does not exist |
| `forbidden` | 403 | Authenticated user is not the job owner |

---

## Library (Public)

### GET /library

Paginated, searchable access to the Protagons library. Public — no auth required.

**Rate limit:** 30 req/min

**Query parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `page` | integer | `1` | Page number (min 1) |
| `limit` | integer | `20` | Items per page (1-100) |
| `category` | string | — | Filter by category (e.g. `professional`, `creative`) |
| `search` | string | — | Search by name or slug (case-insensitive) |

**Response (200):**

```json
{
  "items": [
    {
      "name": "The Eager Assistant",
      "slug": "eager-assistant",
      "tagline": "Helpful, precise, and relentlessly cheerful.",
      "category": "professional",
      "content_tier": "standard",
      "tags": ["helpful", "precise"],
      "personality": "Warm, detail-oriented problem solver who gets genuinely excited about helping.",
      "url": "/api/v1/library/eager-assistant"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 865,
    "pages": 44
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `items[].name` | string | Display name |
| `items[].slug` | string | URL-safe identifier |
| `items[].tagline` | string\|null | Short enriched tagline |
| `items[].category` | string\|null | Content category |
| `items[].content_tier` | string | `"standard"`, `"dark"`, or `"adversarial"` |
| `items[].tags` | string[] | Tag list |
| `items[].personality` | string\|null | Enriched personality summary |
| `items[].url` | string | Relative API path to fetch the full Protagon |
| `pagination.page` | integer | Current page |
| `pagination.limit` | integer | Items per page |
| `pagination.total` | integer | Total items matching query |
| `pagination.pages` | integer | Total pages |

Response is cached (`Cache-Control: public, max-age=300`).

**curl:**

```bash
curl "https://api.usaw.ai/api/v1/library?search=detective&limit=5"
```

---

### GET /library/:slug

Fetch a single Protagon as a full `.protagon.json`. Public — no auth required.

**Rate limit:** 30 req/min

Returns the complete Protagon object with all 28 dimensions, personality axes, synthesized prompt, deployment metadata, and more.

**Response (200):**

The full `.protagon.json` object. See the [schema specification](../schema/v1/protagon.schema.json) for the complete structure.

Key fields:

| Field | Description |
|-------|-------------|
| `name` | Character name |
| `slug` | URL-safe identifier |
| `synthesized_prompt.content` | Ready-to-use system prompt for any LLM |
| `dimensions.*` | 28 linguistic dimension objects (287 total fields) |
| `personality` | Personality axes (formal/casual, analytical/emotional, etc.) |
| `prose_description` | Human-readable voice description |
| `deployment` | Content tier, safety metadata |
| `generation` | How/when the Protagon was generated |

Response is cached (`Cache-Control: public, max-age=3600`).

**Errors:**

| Code | Status | Cause |
|------|--------|-------|
| `not_found` | 404 | No Protagon with that slug in the library |
| `server_error` | 500 | Internal error |

**curl:**

```bash
curl https://api.usaw.ai/api/v1/library/eager-assistant
```

---

### GET /library/:slug/soul.md

Fetch the pre-generated SOUL.md for a library voice. Returns raw Markdown. Public — no auth required.

**Rate limit:** 30 req/min

**Response (200):**

Content-Type: `text/markdown; charset=utf-8`

The response body is raw Markdown text (not JSON).

Response is cached (`Cache-Control: public, max-age=3600`).

**Errors:**

| Code | Status | Cause |
|------|--------|-------|
| `not_found` | 404 | Protagon not found in library |
| `not_generated` | 404 | Protagon exists but SOUL.md has not been generated yet |
| `server_error` | 500 | Internal error |

**curl:**

```bash
curl https://api.usaw.ai/api/v1/library/eager-assistant/soul.md
```

---

## Validation (Public)

### POST /validate

Validate a `.protagon.json` against the schema. Public — no auth required.

**Rate limit:** 30 req/min

**Request:**

```json
{
  "protagon_json": {
    "name": "Dr. Eleanor Voss",
    "spec_version": "1.0.0",
    "dimensions": { ... },
    "synthesized_prompt": { "content": "..." },
    "deployment": { "content_tier": "standard" }
  }
}
```

| Field | Type | Required | Description |
|-------|------|:--------:|-------------|
| `protagon_json` | object | Yes | The `.protagon.json` object to validate. |

**Response (200):**

```json
{
  "valid": true,
  "errors": [],
  "warnings": [
    {
      "field": "dimensions",
      "message": "Only 20/28 facets present. Full extraction yields 287 fields."
    }
  ],
  "stats": {
    "dimensions": 20,
    "has_synthesized_prompt": true,
    "has_deployment": true,
    "has_generation": false,
    "content_tier": "standard"
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `valid` | boolean | `true` if no errors (warnings don't affect validity) |
| `errors` | object[] | Validation errors. Each has `field` and `message`. |
| `warnings` | object[] | Non-blocking warnings. Each has `field` and `message`. |
| `stats.dimensions` | integer | Number of dimension facets present |
| `stats.has_synthesized_prompt` | boolean | Whether a synthesized prompt exists |
| `stats.has_deployment` | boolean | Whether deployment metadata exists |
| `stats.has_generation` | boolean | Whether generation metadata exists |
| `stats.content_tier` | string | Detected content tier or `"unknown"` |

**Validation checks:**

- **Errors** (make `valid: false`):
  - `name` is required
  - `spec_version` is required and must be semver (e.g. `"1.0.0"`)
  - `personality` axes (`formal_casual`, `analytical_emotional`, `authoritative_collaborative`, `serious_playful`, `concise_elaborate`) must be numbers between 0 and 1
  - `deployment.content_tier` must be one of: `standard`, `dark`, `adversarial`

- **Warnings** (informational, `valid` is still `true`):
  - Missing `prose_description` (recommended for best results)
  - Missing `synthesized_prompt` (LLM integration may be limited)
  - Missing or empty `dimensions` (voice will lack depth)
  - Missing `deployment` metadata
  - Fewer than 28 facets in `dimensions`

**Errors:**

| Code | Status | Cause |
|------|--------|-------|
| `validation_error` | 400 | `protagon_json` missing or not an object |
| `server_error` | 500 | Internal error |

**curl:**

```bash
curl -X POST https://api.usaw.ai/api/v1/validate \
  -H "Content-Type: application/json" \
  -d '{
    "protagon_json": {
      "name": "Test",
      "spec_version": "1.0.0"
    }
  }'
```

---

## Deploy

### POST /deploy

Deploy a Protagon to a third-party platform. The platform creates an agent/assistant configured with the Protagon's synthesized prompt.

**Auth:** Required | **Rate limit:** 10 req/min

Currently supported via REST API: **ElevenLabs** (Conversational AI).

> Other platforms (Bland, Vapi, Retell, OpenAI Assistants) are available through the [Python SDK](https://pypi.org/project/protagons/) — see [integrations.md](integrations.md) for details.

**Request:**

```json
{
  "protagon_slug": "eager-assistant",
  "platform": "elevenlabs",
  "api_key": "your-elevenlabs-api-key",
  "options": {
    "agent_name": "Custom Agent Name",
    "first_message": "Hello! How can I help?",
    "voice_id": "optional-elevenlabs-voice-id"
  }
}
```

| Field | Type | Required | Description |
|-------|------|:--------:|-------------|
| `protagon_slug` | string | Yes | Slug of a Protagon from the library. |
| `platform` | string | Yes | Target platform. Currently: `elevenlabs`. |
| `api_key` | string | Yes | Your API key for the target platform (used once, never stored). |
| `options` | object | No | Platform-specific overrides. |

**ElevenLabs options:**

| Option | Type | Description |
|--------|------|-------------|
| `agent_name` | string | Override the agent name (defaults to Protagon name) |
| `first_message` | string | Custom greeting (defaults to "Hello, I'm {name}.") |
| `voice_id` | string | ElevenLabs voice ID. If omitted and the Protagon has a `voice_prompt` in TTS config, a voice is auto-designed. |

**Response (200):**

```json
{
  "platform": "elevenlabs",
  "agent_id": "agent_abc123...",
  "protagon": "eager-assistant",
  "deployed_at": "2026-02-27T12:00:00.000Z",
  "deployed_prompt_hash": "a1b2c3d4...",
  "voice_id": "voice_xyz789..."
}
```

| Field | Type | Description |
|-------|------|-------------|
| `platform` | string | Platform deployed to |
| `agent_id` | string | ID of the created agent on the platform |
| `protagon` | string | Protagon slug that was deployed |
| `deployed_at` | string | ISO 8601 timestamp |
| `deployed_prompt_hash` | string | SHA-256 hash of the deployed prompt (for change detection) |
| `voice_id` | string | ElevenLabs voice ID (included when a voice was used or created) |

**Errors:**

| Code | Status | Cause |
|------|--------|-------|
| `validation_error` | 400 | Missing `protagon_slug`, `api_key`, or invalid `platform` |
| `authentication_required` | 401 | Missing Protagons API key |
| `deploy_error` | 404 | Protagon slug not found |
| `deploy_error` | 502 | Platform API error (key invalid, quota, etc.) |
| `server_error` | 500 | Internal error |

**curl:**

```bash
curl -X POST https://api.usaw.ai/api/v1/deploy \
  -H "Authorization: Bearer pg-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "protagon_slug": "eager-assistant",
    "platform": "elevenlabs",
    "api_key": "your-elevenlabs-api-key"
  }'
```

---

### POST /deploy/elevenlabs

Platform-specific shortcut — identical to `POST /deploy` with `platform` preset to `elevenlabs`. The `platform` field is not required in the request body.

**Auth:** Required | **Rate limit:** 10 req/min

**curl:**

```bash
curl -X POST https://api.usaw.ai/api/v1/deploy/elevenlabs \
  -H "Authorization: Bearer pg-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "protagon_slug": "eager-assistant",
    "api_key": "your-elevenlabs-api-key"
  }'
```

---

## Sitemap

### GET /sitemap.xml

Returns an XML sitemap of all public Protagons library pages. Used by search engines.

**Rate limit:** 30 req/min

**Response:** `Content-Type: application/xml`, cached for 1 hour.

---

## Webhook Callbacks

When you provide a `webhook_url` with a generation request, Protagons sends an HTTPS POST to your URL when the job completes or fails.

**Requirements:**
- URL must use HTTPS
- Your server should respond with a 2xx status

**Completion payload:**

```json
{
  "job_id": "job_a1b2c3d4e5f6...",
  "status": "completed",
  "result": { ... }
}
```

**Failure payload:**

```json
{
  "job_id": "job_a1b2c3d4e5f6...",
  "status": "failed",
  "error": "Generation failed"
}
```

---

## Error Reference

All errors follow this shape:

```json
{
  "error": "error_code",
  "message": "Human-readable description."
}
```

Some errors include additional fields (e.g. `supported_models`, `reset_at`, `retryAfter`).

| Error Code | HTTP Status | Description |
|------------|:-----------:|-------------|
| `validation_error` | 400 | Invalid request body, missing required fields, or field constraints violated |
| `invalid_api_key` | 400 / 401 | Google API key invalid, lacking permissions, or quota exceeded; or Protagons API key invalid/revoked |
| `model_insufficient` | 400 | Requested Gemini model lacks reasoning depth for generation (includes `supported_models` array) |
| `invalid_token` | 401 | JWT session token invalid or expired (web app only) |
| `authentication_required` | 401 | Endpoint requires auth but no valid API key or token was provided |
| `forbidden` | 403 | Authenticated but not authorized (e.g. viewing another user's job) |
| `not_found` | 404 | Job, Protagon, or resource not found |
| `not_generated` | 404 | Resource exists but requested sub-resource not yet generated (e.g. SOUL.md) |
| `rate_limit` | 429 | Hourly generation capacity exceeded (includes `reset_at`, `used`, `limit`) |
| `rate_limit_exceeded` | 429 | Per-minute request rate limit exceeded (includes `retryAfter`) |
| `quota_exceeded` | 429 | Google API key quota exceeded |
| `auth_error` | 500 | Authentication service temporarily unavailable |
| `llm_error` | 502 | No response from language model |
| `deploy_error` | 404 / 502 | Deployment failed — Protagon not found (404) or platform API error (502) |
| `server_error` | 500 | Internal server error |
