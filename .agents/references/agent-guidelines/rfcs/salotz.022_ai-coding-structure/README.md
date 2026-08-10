# AI Coding Repository Structures

- nexp :: `salotz.022_ai-coding-structure`
- long name :: AI Coding Repository Structures
- executive summary :: Provides a standard for structuring repositories to make them useful for AI-enhanced coding. Includes standard naming and schemas for folders, filenames, and content of those files. The goal is to provide useful, incremental context for LLMs that are built up for a specific coding repository.

## Goals

The goal of this is to provide a common structure for adding context
for LLMs and AI or agentic coding to guide them towards writing code
for the author's intent.

LLMs do best when you can provide clear guidelines with minimal
context that is incrementally divulged when necessary.

The content written for AI coding systems should also be *mostly*
useful for humans, as well as in understanding the details of how to
work on a project. There will be content that is specifically for the
AI systems.

When possible we support and prioritize open standards that are
supported by common implementations. But we don't slavishly obey them
where it makes sense not to.

Not all components of this RFC need to be used by all projects. As a
project grows in size and complexity you will use more components as
context limits allow.

## Components


### Generic Rules

Files and folders should be named according to name expressions ([RFC
salotz.004_nexps](../salotz.004_nexps.md)).

See that RFC for details on what the fields in the names should mean.

### Bootloader

There should be a file that should be present at the root of the
project that any AI system can always load to provide context.

For this we stick to the standard [`AGENTS.md`](https://agents.md/) file.

The content of the file should depend on the size and scope of the project.

In a small project it might contain all context but for larger
projects this should only contain a "table of contents" of where to
find instructions and content.

A template is provided alongside this document as
[AGENTS.md](agents_md_template.md).

For small projects it can be expanded with more inline context. For
larger projects it should act primarily as a table of contents
pointing to other context directories like `.agents/`, `design/`,
`contributing/`, and other relevant files.

### Agent Specific Context

Most other directories are dual-use for humans and agents. Additional agent
specific context should be placed in the `.agents/` directory.

This should be used for context that is too large for the Bootloader
file, should be disclosed progressively, or is a standardized form of
context understood by most coding agent harnesses.

This includes the external /de facto/ standards:

- `skills/`: For agent skills defined by the [agentskills.io](https://agentskills.io/home) specification (agents see summary description in this [file](./agentskills_summary.md))
- `agents/`: For defining custom agents. See [this page](https://goose-docs.ai/docs/guides/context-engineering/custom-agents).


Additionally this RFC adds:

- `context/`: Which is simply a collection of arbitrary context discoverable by agents. This is treated like an extension of the Bootloader context to reduce context loaded in each session.

### Design

Each project should have documentation associated with the design of
the project.

This information is housed in the `design/` folder.

There are multiple subsections of the design folder.

#### README

There should be a `README.md` (and optional `AGENTS.md`) that explains
the structure of the directory. There should be a minimal
self-contained description as well as a hyperlink to this reference.

#### Goals

Each project should have a specific `goals.md` file which describes
the goals, non-goals, and any overriding principles that guide the
project.

#### Glossary

A glossary should be used to define any project specific terminology.

You can also reference other glossaries that are relevant to the project.

The glossary should be in the file `glossary.md`.

Glossary should follow this format:

```markdown

# Glossary

## Term A

Write the definition here.

## Term B

Similar to [Term A](#term-a), but different.

```

The subheading approach is preferred because you can then link between them in definitions.

#### Architecture

An architecture subdirectory, `architecture/`, should be used to
describe the current architecture of the system.

The needs in this directory should be tuned to your project's needs.

This folder should only be the current state. For historical
background on why certain decisions were made see the Decisions
section.

#### Decisions

Specific decisions should be documented. These use the [Architecture Decision Record](https://github.com/architecture-decision-record/architecture-decision-record) framework.

ADRs should be placed in this directory and named with fields (index,
name), e.g. `0001_decision-name.md`.

ADRs should be written using the [Nygard style](https://github.com/architecture-decision-record/architecture-decision-record/tree/main/locales/en/templates/decision-record-template-by-michael-nygard).

Using this template:

```markdown
# ADR 0000: Long Name of Decision

**Status**: Proposed / Accepted / Superseded / Deprecated
**Date**: YYYY-MM-DD
**Deciders**: <names of deciders>

## Context
What is the issue that we're seeing that is motivating this decision or change?

Describe the forces at play:
- Technical constraints
- Business or user needs
- Existing system state
- Team or process considerations

## Decision

What is the change that we're proposing or making?

State it clearly and directly.

## Consequences

What are the consequences of this decision?

- Positive
- Negative
- Risks and mitigations
- Follow-up work required

```

### Contributing Instructions

Each project has instructions, processes, and guidelines for
contributing to the project.

This information is housed in the `contributing/` folder or for
smaller projects a `CONTRIBUTING.md` file. If the `contributing/`
folder is present the `CONTRIBUTING.md` file should not be present.

The `contributing/` directory should contain a `README.md` (and an
optional `AGENTS.md` file) with generic considerations.

Additional files should contain documentation on specific work
processes for the project. These can be for specific tasks or
roles. For instance you might have task-based processes for releases,
migrations, etc. which you should name descriptively `releases.md`,
`migrations.md` (or more fully `process_releases.md`,
`process_migrations.md`). Or roles like engineer, product manager,
site reliability engineer (named `role_engineer.md`,
`role_product-manager.md`, `role_sre.md`).

For the full names of each the fields are (document type, name).

Processes should be made available as specific skills to agents
according to [agentskills.io](https://agentskills.io/).

(TODO)
Structure for skills is TBD.


## Generic Structural Considerations

All structure should support recursive definition for large repos
(like monorepos) with multiple sub-projects.
