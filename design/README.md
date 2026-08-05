# Design Documentation

This directory contains the collected knowledge, architectural decisions, and design rationale for the **bimhaw** project.

## Purpose

The `design/` folder serves as the single source of truth for:

- **Why** the system is built the way it is
- **What** the high-level architecture looks like
- **Which** decisions have been made (and their trade-offs)
- **How** to evolve the system in a principled way

It is intentionally separated from both the source code and the user-facing documentation. This allows the design to be maintained as a first-class artifact, especially useful when scaling development with AI coding agents or when onboarding contributors.

## Goals for This Documentation

1. Capture the **current state** of the project accurately before any significant refactoring or modernization.
2. Make implicit knowledge (from the original author’s experience) explicit.
3. Provide a stable foundation for future design discussions, ADRs, and implementation plans.
4. Demonstrate professional-grade practices even on a small personal tool, as an exercise in scaling AI-assisted development.

## Directory Structure

```
design/
├── README.md                 # This file
├── goals.md                  # Goals, non-goals, and overriding principles
├── glossary.md               # Key terms and concepts
├── architecture/
│   └── overview.md           # High-level architecture description
├── decisions/
│   ├── 0000_adr-template.md  # Template for new Architecture Decision Records
│   └── 0001_*.md             # Numbered ADRs following RFC naming (index_name.md)
├── diagrams/                 # Architecture and problem diagrams (source + rendered)
└── research/                 # Background research, shell startup analysis, alternatives (optional)
```

## How to Use This Folder

- **Read first**: Start with `goals.md`, `glossary.md`, and `architecture/overview.md`.
- **Understand decisions**: Read the ADRs in `decisions/`. They document both historical choices and the "as-is" state.
- **Before proposing changes**: Update or add an ADR. Reference the relevant architecture section.
- **With AI agents**: Point agents at this directory early. It provides the context they need to make decisions consistent with the project's intent.

## Current Status

As of the creation of this folder (2026-07), this documentation describes the project **as it exists today**, based on the original implementation and README. No major refactoring has yet been planned or executed using this design material.

The project was originally written as a practical personal tool. The creation of `design/` marks the intentional shift toward treating it with the rigor of a larger, professional codebase.

## Contributing to Design

- Use the ADR template when recording new decisions.
- Keep ADRs focused and decision-oriented (not implementation details).
- Update architecture documents when the mental model changes.
- Diagrams in `diagrams/` should be source-controlled (Graphviz .dot preferred where possible).

## Relationship to Other Documentation

- `README.org` — User-oriented overview and quick start
- `docs/` — Supporting diagrams and example configuration
- `design/` — **Internal** design memory and decision history (this folder)
- Source code — The current realization (to be analyzed after design baseline is established)

## References

- Original shell startup complexity diagram: `docs/manpage_shell_startup.dot`
- Logical layered model: `docs/logical.dot`
- Example configuration shape: `docs/example_config.py`
