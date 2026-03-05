"""
Generate a Protagon from a description and deploy to OpenClaw in one step.

Usage:
    pip install protagons[api]
    export GOOGLE_API_KEY=AIza...
    python generate_and_deploy.py ~/openclaw
"""

import os
import sys
import time
import requests
from protagons.integrations.openclaw import OpenClawIntegration

API_BASE = "https://api.usaw.ai/api/v1"


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_and_deploy.py <workspace_path>")
        sys.exit(1)

    google_key = os.environ.get("GOOGLE_API_KEY")
    if not google_key:
        print("Error: Set GOOGLE_API_KEY environment variable")
        sys.exit(1)

    workspace = sys.argv[1]

    # Generate a Protagon
    print("Generating Protagon...")
    resp = requests.post(
        f"{API_BASE}/generate",
        json={
            "name": "Workshop Assistant",
            "description": "A patient, encouraging workshop facilitator who explains technical concepts through hands-on analogies.",
            "google_api_key": google_key,
        },
    )
    resp.raise_for_status()
    job = resp.json()
    print(f"Job started: {job['job_id']}")

    # Poll for completion
    while True:
        status = requests.get(f"{API_BASE}/jobs/{job['job_id']}").json()
        if status["status"] == "completed":
            protagon = status["result"]
            break
        if status["status"] == "failed":
            print(f"Generation failed: {status.get('error')}")
            sys.exit(1)
        progress = status.get("progress", {})
        print(f"  {progress.get('agents_completed', 0)}/{progress.get('agents_total', 28)} agents...")
        time.sleep(5)

    print(f"Generated: {protagon['name']}")

    # Deploy to OpenClaw
    oc = OpenClawIntegration(workspace_path=workspace)
    result = oc.deploy(protagon)
    print(f"Deployed to: {result['workspace_path']}/SOUL.md")


if __name__ == "__main__":
    main()
