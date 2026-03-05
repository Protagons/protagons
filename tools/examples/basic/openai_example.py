"""
Use a Protagon with OpenAI's API.

Usage:
    pip install openai
    export OPENAI_API_KEY=sk-...
    python openai_example.py path/to/character.protagon.json
"""

import json
import sys
from openai import OpenAI


def main():
    if len(sys.argv) < 2:
        print("Usage: python openai_example.py <protagon_file> [prompt]")
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

    # Call OpenAI
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
