# Agent Framework Examples

Use Protagon identities with popular AI agent frameworks.

## Prerequisites

Install the framework you want to use:

```bash
pip install protagons
pip install langchain-core langchain-openai  # for LangChain
pip install crewai                           # for CrewAI
pip install pyautogen                        # for AutoGen
```

## Examples

| File | Framework | Description |
|------|-----------|-------------|
| `langchain_agent.py` | LangChain | System message in a chain |
| `crewai_agent.py` | CrewAI | Agent with Protagon backstory |
| `autogen_agent.py` | AutoGen | AssistantAgent with system message |

## Quick Start

```bash
export OPENAI_API_KEY=sk-...
python langchain_agent.py path/to/character.protagon.json
```
