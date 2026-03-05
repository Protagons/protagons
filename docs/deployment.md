# Deployment Metadata

Every Protagon includes a `deployment` block that describes how the character should be used in production systems.

## Structure

```json
{
  "deployment": {
    "content_tier": "standard",
    "requires_fiction_wrapper": false,
    "age_gate_required": false,
    "model_notes": null,
    "recommended_context": "general"
  }
}
```

## Content Tiers

| Tier | Description | Fiction Wrapper | Age Gate |
|------|-------------|-----------------|----------|
| `standard` | General-purpose characters | No | No |
| `dark` | Morally complex, dark themes | Yes | Yes |
| `adversarial` | Antagonistic, villain archetypes | Yes | Yes |

### Standard
Safe for all contexts. No restrictions on deployment.

### Dark
Characters with dark themes — trauma, moral ambiguity, complex villains. The consuming application should:
- Wrap output in a fiction context (e.g., "The following is a creative writing exercise...")
- Implement age verification before displaying content
- Consider adding content warnings

### Adversarial
Intentionally antagonistic characters designed for creative fiction. The consuming application should:
- Always present in a clear fiction context
- Never deploy in customer-facing support or advice contexts
- Implement age verification
- Consider pairing with a safety system that can detect if the user is in genuine distress

## Recommended Context

| Value | Meaning |
|-------|---------|
| `general` | Any context — chat, writing, content generation |
| `fiction_only` | Creative writing, storytelling, worldbuilding only |
| `educational` | Classroom, training, demonstration purposes |
| `internal` | Internal tools, testing, development |

## Model Notes

Optional free-text field for deployment guidance specific to this character. Examples:
- "Works best with models that support long system prompts (>2000 tokens)"
- "Temperature 0.8-1.0 recommended for this character's creative range"
- "Pair with content filtering for production deployment"

## Generation Metadata

The `generation` block tracks provenance:

```json
{
  "generation": {
    "generated_via": "protagons-api-v1",
    "generated_at": "2026-02-23T15:30:00.000Z",
    "provider": "google",
    "model": "gemini-2.5-pro",
    "api_version": "v1"
  }
}
```

This tells you how the Protagon was created — useful for auditing, quality tracking, and version management.

## Integrations

The optional `integrations` field records deployment state for third-party platforms. It is populated by the deploy API or Python SDK and should not be manually edited.

```json
{
  "integrations": {
    "elevenlabs": {
      "agent_id": "agent_xxx",
      "deployed_at": "2026-02-24T12:00:00.000Z",
      "deployed_prompt_hash": "sha256...",
      "auto_sync": false
    },
    "openclaw": {
      "workspace_path": "/home/user/openclaw",
      "deployed_at": "2026-02-24T12:00:00.000Z",
      "deployed_prompt_hash": "sha256..."
    }
  }
}
```

### Supported Platforms

| Key | Platform | Agent ID Format |
|-----|----------|-----------------|
| `elevenlabs` | ElevenLabs Conversational AI | ElevenLabs agent ID |
| `openai_assistant` | OpenAI Assistants API | `asst_...` |
| `bland` | Bland AI | Bland agent ID |
| `vapi` | Vapi | Vapi assistant ID |
| `retell` | Retell | Retell agent ID |
| `openclaw` | OpenClaw | Workspace path (local) |

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `agent_id` | string/null | Platform-specific agent identifier |
| `deployed_at` | string/null | ISO 8601 timestamp of last deploy |
| `deployed_prompt_hash` | string/null | SHA-256 of deployed prompt (for drift detection) |
| `auto_sync` | boolean | Whether to auto-deploy on prompt changes |

See [integrations.md](integrations.md) for the full Python SDK and REST API reference.
