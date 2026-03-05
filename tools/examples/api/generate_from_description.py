"""
Generate a Protagon from a description using the Protagons API.

The API uses BYOK (Bring Your Own Key) — you provide your Google API key,
which is sent directly to Google's Gemini API and never stored.

Usage:
    export PROTAGONS_API_KEY=pg-...
    export GOOGLE_API_KEY=AIza...
    python generate_from_description.py
"""

import json
import os
import time

import requests

API_BASE = "https://api.usaw.ai/api/v1"
PROTAGONS_KEY = os.environ.get("PROTAGONS_API_KEY", "")
GOOGLE_KEY = os.environ.get("GOOGLE_API_KEY", "")


def generate(name: str, description: str, model: str = "gemini-2.5-pro") -> dict:
    """Generate a Protagon and wait for completion."""
    # Start the generation job
    response = requests.post(
        f"{API_BASE}/generate",
        headers={"Authorization": f"Bearer {PROTAGONS_KEY}"},
        json={
            "name": name,
            "description": description,
            "google_api_key": GOOGLE_KEY,
            "model": model,
        },
    )
    response.raise_for_status()
    job = response.json()

    print(f"Job started: {job['job_id']}")
    print(f"Poll URL: {job['poll_url']}")

    # Poll for completion
    while True:
        status_response = requests.get(
            f"{API_BASE}/jobs/{job['job_id']}",
            headers={"Authorization": f"Bearer {PROTAGONS_KEY}"},
        )
        status = status_response.json()

        progress = status.get("progress", {})
        agents = progress.get("agents_completed", 0)
        total = progress.get("agents_total", 28)
        current = progress.get("current_agent", "")

        print(f"  [{agents}/{total}] {current}")

        if status["status"] == "completed":
            return status["result"]
        if status["status"] == "failed":
            raise Exception(f"Generation failed: {status.get('error', 'Unknown error')}")

        time.sleep(5)


def main():
    if not PROTAGONS_KEY or not GOOGLE_KEY:
        print("Set PROTAGONS_API_KEY and GOOGLE_API_KEY environment variables.")
        return

    protagon = generate(
        name="Dr. Eleanor Voss",
        description=(
            "A quantum physicist who explains complex theories through cooking metaphors. "
            "Warm, precise, occasionally sardonic. Writes with a blend of academic rigor "
            "and kitchen-table accessibility. Believes that if you can't explain it with "
            "a sourdough analogy, you don't truly understand it."
        ),
    )

    # Save the result
    slug = protagon.get("slug", "dr-eleanor-voss")
    filename = f"{slug}.protagon.json"
    with open(filename, "w") as f:
        json.dump(protagon, f, indent=2)

    print(f"\nSaved to {filename}")
    print(f"Name: {protagon.get('name')}")
    print(f"Dimensions: {len(protagon.get('dimensions', {}))}/28")
    print(f"Fields: {protagon.get('analysis', {}).get('total_fields', 'N/A')}")


if __name__ == "__main__":
    main()
