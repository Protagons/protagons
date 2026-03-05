"""
Use a Protagon with Anthropic's API.

Usage:
    pip install anthropic
    export ANTHROPIC_API_KEY=sk-ant-...
    python anthropic_example.py path/to/character.protagon.json
"""

import json
import sys
import anthropic


def main():
    if len(sys.argv) < 2:
        print("Usage: python anthropic_example.py <protagon_file> [prompt]")
        sys.exit(1)

    protagon_path = sys.argv[1]
    user_prompt = sys.argv[2] if len(sys.argv) > 2 else "Introduce yourself and tell me about your perspective on the world."

    # Load the Protagon
    with open(protagon_path) as f:
        protagon = json.load(f)

    name = protagon.get("name", "Unknown")
    system_prompt = protagon.get("synthesized_prompt", {}).get("content", "")

    if not system_prompt:
        print(f"Error: No synthesized_prompt found in {protagon_path}")
        sys.exit(1)

    print(f"Using Protagon: {name}")
    print(f"Prompt: {user_prompt}")
    print("-" * 60)

    # Call Anthropic
    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )

    print(message.content[0].text)


if __name__ == "__main__":
    main()
