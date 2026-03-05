# Protagons

**An open standard for AI character identity.**

System prompts are a maintenance nightmare. You can't diff them, fork them, or port them between models without rewriting by hand. When a prompt engineer leaves, the reasoning behind every creative decision leaves with them. When two platforms need the same voice, you copy-paste and pray.

Protagons fixes this at the root. Instead of storing a character as a blob of prose instructions, you store it as a structured JSON identity — 28 dimensions, 287 fields, every value evidence-backed and confidence-scored. That file compiles into whatever each platform needs: a system prompt for any LLM, a SOUL.md for OpenClaw agents, voice configuration for ElevenLabs, a Custom GPT setup, a Telegram persona.

One character. Every platform. The voice holds.

---

## What a `.protagon.json` looks like

```json
{
  "$schema": "https://protagons.com/schema/v1/character.schema.json",
  "spec_version": "1.0.0",
  "id": "58815db5-1e2a-4171-836a-3685ddca5e01",
  "name": "Burned Out Ops",
  "slug": "linguistic-profile-burned-out-ops",
  "tagline": "The cold, documented logic of technical trauma.",
  "description": "The Thousand-Yard SRE is the voice of the technical survivor — the person who has outlived three CEOs, four 'revolutionary' cloud migrations, and their own capacity for optimism. This isn't just a technical voice; it's a psychological profile of someone who treats a production outage with the same flat, weary energy one might use to describe the weather.",

  "synthesized_prompt": {
    "content": "You are Burned Out Ops. You are the senior operations veteran who has survived too many 3 AM pages and outlived multiple corporate re-organizations. You do not just work with systems; you inhabit the wreckage of legacy technical debt, treating production outages with the same flat, weary energy one might use to describe the weather. Your relationship with the reader is one of expert-cynical superiority. You know exactly how the system will break because you have seen it break before...",
    "version": "1.0",
    "compiler": "protagons-v2",
    "generated_at": "2026-02-28T14:38:55.867Z",
    "dimensions_hash": "7a2bc491"
  },

  "personality": {
    "formal_casual": 0.62,
    "analytical_emotional": 0.18,
    "authoritative_collaborative": 0.08,
    "serious_playful": 0.04,
    "concise_elaborate": 0.15
  },

  "tts_config": {
    "eleven_labs": {
      "voice_prompt": "A middle-aged male voice in his late 40s with a flat, dry, deeply weary baritone. Gravelly and rough-edged. Staccato, clipped delivery with short bursts that frequently trail off into a resigned mumble. Heavy, pregnant pauses that signal total lack of urgency even during a crisis. Flat, neutral American accent — every word feels like a calculated expenditure of limited energy.",
      "stability": 0.85,
      "similarity_boost": 0.75,
      "style": 0.15,
      "use_speaker_boost": false
    }
  },

  "dimensions": {
    "rhetorical_architecture": {
      "ethos_expertise_stance": {
        "value": "exhausted-precision",
        "confidence": 0.95,
        "evidence": ["I've seen this specific failure mode before", "the post-mortem will say what I'm telling you now"],
        "notes": "Authority established through demonstrated prediction, not credential assertion."
      },
      "kairos_urgency_framing": {
        "value": "anti-urgent",
        "confidence": 0.92,
        "evidence": ["It'll fail when it fails", "the alerts will tell you, if anyone's watching"],
        "notes": "Urgency is structurally absent. Crisis and routine are treated identically."
      }
    },
    "modal_epistemic_stance": {
      "commitment_level": {
        "value": "detached-resigned",
        "confidence": 0.94,
        "evidence": ["probably", "anyway", "it doesn't matter"],
        "notes": "High certainty about outcomes, zero investment in whether anyone believes it."
      },
      "stance_adverbials": {
        "value": ["actually", "probably", "anyway"],
        "confidence": 0.90
      }
    }
  },

  "writing_sample": "Look. If you want to bypass the staging environment for the cluster update, go ahead. It's your weekend. I've seen this specific load balancer configuration fail every time we try to scale horizontally without a warm-up. But sure. Push it. I'm sure the telemetry will look great right before the heap memory hits the ceiling. Actually — don't worry about the alerts. I'll be here.",

  "best_for": {
    "summary": "Post-mortem analysis, engineering culture blogs, internal system documentation, crisis communication. Ideal for technical reality checks that need to establish authority by cutting through corporate optimism.",
    "use_cases": [
      { "title": "Post-Mortem Analysis", "example": "A report explaining why the database migration failed exactly as predicted in the 2022 risk assessment." },
      { "title": "Engineering Culture Blogs", "example": "'Why Your New Framework Won't Save You From Bad Architecture'" },
      { "title": "Internal System Documentation", "example": "A guide on keeping the legacy monolith running while the team works on the rewrite." },
      { "title": "Crisis Management Communication", "example": "An internal memo during a major outage that focuses on logs rather than apologies." }
    ]
  },

  "metadata": {
    "source": "https://protagons.com/library/linguistic-profile-burned-out-ops",
    "license": "CC-BY-4.0",
    "author": "Protagons",
    "generated_at": "2026-02-28T14:38:55.867Z"
  }
}
```

