"""
Deploy a Protagon as a Vapi voice assistant.

Usage:
    pip install protagons[voice]
    export VAPI_API_KEY=...
    python vapi_assistant.py path/to/character.protagon.json
"""

import os
import sys
from protagons import load
from protagons.integrations.voice_platforms import VapiIntegration


def main():
    if len(sys.argv) < 2:
        print("Usage: python vapi_assistant.py <protagon_file>")
        sys.exit(1)

    api_key = os.environ.get("VAPI_API_KEY")
    if not api_key:
        print("Error: Set VAPI_API_KEY environment variable")
        sys.exit(1)

    protagon = load(sys.argv[1])
    print(f"Deploying: {protagon.name}")

    vapi = VapiIntegration(api_key=api_key)
    result = vapi.create_assistant(protagon.raw)

    print(f"Assistant created: {result['agent_id']}")
    print(f"Dashboard: https://dashboard.vapi.ai/assistants")


if __name__ == "__main__":
    main()
