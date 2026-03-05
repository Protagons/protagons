"""
Deploy a Protagon as an OpenAI Assistant.

Usage:
    pip install protagons[openai]
    export OPENAI_API_KEY=sk-...
    python assistant_setup.py path/to/character.protagon.json
"""

import os
import sys
from protagons import load
from protagons.integrations.openai_assistants import OpenAIAssistantIntegration


def main():
    if len(sys.argv) < 2:
        print("Usage: python assistant_setup.py <protagon_file>")
        sys.exit(1)

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: Set OPENAI_API_KEY environment variable")
        sys.exit(1)

    protagon = load(sys.argv[1])
    print(f"Deploying: {protagon.name}")

    oai = OpenAIAssistantIntegration(api_key=api_key)
    result = oai.create_assistant(protagon.raw, model="gpt-4o")

    print(f"Assistant created: {result['assistant_id']}")
    print(f"Deployed at: {result['deployed_at']}")
    print(f"Dashboard: https://platform.openai.com/assistants")


if __name__ == "__main__":
    main()
