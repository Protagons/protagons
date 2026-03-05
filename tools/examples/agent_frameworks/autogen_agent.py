"""
Use a Protagon as an AutoGen AssistantAgent.

Usage:
    pip install protagons pyautogen
    export OPENAI_API_KEY=sk-...
    python autogen_agent.py path/to/character.protagon.json
"""

import sys
from protagons import load
from protagons.integrations.agent_frameworks import to_autogen_agent


def main():
    if len(sys.argv) < 2:
        print("Usage: python autogen_agent.py <protagon_file>")
        sys.exit(1)

    protagon = load(sys.argv[1])
    print(f"Using Protagon: {protagon.name}")

    from autogen import UserProxyAgent

    llm_config = {
        "model": "gpt-4o",
        "temperature": 0.7,
    }

    assistant = to_autogen_agent(protagon.raw, llm_config=llm_config)

    user = UserProxyAgent(
        name="user",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=1,
    )

    user.initiate_chat(assistant, message="Introduce yourself in your unique voice.")


if __name__ == "__main__":
    main()