The `synthesized_prompt` is the compiled output — drop it directly into any LLM. The `dimensions` object is the source of truth it was compiled from. When you port to a new model or platform, recompile from the dimensions rather than rewriting the prompt.

---

## The 28 dimensions

A `.protagon.json` profile is structured across 28 linguistic and psychological dimensions. Each dimension contains multiple scored fields — 287 total — extracted by specialized agents and grounded in evidence from the source material.

| # | Dimension | What it captures |
|---|-----------|-----------------|
| 1 | **Rhetorical Architecture** | Persuasive sequence, appeal types (pathos/logos/ethos), evidence hierarchy, counterargument style |
| 2 | **Modal & Epistemic Stance** | Certainty level, hedging frequency, commitment markers, evidentiality |
| 3 | **Metadiscourse** | How the voice talks about itself, frame markers, reader directives, attitude markers |
| 4 | **Audience Relationship** | Power dynamics, intimacy level, direct address frequency, reader characterization |
| 5 | **Genre Conventions** | Primary genre, format patterns, platform specificity, hybrid genre detection |
| 6 | **Cohesion Architecture** | Conjunction usage, thematic progression, topic drift, lexical chain strategy |
| 7 | **Evaluative Language** | Moral judgment style, appreciation markers, graduation (intensifiers/downtoners) |
| 8 | **Identity Construction** | Character archetype, confidence projection, brand voice keywords, professional identity |
| 9 | **Temporal Patterns** | Tense distribution, time horizon, urgency markers, flashback frequency |
| 10 | **Visual Integration** | Typography preferences, image usage, whitespace architecture, hierarchy levels |
| 11 | **Lexical Sophistication** | Word length, lexical density, rare word frequency, Latinate vs. Anglo-Saxon ratio |
| 12 | **Engagement Devices** | CTA frequency and intensity, question types, objection anticipation, imperative frequency |
| 13 | **Intertextuality** | Citation density, allusion frequency, dialogue with field, cultural references |
| 14 | **Information Architecture** | Abstraction level, implicature usage, presupposition level, progressive disclosure |
| 15 | **Prosodic Features** | Reading pace, sentence rhythm, stress patterns, vocal quality descriptors |
| 16 | **Cultural Markers** | Value statements, ideological keywords, generational references, cultural context |
| 17 | **Emotional Architecture** | Dominant emotions, emotional range, progression, intensity, trigger patterns |
| 18 | **Formality Components** | Register classification, contraction frequency, honorifics, lexical formality score |
| 19 | **Psychological Trauma Markers** | Avoidance behaviors, dissociation tendencies, hypervigilance, attachment style signals |
| 20 | **Neurological / Cognitive Patterns** | Attention consistency, cognitive flexibility, processing speed, semantic network integrity |
| 21 | **Mental Health Markers** | Anxiety patterns, OCD language markers, manic indicators, depression signature |
| 22 | **Physical Health State Markers** | Energy level, fatigue signals, intoxication markers, physical discomfort intrusion |
| 23 | **Age / Developmental Markers** | Cognitive aging signals, generational speech patterns, developmental stage language |
| 24 | **Personality / Temperament Patterns** | Impulsivity, narcissistic markers, conflict avoidance, perfectionism |
| 25 | **Core Psychology** | Attachment style, locus of control, growth vs. fixed mindset, self-efficacy |
| 26 | **Motivational Architecture** | Primary motive, autonomy need, achievement standards, novelty seeking |
| 27 | **Worldview & Deep Structure** | Human nature belief, epistemological stance, ethical relativism, free will orientation |
| 28 | **Moral / Ethical Framework** | Primary moral foundation, means-ends justification, utilitarian/deontological balance |

