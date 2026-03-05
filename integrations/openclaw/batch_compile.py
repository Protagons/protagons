"""
Batch compile multiple .protagon.json profiles into SOUL.md files.

Usage:
    python batch_compile.py <profiles_dir> <output_dir>

Useful for multi-agent OpenClaw setups where each agent needs its own SOUL.md.
"""

import sys
from pathlib import Path
from compile_soul_md import compile_soul_md


def batch_compile(profiles_dir: str, output_dir: str) -> None:
    profiles_path = Path(profiles_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    profiles = list(profiles_path.glob("**/*.protagon.json"))

    if not profiles:
        print(f"No .protagon.json files found in {profiles_dir}", file=sys.stderr)
        sys.exit(1)

    for profile_file in profiles:
        try:
            soul_md = compile_soul_md(str(profile_file))
            out_file = output_path / f"{profile_file.stem.replace('.protagon', '')}-SOUL.md"
            out_file.write_text(soul_md, encoding="utf-8")
            print(f"  {profile_file.name} -> {out_file.name}")
        except Exception as e:
            print(f"  SKIP {profile_file.name}: {e}", file=sys.stderr)

    print(f"\nCompiled {len(profiles)} profiles to {output_dir}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <profiles_dir> <output_dir>", file=sys.stderr)
        sys.exit(1)

    batch_compile(sys.argv[1], sys.argv[2])
