"""
Generate a Protagon from writing samples using the Protagons API.

Extracts a voice identity from existing text — useful for replicating
a specific writer's style, tone, and linguistic patterns.

Usage:
    export PROTAGONS_API_KEY=pg-...
    export GOOGLE_API_KEY=AIza...
    python generate_from_text.py sample1.txt sample2.txt
"""

import json
import os
import sys
import time

import requests

API_BASE = "https://api.usaw.ai/api/v1"
PROTAGONS_KEY = os.environ.get("PROTAGONS_API_KEY", "")
GOOGLE_KEY = os.environ.get("GOOGLE_API_KEY", "")


def generate_from_text(name: str, writing_samples: list[str]) -> dict:
    """Generate a Protagon from writing samples and wait for completion."""
    response = requests.post(
        f"{API_BASE}/generate/from-text",
        headers={"Authorization": f"Bearer {PROTAGONS_KEY}"},
        json={
            "name": name,
            "writing_samples": writing_samples,
            "google_api_key": GOOGLE_KEY,
        },
    )
    response.raise_for_status()
    job = response.json()

    print(f"Job started: {job['job_id']}")
    print(f"Analyzing {len(writing_samples)} sample(s)...")

    while True:
        status = requests.get(
            f"{API_BASE}/jobs/{job['job_id']}",
            headers={"Authorization": f"Bearer {PROTAGONS_KEY}"},
        ).json()

        progress = status.get("progress", {})
        agents = progress.get("agents_completed", 0)
        total = progress.get("agents_total", 28)

        print(f"  [{agents}/{total}] {progress.get('current_agent', '')}")

        if status["status"] == "completed":
            return status["result"]
        if status["status"] == "failed":
            raise Exception(f"Analysis failed: {status.get('error')}")

        time.sleep(5)


def main():
    if not PROTAGONS_KEY or not GOOGLE_KEY:
        print("Set PROTAGONS_API_KEY and GOOGLE_API_KEY environment variables.")
        return

    if len(sys.argv) < 2:
        print("Usage: python generate_from_text.py <file1.txt> [file2.txt] ...")
        print("\nProvide one or more text files containing writing samples.")
        return

    # Read writing samples from files
    samples = []
    for filepath in sys.argv[1:]:
        with open(filepath) as f:
            samples.append(f.read())

    total_words = sum(len(s.split()) for s in samples)
    print(f"Loaded {len(samples)} sample(s), {total_words} words total")

    if total_words < 100:
        print("Error: Need at least 100 words total for quality extraction.")
        return

    protagon = generate_from_text(
        name=os.path.splitext(os.path.basename(sys.argv[1]))[0].replace("-", " ").title(),
        writing_samples=samples,
    )

    slug = protagon.get("slug", "analyzed-voice")
    filename = f"{slug}.protagon.json"
    with open(filename, "w") as f:
        json.dump(protagon, f, indent=2)

    print(f"\nSaved to {filename}")
    print(f"Name: {protagon.get('name')}")
    print(f"Completeness: {protagon.get('analysis', {}).get('completeness_score', 'N/A')}%")


if __name__ == "__main__":
    main()
