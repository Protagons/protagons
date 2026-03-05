# Protagon Dimensions Reference

Every `.protagon.json` contains 28 linguistic dimensions extracted by specialized AI agents. Each dimension captures a distinct facet of how a character thinks, writes, and communicates.

## The 28 Dimensions

### 1. Rhetorical Architecture
How arguments are structured and deployed. Includes thesis positioning, evidence patterns, counterargument handling, and persuasion strategies.

### 2. Modal-Epistemic Stance
Certainty and knowledge claims. How the voice hedges, asserts, speculates, and signals what it knows vs. believes vs. assumes.

### 3. Metadiscourse
Self-referential language. How the voice talks about its own communication — signposting, hedging, boosting, commenting on the discourse itself.

### 4. Audience Relationship
Reader/listener positioning. How the voice addresses, includes, challenges, or distances its audience. Power dynamics and solidarity markers.

### 5. Genre Conventions
Format and structural expectations. How the voice adapts to genre norms — academic, journalistic, conversational, creative, technical, etc.

### 6. Cohesion Architecture
How ideas connect. Transition patterns, paragraph structure, thematic threading, information flow between sentences and sections.

### 7. Evaluative Language
Judgment and appraisal. How the voice evaluates people, ideas, events — positive/negative, strong/weak, important/trivial.

### 8. Identity Construction
Self-presentation. How the voice constructs and performs identity through language — professional, personal, cultural, ideological.

### 9. Temporal Patterns
Time orientation. How the voice uses tense, aspect, temporal markers — past-focused, present-anchored, future-oriented.

### 10. Visual Integration
Imagery and sensory language. How the voice uses metaphor, simile, concrete imagery, spatial language, and sensory details.

### 11. Lexical Sophistication
Vocabulary profile. Word choice complexity, register, technical density, neologism frequency, etymological preferences.

### 12. Engagement Devices
Reader interaction techniques. Questions, directives, shared knowledge appeals, humor, surprise, emotional hooks.

### 13. Intertextuality
References and allusions. How the voice draws on other texts, cultural artifacts, shared knowledge, and common narratives.

### 14. Information Architecture
How information is organized and prioritized. Given-new patterns, topic management, information density.

### 15. Prosodic Features
Rhythm and emphasis. Sentence length variation, stress patterns, pausing, spoken-word qualities in written text.

### 16. Cultural Markers
Cultural positioning. Regional idioms, generational references, subculture signals, in-group vocabulary.

### 17. Emotional Architecture
Emotional range and regulation. How the voice expresses, modulates, and responds to emotion.

### 18. Formality Components
Register and decorum. How the voice calibrates between formal and informal across different contexts.

### 19. Psychological Trauma Markers
Trauma-related linguistic patterns. How past experiences surface in communication patterns (avoidance, hypervigilance, narrative fragmentation).

### 20. Neurological-Cognitive Patterns
Cognitive style markers. Processing speed indicators, attention patterns, memory references, executive function signatures.

### 21. Mental Health Markers
Psychological state indicators. Anxiety patterns, mood stability, cognitive distortions, coping strategy language.

### 22. Physical Health State Markers
Embodiment language. How physical state, energy, pain, vitality surface in communication.

### 23. Age-Developmental Markers
Developmental stage indicators. Vocabulary age, cultural reference era, maturity level, generational identity.

### 24. Personality-Temperament Patterns
Core temperament. Introversion/extraversion, openness, conscientiousness, agreeableness, neuroticism as expressed through language.

### 25. Core Psychology
Deep psychological structure. Attachment style, defense mechanisms, object relations, self-concept.

### 26. Motivational Architecture
What drives the voice. Achievement orientation, affiliation needs, power dynamics, intrinsic vs. extrinsic motivation.

### 27. Worldview Deep Structure
Fundamental assumptions. Ontological beliefs, epistemological stance, cosmological orientation, existential positioning.

### 28. Moral-Ethical Framework
Values and ethics. Moral reasoning style, ethical priorities, justice orientation, care ethics, virtue emphasis.

## Dimension Data Structure

Each dimension in the `.protagon.json` is stored as a structured object with:

```json
{
  "dimensions": {
    "rhetorical_architecture": {
      "primary_mode": "analytical-systematic",
      "argument_structure": "evidence-first",
      "evidence_preferences": ["data", "case_studies", "expert_opinion"],
      "counterargument_handling": "acknowledge-and-reframe",
      "persuasion_strategy": "logical-progression",
      "confidence_score": 0.87
    }
  }
}
```

Field names and structures vary by dimension. See the [JSON Schema](../schema/v1/protagon.schema.json) for the complete specification.

## Personality Axes

In addition to the 28 dimensions, each Protagon includes personality axes from established frameworks:

- **Big Five (OCEAN)**: Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism (0-100 scale)
- **Jungian Archetype**: Primary and shadow archetypes
- **Enneagram**: Primary type and wing
- **Communication Style**: Dominant, Expressive, Analytical, Driver

These are stored in the `personality` top-level object.
