# Synthesized Prompt

The `synthesized_prompt` is the compiled output of a Protagon — a single system prompt that any LLM can use to fully embody the character identity.

## How It Works

1. **28 AI agents** analyze dimensions independently (rhetorical architecture, emotional patterns, cultural markers, etc.)
2. Each agent extracts structured fields for its dimension
3. The **synthesized prompt compiler** reads all 28 dimensions and produces a single, coherent system prompt
4. The prompt includes writing style instructions, voice guidelines, personality traits, and behavioral boundaries

## Structure

```json
{
  "synthesized_prompt": {
    "content": "You are Dr. Eleanor Voss, a quantum physicist who...",
    "compiler": "protagons-api-v1",
    "compiled_at": "2026-02-23T15:30:00.000Z",
    "dimensions_hash": "a1b2c3d4...",
    "word_count": 847,
    "source_dimensions": 28
  }
}
```

| Field | Description |
|-------|-------------|
| `content` | The full system prompt text |
| `compiler` | Which compiler generated it (`protagons-api-v1` or `usaw-platform-v2`) |
| `compiled_at` | ISO 8601 timestamp |
| `dimensions_hash` | Hash of the source dimensions (changes if you edit dimensions) |
| `word_count` | Prompt word count |
| `source_dimensions` | How many of the 28 dimensions contributed |

## Using the Prompt

### OpenAI

```python
response = openai.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": protagon["synthesized_prompt"]["content"]},
        {"role": "user", "content": "Your prompt here"}
    ]
)
```

### Anthropic

```python
message = anthropic.messages.create(
    model="claude-sonnet-4-20250514",
    system=protagon["synthesized_prompt"]["content"],
    messages=[{"role": "user", "content": "Your prompt here"}]
)
```

### Google Gemini

```python
model = genai.GenerativeModel(
    model_name="gemini-2.5-pro",
    system_instruction=protagon["synthesized_prompt"]["content"]
)
response = model.generate_content("Your prompt here")
```

## Recompilation

If you manually edit a Protagon's dimensions (e.g., adjust the emotional architecture or change the formality level), the synthesized prompt becomes stale. Use the recompile endpoint to regenerate it:

```bash
curl -X POST https://api.usaw.ai/api/v1/recompile \
  -H "Authorization: Bearer pg-your-key" \
  -H "Content-Type: application/json" \
  -d '{"protagon_json": {...}, "google_api_key": "AIza..."}'
```

This produces a new `synthesized_prompt` that reflects your changes. The `dimensions_hash` will update to match.
