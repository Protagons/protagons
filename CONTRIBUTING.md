# Contributing to Protagons

Thank you for your interest in contributing to the Protagons open standard.

## Ways to Contribute

### Add a Profile

Submit a new `.protagon.json` file to the appropriate directory under `/profiles/`:

- `profiles/archetypes/` — Jungian, Myers-Briggs, Enneagram characters
- `profiles/professional/` — Business, tech, creative roles
- `profiles/adversarial/` — Dark, antagonist, trickster characters
- `profiles/brand/` — Brand voice examples

**Requirements:**
- Must validate against `schema/character.schema.json`
- Must include at least `name`, `spec_version`, `synthesized_prompt`, and `dimensions`
- Dimensions should include confidence scores and evidence where possible
- Include a `writing_sample` demonstrating the voice
- Set appropriate `deployment.content_tier` (`standard`, `dark`, or `adversarial`)

Run the validator before submitting:
```bash
python tools/validator.py your-profile.protagon.json
```

### Propose Schema Changes

1. Open an issue with the `schema` label
2. Describe the proposed change and rationale
3. Breaking changes require a formal RFC process
4. Additive (new optional fields) changes can go through standard PR review

### Fix a Profile

If a dimension value seems wrong or a confidence score is off:

1. Fork the repo
2. Make your correction with evidence
3. Submit a PR explaining the change and why the current value is incorrect

### Add Integration Examples

New platform integration examples are welcome in `/tools/examples/` or `/integrations/`. Include:

- Working code with comments
- A README explaining the integration
- Any required configuration

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b add-profile-name`)
3. Make your changes
4. Run `python tools/validator.py` on any new profiles
5. Submit a PR with a clear description

## Code of Conduct

Be respectful. Profiles representing dark or adversarial characters are welcome for creative fiction — but contributions should not target real individuals or promote harm outside of clearly fictional contexts.

## License

By contributing, you agree that:
- Schema and tooling contributions are MIT licensed
- Profile contributions are CC-BY-4.0 licensed