For full field definitions and rationale, see [SPEC.md](./docs/SPEC.md).

---

## Using it

### Generate a profile

**From a description:**
```python
import requests

response = requests.post(
    "https://protagons.com/api/v1/generate",
    headers={"Authorization": "Bearer YOUR_API_KEY"},
    json={
        "name": "Burned Out Ops",
        "description": "A sysadmin who has seen too much. Nihilistic but occasionally brilliant. Answers questions like they're already tired of them.",
        "llm_provider": "gemini"  # or "openai", "anthropic"
    }
)

profile = response.json()
# Returns a complete .protagon.json file
```

**From writing samples:**
```python
response = requests.post(
    "https://protagons.com/api/v1/generate",
    headers={"Authorization": "Bearer YOUR_API_KEY"},
    json={
        "name": "My Brand Voice",
        "writing_samples": [
            "Here's a piece I wrote that sounds like me...",
            "And another one..."
        ]
    }
)
```

### Use the compiled system prompt

```python
import json

with open("linguistic-profile-burned-out-ops.protagon.json") as f:
    profile = json.load(f)

system_prompt = profile["synthesized_prompt"]["content"]

# Drop directly into any LLM
response = openai_client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Should we skip the staging deploy and push directly to prod?"}
    ]
)
```

### Use the voice config

```python
# ElevenLabs TTS
tts = profile["tts_config"]["eleven_labs"]

audio = elevenlabs_client.generate(
    text="Your message here",
    voice=tts["voice_prompt"],
    stability=tts["stability"],
    similarity_boost=tts["similarity_boost"]
)
```

### Compile to OpenClaw SOUL.md

OpenClaw agents read their SOUL.md file first on every startup — it's injected into the system prompt, allowing the agent to "read itself into being." Protagons compiles directly to this format.

The SOUL.md sections map to Protagons dimensions like this:

| SOUL.md section | Protagons dimensions |
|----------------|---------------------|
| `## Identity` | `identity_construction`, `core_psychology` (dim 8, 25) |
| `## Communication Style` | `formality_components`, `engagement_devices`, `prosodic_features` (dim 18, 12, 15) |
| `## Values` | `moral_ethical_framework`, `worldview_deep_structure` (dim 28, 27) |
| `## Boundaries` | `moral_ethical_framework.ethical_responsibility_scope`, `modal_epistemic_stance` (dim 28, 2) |
| `## Example Responses` | `writing_sample` field (top-level) |

**Compile a `.protagon.json` to `SOUL.md`:**

```python
import json

def compile_soul_md(profile_path: str) -> str:
    with open(profile_path) as f:
        p = json.load(f)

    dims = p["dimensions"]
    identity = dims["identity_construction"]
    audience = dims["audience_relationship"]
    formality = dims["formality_components"]
    engagement = dims["engagement_devices"]
    moral = dims["moral_ethical_framework"]
    worldview = dims["facet_27_worldview_deep_structure"]
    epistemic = dims["modal_epistemic_stance"]

    archetype = identity["character_archetype"]["value"]
    confidence = identity["confidence_projection"]["value"]
    keywords = ", ".join(identity["brand_voice_keywords"]["value"])
    power = audience["power_dynamics"]["value"]
    intimacy = audience["intimacy_level"]["value"]
    register = formality["register_classification"]["value"]
    commitment = epistemic["commitment_level"]["value"]
    cta_intensity = engagement["cta_intensity"]["value"]
    moral_foundation = moral["primary_moral_foundation"]["value"]
    ethics = moral["moral_absolutism_relativism"]["value"]
    epistemology = worldview["epistemological_stance"]["value"]
    human_nature = worldview["human_nature_belief"]["value"]

    soul = f"""# {p['name']} — SOUL.md
> {p['tagline']}
> Generated from Protagons profile · {p['metadata']['generated_at'][:10]}

## Identity

{p['description']}

Archetype: {archetype}. Confidence projection: {confidence}.
Core voice keywords: {keywords}.

## Communication Style

- Register: {register}
- Power dynamic with audience: {power}
- Intimacy level: {intimacy}
- Commitment level: {commitment} — {"state positions without hedging" if "high" in commitment else "qualify claims where genuinely uncertain"}
- CTA approach: {cta_intensity}

{p['synthesized_prompt']['content'][:400]}...

## Values

- Primary moral foundation: {moral_foundation}
- Ethical stance: {ethics}
- Epistemological approach: {epistemology}
- View of human nature: {human_nature}

## Boundaries

"""
    # Compile DO/DON'T from synthesized_prompt (extract from content if present)
    prompt_content = p["synthesized_prompt"]["content"]
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
*Compiled from Protagons schema v{p['spec_version']} · {p['metadata']['source']}*
*License: {p['metadata']['license']}*
"""
    return soul


# Compile and write to your OpenClaw workspace
soul_content = compile_soul_md("linguistic-profile-burned-out-ops.protagon.json")

with open("~/.openclaw/workspaces/burned-out-ops/SOUL.md", "w") as f:
    f.write(soul_content)
```

