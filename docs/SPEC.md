# Protagons Specification

**Version:** 1.0.0

This document defines the `.protagon.json` file format — a portable, structured representation of AI character identity.

## Overview

A Protagon profile encodes a character's linguistic and psychological identity across 28 dimensions with 287 total fields. Each field is evidence-backed and confidence-scored.

## Schema

The formal JSON Schema is located at [`/schema/character.schema.json`](../schema/character.schema.json).

## Dimensions

For a detailed breakdown of all 28 dimensions, see [`dimensions.md`](./dimensions.md).

## Required Fields

Every `.protagon.json` file must contain:

- `name` (string) — Display name of the character
- `spec_version` (string) — Semantic version of the spec (e.g., `"1.0.0"`)

## Recommended Fields

- `synthesized_prompt` — Compiled system prompt for LLM use
- `dimensions` — The 28 analytical facets
- `personality` — Five bipolar personality axes
- `metadata` — Provenance and licensing

## File Extension

Files should use the `.protagon.json` extension to indicate they conform to this specification.

## Versioning

The spec follows semantic versioning. Breaking changes increment the major version. New optional fields increment the minor version.
