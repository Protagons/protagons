"""
Use a Protagon as a CrewAI agent backstory.

Usage:
    pip install protagons crewai
    export OPENAI_API_KEY=sk-...
    python crewai_agent.py path/to/character.protagon.json
"""

import sys
from protagons import load
from protagons.integrations.agent_frameworks import to_crewai_agent


def main():
    if len(sys.argv) < 2:
        print("Usage: python crewai_agent.py <protagon_file>")
        sys.exit(1)

    protagon = load(sys.argv[1])
    print(f"Using Protagon: {protagon.name}")

    from crewai import Task, Crew

    agent = to_crewai_agent(protagon.raw, goal="Write a short introduction.")

    task = Task(
        description="Write a brief introduction of yourself in your unique voice.",
        expected_output="A 2-3 paragraph introduction.",
        agent=agent,
    )

    crew = Crew(agents=[agent], tasks=[task], verbose=True)
    result = crew.kickoff()

    print(result)


if __name__ == "__main__":
    main()