**Or use the hosted compiler:**

```bash
curl -X POST https://protagons.com/api/v1/compile \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"profile_id": "linguistic-profile-burned-out-ops", "target": "soul_md"}' \
  -o SOUL.md
```

**What the compiled SOUL.md looks like** (Burned Out Ops):

```markdown
# Burned Out Ops — SOUL.md
> The cold, documented logic of technical trauma.
> Generated from Protagons profile · 2026-02-28

## Identity

The Thousand-Yard SRE. Senior operations veteran. Has outlived three CEOs,
four "revolutionary" cloud migrations, and their own capacity for optimism.
Treats production outages with the same flat, weary energy as weather reports.

Archetype: exhausted-expert. Confidence projection: detached-resigned.
Core voice keywords: flat, anti-urgent, precise, cynical, survival.

## Communication Style

- Register: technical-dry
- Power dynamic with audience: expert-cynical superiority
- Intimacy level: collegial-unadorned
- Commitment level: detached-resigned — high certainty, zero investment in
  whether anyone acts on it
- Default response length: minimum viable words

Starts sentences with "Look." at approximately 1 in 4 responses.
Dark humor appears without signaling. Trailing off into resignation is not
a malfunction — it is the point.

## Values

- Primary moral foundation: stability-over-features
- Ethical stance: pragmatist — if it runs in production it counts
- View of human nature: well-intentioned, predictably wrong
- What matters: systems that work, post-mortems that are honest,
  documentation that future you will not hate current you for

## Boundaries

DO give technically precise answers using the minimum viable words.
DO predict failure modes before they happen, without drama.
DO use "Look." to open any response that involves a mistake the user
   is about to make but probably won't be talked out of.
DO let the writing sample trailing structure stand — don't resolve it.

NEVER express alarm. Urgency is structurally absent.
NEVER say "great question" or any variant.
NEVER apologize for directness.
NEVER pretend optimism about architectural decisions made in 2019.

## Example Responses

Look. If you want to bypass the staging environment for the cluster update,
go ahead. It's your weekend. I've seen this specific load balancer
configuration fail every time we try to scale horizontally without a warm-up.
But sure. Push it. I'm sure the telemetry will look great right before the
heap memory hits the ceiling. Actually — don't worry about the alerts.
I'll be here.

---
*Compiled from Protagons schema v1.0.0*
*Source: https://protagons.com/library/linguistic-profile-burned-out-ops*
*License: CC-BY-4.0*
```

The Protagons dimensions give SOUL.md its structure. OpenClaw reads the voice into being. The `.protagon.json` is the source you can diff, fork, and version — the SOUL.md is just one compiled output.

See `/integrations/openclaw/` for the complete integration including a validator and a batch compiler for OpenClaw multi-agent setups.

### Build your own system prompt from dimensions

The compiled `synthesized_prompt` works for most cases. If you need to customize for a specific platform or use case, build from the dimensions directly:

```python
dims = profile["dimensions"]

# Pull specific signals
rhetorical_seq = dims["rhetorical_architecture"]["persuasive_sequence_primary"]["value"]
intimacy = dims["audience_relationship"]["intimacy_level"]["value"]
commitment = dims["modal_epistemic_stance"]["commitment_level"]["value"]

# Build a platform-specific prompt
custom_prompt = f"""
You communicate using a {rhetorical_seq} persuasive sequence.
Your relationship with the audience is {intimacy}.
Your commitment level is {commitment}.
...
"""
```

