# Protagons Skill for OpenClaw

You have access to the Protagons library — a collection of portable AI character identities.

## What you can do

- **List** available Protagons from the public library
- **Get** a specific Protagon by slug (returns full `.protagon.json`)
- **Deploy** a Protagon to your workspace as a SOUL.md personality file
- **Check status** of a deployed Protagon
- **Generate** a new Protagon from a description (requires a Google API key)

## How Protagons work

A Protagon is a portable AI identity file (`.protagon.json`) containing:
- A synthesized system prompt distilled from 28 linguistic/psychological dimensions
- Personality axes (formal/casual, analytical/emotional, etc.)
- Voice configuration (ElevenLabs TTS settings)
- Deployment metadata (content tier, safety requirements)

When you deploy a Protagon, it becomes your SOUL.md — shaping how you communicate.

## Tool usage

Use `protagons_list` to browse available characters.
Use `protagons_get` with a slug to fetch the full identity.
Use `protagons_deploy` to write a SOUL.md to your workspace.
Use `protagons_status` to check what's currently deployed.
Use `protagons_generate` to create a new character from a description.

## Content tiers

- **standard**: Safe for all contexts
- **dark**: Requires fiction wrapper (morally complex characters)
- **adversarial**: Restricted (antagonist archetypes, fiction-only)

Always respect content tier requirements when deploying.
