# Voice Platform Examples

Deploy Protagon identities to voice AI platforms.

## Prerequisites

```bash
pip install protagons[voice]
```

## Examples

| File | Platform | Description |
|------|----------|-------------|
| `elevenlabs_agent.py` | ElevenLabs | Conversational AI agent |
| `bland_agent.py` | Bland AI | Phone call agent |
| `vapi_assistant.py` | Vapi | Voice assistant |
| `retell_agent.py` | Retell | Voice agent with custom LLM |

## Quick Start

```bash
export ELEVENLABS_API_KEY=xi-...
python elevenlabs_agent.py path/to/character.protagon.json
```

See the [full integration docs](https://protagons.com/integrations) for API details.
