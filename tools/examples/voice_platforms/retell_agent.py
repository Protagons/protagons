"""
Deploy a Protagon as a Retell voice agent.

Note: Retell requires an llm_id created in the Retell dashboard.

Usage:
    pip install protagons[voice]
    export RETELL_API_KEY=...
    python retell_agent.py path/to/character.protagon.json llm_xxx
"""

import os
import sys
from protagons import load
from protagons.integrations.voice_platforms import RetellIntegration


def main():
    if len(sys.argv) < 3:
        print("Usage: python retell_agent.py <protagon_file> <llm_id>")
        sys.exit(1)

    api_key = os.environ.get("RETELL_API_KEY")
    if not api_key:
        print("Error: Set RETELL_API_KEY environment variable")
        sys.exit(1)

    protagon = load(sys.argv[1])
    llm_id = sys.argv[2]
    print(f"Deploying: {protagon.name} with LLM {llm_id}")

    retell = RetellIntegration(api_key=api_key)
    result = retell.create_agent(protagon.raw, llm_id=llm_id)

    print(f"Agent created: {result['agent_id']}")
    print(f"Dashboard: https://app.retellai.com/agents")


if __name__ == "__main__":
    main()