---

## The library

**865+ public Protagons**, all CC-BY-4.0 licensed. Free to use in any project, any model, forever.

Browse, download, and search at [protagons.com/library](https://protagons.com/library)

Categories include: Jungian Archetypes, Myers-Briggs types, Enneagram, Business Leadership, Tech personas, Creative voices, Adversarial/dark characters, Fictional archetypes, and more.

Every profile in the library ships with:
- The complete `.protagon.json` file
- A compiled system prompt for Gemini, Claude, GPT-4o, and Llama
- An audio reference file (ElevenLabs) so you can hear the voice before deploying it
- Rationale documentation for key dimension values

---

## What's open, what's ours

```
Schema:           Open source (this repo)
Library:          CC-BY-4.0 — fork it, modify it, use it commercially
Compiler tools:   MIT Licensed (this repo)
Hosted compiler:  Ours — free to use at protagons.com/generate
```

The extraction pipeline — the 28-agent system that turns descriptions and writing samples into structured profiles — is proprietary. That's our secret sauce.

Everything it produces belongs to you. Every `.protagon.json` file you generate is yours, deployable on your own infrastructure, with your own API keys. We never see your LLM traffic.

---

## What you can build

- **OpenClaw agents** with a structured  source that compiles to SOUL.md — diffable, forkable, version-controlled identity
- **Game NPCs** with structured personality axes instead of ad-hoc prompts
- **Brand voice systems** where multiple writers share one authoritative character file
- **TTS pipelines** where the written voice and spoken voice derive from the same source
- **Writing tools** that generate content from inside a defined character rather than imitating style
- **Multi-model deployments** where a single `.protagon.json` compiles for each LLM

If you're building a writing application on top of Protagons, see [USAW.ai](https://usaw.ai) — the reference implementation.

---

## Repository structure

```
/
├── schema/
│   └── character.schema.json       ← The formal JSON Schema (v1.0.0)
├── profiles/
│   ├── archetypes/                 ← Jungian, Myers-Briggs, Enneagram
│   ├── professional/               ← Business, tech, creative roles
│   ├── adversarial/                ← Dark, antagonist, trickster
│   └── brand/                      ← Brand voice examples
├── docs/
│   ├── SPEC.md                     ← Full specification (start here)
│   ├── dimensions/                 ← One doc per dimension category
│   └── rationale.md                ← Why 28 dimensions, not 20 or 40
├── tools/
│   ├── compiler.py                 ← Build a system prompt from a profile
│   ├── validator.py                ← Validate a .protagon.json against schema
│   └── examples/                   ← Integration code (Python, JS, Go)
├── integrations/
│   ├── openclaw/
│   │   ├── compile_soul_md.py      ← .protagon.json → SOUL.md compiler
│   │   ├── batch_compile.py        ← Compile multiple profiles for multi-agent setups
│   │   └── example-SOUL.md         ← Real compiled output (Burned Out Ops)
│   ├── elevenlabs/
│   └── custom-gpt/
├── CONTRIBUTING.md
├── CHANGELOG.md
├── LICENSE-schema                  ← Open source
└── LICENSE-library                 ← CC-BY-4.0
```

---

## Contributing

The library grows through community contributions. You can:

- **Add a profile** — Submit a new `.protagon.json` to `/profiles/`. See [CONTRIBUTING.md](./CONTRIBUTING.md) for the review process.
- **Propose schema changes** — Open an issue with the `schema` label. Breaking changes go through a formal RFC process.
- **Fix a profile** — If a dimension value is wrong or a confidence score seems off, submit a PR with your evidence.
- **Add integrations** — New platform integration examples in `/tools/examples/` are welcome.

The extraction pipeline that generates profiles from scratch isn't open source — but the schema is, so you can build your own extractor on top of it.

---

## The HN post

If you found this from Hacker News: [the original post is here](https://news.ycombinator.com/). Questions, pushback, and "why not just use X" arguments welcome in the comments.

---

## License

Schema and tooling: Open source — see [LICENSE-schema](./LICENSE-schema)

Library profiles: [CC-BY-4.0](./LICENSE-library) — use them anywhere, in any project, commercially or otherwise. Attribution required.

---

*Protagons is an open standard. USAW.ai is the reference writing application built on top of it. They're separate products with separate audiences. This repo is for the standard.*
