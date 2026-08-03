# Project Description

Guidance for AI agents (and humans) working on the **bimhaw** codebase.

bimhaw is a tool for managing shell configuration using **profiles** and **modules**. It generates thin shell scripts from templates and uses symlinks + indirection to support multiple environments without duplicating logic or editing raw dotfiles.

# Standard Project Layout

This file is the primary **bootloader** for AI agents and coding assistants.

It provides orientation and points to more detailed context as needed.
This structure follows the [AI Coding Repository Structures standard](https://github.com/salotz/rfcs/blob/main/rfcs/salotz.022_ai-coding-structure/README.md).

> **Note for copy-paste**: This is a template. Relative links below (e.g. `design/goals.md`) are meant to point to files in *your* project after you adopt this structure. Absolute links point to the official specification in this repository.

## How to Use This Document

- Read this file first on every new session or major task.
- For **small projects** this file may grow to contain most of the relevant
  context.
- For **large projects** or monorepos, keep this file compact (table of
  contents style). Load additional files only when the task requires them.
- Prefer incremental context: start general, then fetch specific files
  (goals, glossary, architecture, processes) as needed.

## Project Intent and Principles

The goals, non-goals, and overriding principles for this project are
documented in:

- [design/goals.md](design/goals.md)

See the [Goals section](https://github.com/salotz/rfcs/blob/main/rfcs/salotz.022_ai-coding-structure/README.md#goals)
of the AI Coding Repository Structures standard for more information.

Read this early when starting work.

## Terminology

Project-specific terms and definitions live in:

- [design/glossary.md](design/glossary.md)

You may also reference external glossaries listed there.

## Design Documentation

Design information is organized under the `design/` directory:

- [design/README.md](design/README.md) — explains the layout of the design
  folder for this project. See the
  [Design section](https://github.com/salotz/rfcs/blob/main/rfcs/salotz.022_ai-coding-structure/README.md#design)
  of the [AI Coding Repository Structures standard](https://github.com/salotz/rfcs/blob/main/rfcs/salotz.022_ai-coding-structure/README.md) for the full specification.
- [design/architecture/](design/architecture/) — current architecture of the system.
- [design/decisions/](design/decisions/) — Architecture Decision Records (ADRs) following the
  [Nygard style template](https://github.com/architecture-decision-record/architecture-decision-record/tree/main/locales/en/templates/decision-record-template-by-michael-nygard).
  Files are named with an index, e.g. `0001_decision-name.md`.

Use these to understand both the current state and the reasoning behind it.

## Contributing Processes

Instructions for working on the project are in:

- [contributing/](contributing/) (preferred for non-trivial projects), or
- `CONTRIBUTING.md` (for very small projects)

Start with [contributing/README.md](contributing/README.md) (or the root
`CONTRIBUTING.md`).

Specific processes are in dedicated files (e.g. `releases.md`,
`role_engineer.md`). These may be exposed as agent skills.

## Naming Conventions

Files and directories follow structured **Name Expressions (nexps)** as
defined in the [Name Expressions (nexps) standard](https://github.com/salotz/rfcs/blob/main/rfcs/salotz.004_nexps.md).

- Dots (`.`) separate namespaces.
- Underscores (`_`) and hyphens (`-`) separate fields within names.

See the standard linked above for details when interpreting or creating new names.

## General Guidance for Agents

- The content in `design/` and `contributing/` is intended to be useful for
  both humans and agents.
- When in doubt, load the most specific relevant file rather than guessing.
- Respect recursive structure: sub-projects may have their own `design/`,
  `contributing/`, and `AGENTS.md` files.
- Always check for relevant ADRs before proposing significant changes.

This file should remain mostly human-readable while still being effective
context for agents.
