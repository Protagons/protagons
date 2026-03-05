# OpenClaw Examples

Deploy Protagon identities to OpenClaw workspaces.

OpenClaw is a personal AI assistant platform. Unlike hosted services where
your identity lives on someone else's infrastructure, OpenClaw runs locally
and your SOUL.md stays on your machine.

## Prerequisites

```bash
pip install protagons
```

## Examples

| File | Description |
|------|-------------|
| `deploy_to_workspace.py` | Deploy a local `.protagon.json` to an OpenClaw workspace |
| `generate_and_deploy.py` | Generate a new Protagon via API and deploy in one step |
| `SOUL.md.example` | Example output of a deployed SOUL.md file |

## Quick Start

```bash
python deploy_to_workspace.py path/to/character.protagon.json ~/openclaw
```
