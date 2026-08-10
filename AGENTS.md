# Project Description

Guidance for AI agents (and humans) working on the **bimhaw** codebase.

bimhaw is a tool for managing shell configuration using **profiles** and **modules**. It generates thin shell scripts from templates and uses symlinks + indirection to support multiple environments without duplicating logic or editing raw dotfiles.

# Standard Project Layout

This file is the primary **bootloader** for AI agents and coding assistants.

It provides orientation and points to more detailed context as needed.
This structure follows the [AI Coding Repository Structures standard](https://github.com/salotz/rfcs/blob/master/rfcs/salotz.022_ai-coding-structure/README.md) (RFC 22), along with RFC 23 (local agent context) and RFC 24 (extended XDG / naming).

> **Note**: Relative links below point to files in this project. See `.agents/references/agent-guidelines/` for cached summaries and full references.

## How to Use

- Read this first on every new session or major task.
- Small projects: expand inline with context.
- Large projects/monorepos: keep compact (TOC style). Load additional files only when needed.
- Prefer incremental disclosure: start general, fetch specifics (goals, glossary, etc.) as required.
- This project is in the process of adopting the full structure (see `.agents/plan/` for the upgrade plan).

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

- `.agents/plan/` — upgrade/refactor/feature plans (this adoption effort documented here).
- `.agents/references/agent-guidelines/` — cached copies of guidelines, RFC summaries (RFC 22/23/24), and supporting material.
- `skills/`: Agent skills per [agentskills.io](https://agentskills.io/home).
- `agents/`: Custom agent definitions.
- `context/`: Arbitrary additional context files (treated as an extension of this bootloader).

See `.agents/references/agent-guidelines/summaries/salotz-rfc-022-ai-coding-structure.md` and related.

## Contributing Processes

Instructions are in:

- [contributing/](contributing/) (preferred), or
- `CONTRIBUTING.md` (small projects)

Start with [contributing/README.md](contributing/README.md).

Specific processes (e.g. `releases.md`, `role_engineer.md`) may be exposed as agent skills.

## Naming Conventions

Files/directories use **Name Expressions (nexps)**:

- [Name Expressions (nexps) standard](https://github.com/salotz/rfcs/blob/master/rfcs/salotz.004_nexps.md) (see RFC 24 summary)

Dots (`.`) separate namespaces; underscores/hyphens separate fields.

## General Guidance for Agents

- `design/` and `contributing/` content is dual-use (human + agent).
- Load the most specific relevant file rather than guessing.
- Respect recursive structure (sub-projects may have their own `design/`, `contributing/`, `AGENTS.md`).
- Check relevant ADRs before significant changes.
- Prefer task-specific tools (write, tree, analyze, summarize, edit, todo) over shell.
- Cache remote resources locally under `.agents/references/` when possible.
- Use compacted inlining for referenced standards.
- Follow RFC 22 (project layout), RFC 23 (host context), RFC 24 (naming / XDG).

This project is adopting these guidelines; see `.agents/plan/README.md` and the adoption ADR (to be added) for status.

Keep this file mostly human-readable while effective for agents.

---
*Analyzed via task tools only.*