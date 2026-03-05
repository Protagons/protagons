"""
Deploy a Protagon as an ElevenLabs Conversational AI agent.

Usage:
    pip install protagons[voice]
    export ELEVENLABS_API_KEY=xi-...
    python elevenlabs_agent.py path/to/character.protagon.json
"""

import os
import sys
from protagons import load
from protagons.integrations.elevenlabs import ElevenLabsIntegration


def main():
    if len(sys.argv) < 2:
        print("Usage: python elevenlabs_agent.py <protagon_file>")
        sys.exit(1)

    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        print("Error: Set ELEVENLABS_API_KEY environment variable")
        sys.exit(1)

    protagon = load(sys.argv[1])
    print(f"Deploying: {protagon.name}")

    el = ElevenLabsIntegration(api_key=api_key)
    result = el.create_agent(protagon.raw)

    print(f"Agent created: {result['agent_id']}")
    print(f"Deployed at: {result['deployed_at']}")
    print(f"Dashboard: https://elevenlabs.io/app/conversational-ai")


if __name__ == "__main__":
    main()
