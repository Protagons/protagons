"""
Compile a .protagon.json profile into an OpenClaw SOUL.md file.

Usage:
    python compile_soul_md.py <profile.protagon.json> [output_path]

If output_path is omitted, prints to stdout.
"""

import json
import sys
from pathlib import Path


def compile_soul_md(profile_path: str) -> str:
    with open(profile_path) as f:
        p = json.load(f)

    dims = p.get("dimensions", {})
    identity = dims.get("identity_construction", {})
    audience = dims.get("audience_relationship", {})
    formality = dims.get("formality_components", {})
    engagement = dims.get("engagement_devices", {})
    moral = dims.get("facet_28_moral_ethical_framework", {})
    worldview = dims.get("facet_27_worldview_deep_structure", {})
    epistemic = dims.get("modal_epistemic_stance", {})

    archetype = identity.get("character_archetype", {}).get("value", "unknown")
    confidence = identity.get("confidence_projection", {}).get("value", "unknown")
    keywords_val = identity.get("brand_voice_keywords", {}).get("value", [])
    keywords = ", ".join(keywords_val) if isinstance(keywords_val, list) else str(keywords_val)
    power = audience.get("power_dynamics", {}).get("value", "unspecified")
    intimacy = audience.get("intimacy_level", {}).get("value", "unspecified")
    register = formality.get("register_classification", {}).get("value", "unspecified")
    commitment = epistemic.get("commitment_level", {}).get("value", "unspecified")
    cta_intensity = engagement.get("cta_intensity", {}).get("value", "unspecified")
    moral_foundation = moral.get("primary_moral_foundation", {}).get("value", "unspecified")
    ethics = moral.get("moral_absolutism_relativism", {}).get("value", "unspecified")
    epistemology = worldview.get("epistemological_stance", {}).get("value", "unspecified")
    human_nature = worldview.get("human_nature_belief", {}).get("value", "unspecified")

    metadata = p.get("metadata", {})
    generated_at = metadata.get("generated_at", "unknown")[:10]

    soul = f"""# {p.get('name', 'Unnamed')} — SOUL.md
> {p.get('tagline', '')}
> Generated from Protagons profile · {generated_at}

## Identity

{p.get('description', '')}

Archetype: {archetype}. Confidence projection: {confidence}.
Core voice keywords: {keywords}.

## Communication Style

- Register: {register}
- Power dynamic with audience: {power}
- Intimacy level: {intimacy}
- Commitment level: {commitment}
- CTA approach: {cta_intensity}

{p.get('synthesized_prompt', {}).get('content', '')[:400]}...

## Values

- Primary moral foundation: {moral_foundation}
- Ethical stance: {ethics}
- Epistemological approach: {epistemology}
- View of human nature: {human_nature}

## Boundaries

"""
    # Extract DO/DON'T rules from synthesized_prompt
    prompt_content = p.get("synthesized_prompt", {}).get("content", "")
    if "DO " in prompt_content and "NEVER " in prompt_content:
        do_start = prompt_content.find("\nDO ")
        never_start = prompt_content.find("\nNEVER ")
        end = prompt_content.find("\n\nMaintain", never_start)
        if do_start > 0 and never_start > 0:
            soul += prompt_content[do_start:end if end > 0 else never_start + 500].strip()

    soul += f"""

## Example Responses

{p.get('writing_sample', '')}

---
*Compiled from Protagons schema v{p.get('spec_version', '1.0.0')} · {metadata.get('source', '')}*
*License: {metadata.get('license', 'CC-BY-4.0')}*
"""
    return soul


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <profile.protagon.json> [output_path]", file=sys.stderr)
        sys.exit(1)

    profile_path = sys.argv[1]
    result = compile_soul_md(profile_path)

    if len(sys.argv) >= 3:
        output_path = Path(sys.argv[2])
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(result, encoding="utf-8")
        print(f"Wrote SOUL.md to {output_path}")
    else:
        print(result)
