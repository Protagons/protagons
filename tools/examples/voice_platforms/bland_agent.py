"""
Deploy a Protagon as a Bland AI phone agent.

Usage:
    pip install protagons[voice]
    export BLAND_API_KEY=sk-...
    python bland_agent.py path/to/character.protagon.json
"""

import os
import sys
from protagons import load
from protagons.integrations.voice_platforms import BlandAIIntegration


def main():
    if len(sys.argv) < 2:
        print("Usage: python bland_agent.py <protagon_file>")
        sys.exit(1)

    api_key = os.environ.get("BLAND_API_KEY")
    if not api_key:
        print("Error: Set BLAND_API_KEY environment variable")
        sys.exit(1)

    protagon = load(sys.argv[1])
    print(f"Deploying: {protagon.name}")

    bland = BlandAIIntegration(api_key=api_key)
    result = bland.create_agent(protagon.raw, voice="maya")

    print(f"Agent created: {result['agent_id']}")
    print(f"Dashboard: https://app.bland.ai/agents")


if __name__ == "__main__":
    main()
