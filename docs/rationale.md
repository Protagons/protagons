# Why 28 Dimensions

The Protagons schema uses exactly 28 dimensions to capture AI character identity. This document explains the reasoning behind this number and the selection of each dimension category.

## The Problem with Fewer

Most AI character systems use 5-10 parameters (tone, formality, personality type). This produces characters that sound similar — you get "friendly and professional" or "casual and witty" but nothing that would survive a Turing test against a real person's writing.

Real writing voice is the intersection of hundreds of micro-decisions: when to hedge, how to handle counterarguments, what kind of humor to deploy, whether to use contractions, how much to trust the reader. Fewer than ~25 dimensions and you lose the nuance that makes a voice recognizable.

## The Problem with More

Above ~30 dimensions, you hit diminishing returns. Additional dimensions start overlapping with existing ones, the extraction pipeline becomes unreliable, and the file size balloons without improving prompt quality.

28 is the empirical sweet spot: enough resolution to capture a distinctive voice, compact enough that every field earns its place.

## Dimension Categories

The 28 dimensions fall into four broad categories:

1. **Linguistic structure** (dimensions 1-16): How the voice constructs text
2. **Emotional/psychological** (dimensions 17-22): The voice's inner state
3. **Developmental** (dimensions 23-24): Age and temperament signals
4. **Deep psychology** (dimensions 25-28): Core beliefs and values

For the complete field-level breakdown, see [dimensions.md](./dimensions.md).
