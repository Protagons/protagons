"""
Deploy a Protagon to an OpenClaw workspace.

Usage:
    pip install protagons
    python deploy_to_workspace.py path/to/character.protagon.json ~/openclaw
"""

import sys
from protagons import load
from protagons.integrations.openclaw import OpenClawIntegration


def main():
    if len(sys.argv) < 3:
        print("Usage: python deploy_to_workspace.py <protagon_file> <workspace_path>")
        sys.exit(1)

    protagon = load(sys.argv[1])
    workspace = sys.argv[2]

    print(f"Deploying: {protagon.name}")
    print(f"Workspace: {workspace}")

    oc = OpenClawIntegration(workspace_path=workspace)
    result = oc.deploy(protagon.raw)

    print(f"Deployed at: {result['deployed_at']}")
    print(f"SOUL.md written to: {result['workspace_path']}/SOUL.md")

    # Check status
    status = oc.status()
    print(f"Has SOUL.md: {status['has_soul_md']}")
    print(f"Has voice config: {status['has_voice_config']}")


if __name__ == "__main__":
    main()
