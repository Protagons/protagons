# Integrations Guide

Deploy Protagon identities to third-party platforms using the Python SDK, REST API, or one-click deploy from the library UI.

## Installation

```bash
# Core (load + validate only)
pip install protagons

# With voice platform support
pip install protagons[voice]

# With OpenAI Assistants
pip install protagons[openai]

# With Anthropic
pip install protagons[anthropic]

# Everything
pip install protagons[all]
```

## Voice AI Platforms

### ElevenLabs

Deploy as a Conversational AI agent with voice synthesis.

```python
from protagons import load
from protagons.integrations.elevenlabs import ElevenLabsIntegration

protagon = load("character.protagon.json")
el = ElevenLabsIntegration(api_key="xi-your-key")

# Create a Conversational AI agent
result = el.create_agent(protagon.raw)
print(result["agent_id"])

# Generate a voice from the protagon's voice_prompt
voice = el.create_voice(protagon.raw)

# Update an existing agent
el.update_agent(result["agent_id"], protagon.raw)
```

### Bland AI

Deploy as a phone call agent.

```python
from protagons.integrations.voice_platforms import BlandAIIntegration

bland = BlandAIIntegration(api_key="sk-your-key")
result = bland.create_agent(protagon.raw, voice="maya")
```

### Vapi

Deploy as a voice assistant with multi-provider support.

```python
from protagons.integrations.voice_platforms import VapiIntegration

vapi = VapiIntegration(api_key="your-vapi-key")
result = vapi.create_assistant(
    protagon.raw,
    model_provider="openai",
    model="gpt-4o",
    voice_provider="11labs",
)
```

### Retell

Deploy as a voice agent. Requires an `llm_id` created in the Retell dashboard.

```python
from protagons.integrations.voice_platforms import RetellIntegration

retell = RetellIntegration(api_key="your-retell-key")
result = retell.create_agent(protagon.raw, llm_id="llm_xxx")
```

## LLM APIs

### OpenAI Assistants

Deploy as an OpenAI Assistant with the Protagon as instructions.

```python
from protagons.integrations.openai_assistants import OpenAIAssistantIntegration

oai = OpenAIAssistantIntegration(api_key="sk-your-key")
result = oai.create_assistant(protagon.raw, model="gpt-4o")
print(result["assistant_id"])

# Update instructions on an existing assistant
oai.update_assistant(result["assistant_id"], updated_protagon)
```

### Anthropic

Fiction wrapper for dark/adversarial content tiers + direct message creation.

```python
from protagons.integrations.anthropic import create_fiction_wrapper, create_message

# Wrap dark content in fiction framing
prompt = create_fiction_wrapper(dark_protagon)

# Send a message using the Protagon
response = create_message(protagon.raw, "Introduce yourself.")
print(response.content[0].text)
```

## Agent Frameworks

### LangChain

```python
from protagons.integrations.agent_frameworks import to_langchain_system_message
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

msg = to_langchain_system_message(protagon.raw)
llm = ChatOpenAI(model="gpt-4o")
response = llm.invoke([msg, HumanMessage(content="Hello")])
```

### CrewAI

```python
from protagons.integrations.agent_frameworks import to_crewai_agent

agent = to_crewai_agent(protagon.raw, goal="Write a report")
```

### AutoGen

```python
from protagons.integrations.agent_frameworks import to_autogen_agent

agent = to_autogen_agent(protagon.raw, llm_config={"model": "gpt-4o"})
```

## Personal Assistants

### OpenClaw

Deploy as a SOUL.md personality file in an OpenClaw workspace.

```python
from protagons.integrations.openclaw import OpenClawIntegration

oc = OpenClawIntegration(workspace_path="~/openclaw")
result = oc.deploy(protagon.raw)
status = oc.status()
oc.reset()  # Remove deployed files
```

## REST API

### POST /api/v1/deploy

Unified deploy endpoint. Requires a Protagons API key (`pg-...`).

```bash
curl -X POST https://api.usaw.ai/api/v1/deploy \
  -H "Authorization: Bearer pg-your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "protagon_slug": "software-developer",
    "platform": "elevenlabs",
    "api_key": "xi-your-platform-key",
    "options": {}
  }'
```

Platform-specific endpoints are also available:

- `POST /api/v1/deploy/elevenlabs`
- `POST /api/v1/deploy/openai-assistant`
- `POST /api/v1/deploy/bland`
- `POST /api/v1/deploy/vapi`
- `POST /api/v1/deploy/retell`

### Response

```json
{
  "platform": "elevenlabs",
  "agent_id": "agent_xxx",
  "protagon": "software-developer",
  "deployed_at": "2026-02-24T12:00:00.000Z",
  "deployed_prompt_hash": "sha256..."
}
```

## Security

- Platform API keys are used once per request and **never stored or logged**
- All outbound calls use HTTPS with 30-second timeouts
- Error messages are scrubbed of potential API key fragments
- The `integrations` field in `.protagon.json` records deployment state without storing credentials
