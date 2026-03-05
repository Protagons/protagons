"""
Compile a .protagon.json profile into a system prompt.

Usage:
    python compiler.py <profile.protagon.json>

Loads the profile and prints the synthesized_prompt content,
ready to be used as a system prompt for any LLM.
"""

import json
import sys


def compile_prompt(profile_path: str) -> str:
    with open(profile_path) as f:
        profile = json.load(f)

    prompt = profile.get("synthesized_prompt", {}).get("content")
    if not prompt:
        print("Warning: No synthesized_prompt.content found in profile.", file=sys.stderr)
        return ""

    return prompt


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <profile.protagon.json>", file=sys.stderr)
        sys.exit(1)

    result = compile_prompt(sys.argv[1])
    if result:
        print(result)
