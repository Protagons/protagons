"""
Use a Protagon as a LangChain system message.

Usage:
    pip install protagons langchain-core langchain-openai
    export OPENAI_API_KEY=sk-...
    python langchain_agent.py path/to/character.protagon.json [prompt]
"""

import sys
from protagons import load
from protagons.integrations.agent_frameworks import to_langchain_system_message


def main():
    if len(sys.argv) < 2:
        print("Usage: python langchain_agent.py <protagon_file> [prompt]")
        sys.exit(1)

    protagon = load(sys.argv[1])
    user_prompt = sys.argv[2] if len(sys.argv) > 2 else "Introduce yourself."

    print(f"Using Protagon: {protagon.name}")

    from langchain_core.messages import HumanMessage
    from langchain_openai import ChatOpenAI

    system_msg = to_langchain_system_message(protagon.raw)
    llm = ChatOpenAI(model="gpt-4o")
    response = llm.invoke([system_msg, HumanMessage(content=user_prompt)])

    print(response.content)


if __name__ == "__main__":
    main()
