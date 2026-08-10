# Project Description

Put in a brief description of the project.

# Standard Project Layout

This file is the primary **bootloader** for AI agents and coding assistants.

It provides orientation and points to more detailed context as needed.
This structure follows the [AI Coding Repository Structures standard](https://github.com/salotz/rfcs/blob/master/rfcs/salotz.022_ai-coding-structure/README.md).

> **Note for copy-paste**: This is a template. Relative links below (e.g. `design/goals.md`) are meant to point to files in *your* project after you adopt this structure. Absolute links point to the official specification in this repository.

## How to Use

- Read this first on every new session or major task.
- Small projects: expand inline with context.
- Large projects/monorepos: keep compact (TOC style). Load additional files only when needed.
- Prefer incremental disclosure: start general, fetch specifics (goals, glossary, etc.) as required.

## Project Intent

Goals, non-goals, and principles:

- [design/goals.md](design/goals.md)

See the [Goals section](https://github.com/salotz/rfcs/blob/master/rfcs/salotz.022_ai-coding-structure/README.md#goals) of the standard.

## Terminology

Project-specific terms:

- [design/glossary.md](design/glossary.md)

Reference external glossaries as listed.

## Design

Design docs live under `design/`:

- [design/README.md](design/README.md) — layout of this folder (see [Design section](https://github.com/salotz/rfcs/blob/master/rfcs/salotz.022_ai-coding-structure/README.md#design) of the standard).
- [design/architecture/](design/architecture/) — current architecture.
- [design/decisions/](design/decisions/) — ADRs (Nygard style; e.g. `0001_decision-name.md`).

## Agent Context (.agents/)

Large, progressive, or agent-specific context goes in the `.agents/` directory:

- `skills/`: Agent skills per [agentskills.io](https://agentskills.io/home) (see summary in [agentskills_summary.md](agentskills_summary.md)).
- `agents/`: Custom agent definitions (see [this page](https://goose-docs.ai/docs/guides/context-engineering/custom-agents)).
- `context/`: Arbitrary additional context files (treated as an extension of this bootloader to reduce per-session load).

## Contributing Processes

Instructions are in:

- [contributing/](contributing/) (preferred), or
- `CONTRIBUTING.md` (small projects)

Start with [contributing/README.md](contributing/README.md).

Specific processes (e.g. `releases.md`, `role_engineer.md`) may be exposed as agent skills.

## Naming Conventions

Files/directories use **Name Expressions (nexps)**:

- [Name Expressions (nexps) standard](https://github.com/salotz/rfcs/blob/master/rfcs/salotz.004_nexps.md)

Dots (`.`) separate namespaces; underscores/hyphens separate fields.

## General Guidance for Agents

- `design/` and `contributing/` content is dual-use (human + agent).
- Load the most specific relevant file rather than guessing.
- Respect recursive structure (sub-projects may have their own `design/`, `contributing/`, `AGENTS.md`).
- Check relevant ADRs before significant changes.

Keep this file mostly human-readable while effective for agents.
