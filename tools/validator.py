"""
Validate .protagon.json files against the schema.
"""

import json
from pathlib import Path


# Required top-level fields
REQUIRED_FIELDS = ["name", "spec_version"]

# All 28 dimension keys
DIMENSION_KEYS = [
    "rhetorical_architecture", "modal_epistemic_stance", "metadiscourse",
    "audience_relationship", "genre_conventions", "cohesion_architecture",
    "evaluative_language", "identity_construction", "temporal_patterns",
    "visual_integration", "lexical_sophistication", "engagement_devices",
    "intertextuality", "information_architecture", "prosodic_features",
    "cultural_markers", "emotional_architecture", "formality_components",
    "psychological_trauma_markers", "neurological_cognitive_patterns",
    "mental_health_markers", "physical_health_state_markers",
    "age_developmental_markers", "personality_temperament_patterns",
    "facet_25_core_psychology", "facet_26_motivational_architecture",
    "facet_27_worldview_deep_structure", "facet_28_moral_ethical_framework",
]

VALID_CONTENT_TIERS = {"standard", "dark", "adversarial"}


def validate_dict(data: dict) -> dict:
    """
    Validate a Protagon dictionary against the schema.

    Returns:
        dict with keys: valid (bool), errors (list), warnings (list)
    """
    errors = []
    warnings = []

    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"Missing required field: {field}")

    # Check schema URL
    schema_url = data.get("$schema", "")
    if schema_url and "character.schema.json" not in schema_url and "protagon.schema.json" not in schema_url:
        warnings.append(f"Unexpected $schema URL: {schema_url}")

    # Check name and slug
    if "name" in data and not isinstance(data["name"], str):
        errors.append("'name' must be a string")
    if "slug" in data and not isinstance(data["slug"], str):
        errors.append("'slug' must be a string")

    # Check synthesized_prompt
    sp = data.get("synthesized_prompt")
    if sp:
        if not isinstance(sp, dict):
            errors.append("'synthesized_prompt' must be an object")
        elif not sp.get("content"):
            warnings.append("'synthesized_prompt.content' is empty")
    else:
        warnings.append("No synthesized_prompt — Protagon won't be directly usable as a system prompt")

    # Check dimensions
    dimensions = data.get("dimensions", {})
    if dimensions:
        found = set(dimensions.keys())
        missing = set(DIMENSION_KEYS) - found
        if missing:
            warnings.append(f"Missing {len(missing)}/28 dimensions: {', '.join(sorted(missing)[:5])}...")
    else:
        warnings.append("No dimensions found")

    # Check deployment
    deployment = data.get("deployment", {})
    if deployment:
        tier = deployment.get("content_tier", "standard")
        if tier not in VALID_CONTENT_TIERS:
            errors.append(f"Invalid content_tier: {tier}. Must be one of: {VALID_CONTENT_TIERS}")
    else:
        warnings.append("No deployment metadata")

    # Check personality
    personality = data.get("personality", {})
    if not personality:
        warnings.append("No personality axes")

    # Check integrations (optional, validate structure if present)
    integrations = data.get("integrations", {})
    if integrations and not isinstance(integrations, dict):
        errors.append("'integrations' must be an object")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
    }


def validate(path: str | Path) -> dict:
    """Validate a .protagon.json file from disk."""
    path = Path(path)
    with path.open() as f:
        data = json.load(f)
    return validate_dict(data)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <file.protagon.json>", file=sys.stderr)
        sys.exit(1)

    result = validate(sys.argv[1])

    if result["valid"]:
        print(f"VALID: {sys.argv[1]}")
    else:
        print(f"INVALID: {sys.argv[1]}")
        for err in result["errors"]:
            print(f"  ERROR: {err}")

    for warn in result["warnings"]:
        print(f"  WARNING: {warn}")

    sys.exit(0 if result["valid"] else 1)
