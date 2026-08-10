# Summary: salotz RFC 22 - AI Coding Repository Structures

Source: https://github.com/salotz/rfcs/tree/master/rfcs/salotz.022_ai-coding-structure

## Purpose
Standard structure for repositories to provide incremental, useful context to AI/LLM coding agents. Content should be mostly useful for humans too. Not all components required for every project.

## Core Components

### Bootloader
- Root `AGENTS.md` (per https://agents.md/)
- Small projects: full context inline.
- Larger: table of contents pointing to `.agents/`, `design/`, `contributing/`, etc.

### Agent-Specific Context
- `.agents/` directory for progressive disclosure and harness-specific context.
- Includes:
  - `skills/`: per agentskills.io
  - `agents/`: custom agents
  - `context/`: arbitrary discoverable context files

### Design Documentation (`design/`)
- `README.md` + optional `AGENTS.md`
- `goals.md`: goals, non-goals, principles
- `glossary.md`: project terminology (subheading format for cross-links)
- `architecture/`: current architecture state
- `decisions/`: ADRs using Nygard style (status, context, decision, consequences)

### Contributing Instructions (`contributing/`)
- `README.md` (and optional `AGENTS.md`)
- Task/role specific process docs (e.g. `releases.md`, `role_engineer.md`)
- Expose processes as agent skills

## Generic Rules
- Use name expressions (RFC salotz.004_nexps) for files/folders.
- Supports recursive/monorepo structures.

## References
- See original RFC for full details and templates.
