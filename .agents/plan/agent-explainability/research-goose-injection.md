# Research: Goose context injection (for bimhaw explain / prompt legend)

**Date**: 2026-10-23  
**Docs root**: https://goose-docs.ai (map: `/goose-docs-map.md`)  
**Status**: Supporting note — not an ADR

Verified against official docs before planning. Do not invent Goose field names.

## Mechanisms that apply

### Skills (primary for this plan)

Source: [Agent Skills](https://goose-docs.ai/docs/guides/context-engineering/using-skills)

- Session start: goose adds **skill names and descriptions** to instructions (not full `SKILL.md`).
- Full skill loads when the request matches the description, or the user says to use it, or `/skills name`.
- Locations (recommended): `~/.agents/skills/<name>/SKILL.md` (global), `<project>/.agents/skills/` (project), plugins.
- Frontmatter **requires** `name` and `description`.
- Compatible with agentskills.io / Claude Desktop.
- Supporting files in the skill directory are visible when the skill is loaded.

**Implication:** put bimhaw *consumer* docs in a **global** skill. The `description` must mention PS1 / `~/.bimhaw` / nonstandard bashrc or Goose will never load it for a pasted prompt.

### `.goosehints` (session-start project/global context)

Source: [Providing Hints](https://goose-docs.ai/docs/guides/context-engineering/using-goosehints)

- Global: `~/.config/goose/.goosehints`
- Local: `.goosehints` in dir hierarchy (git repo: cwd up to root at start; nested loaded when files in those dirs are accessed)
- Also loads `AGENTS.md` by default; `CONTEXT_FILE_NAMES` can add names
- `@path` **includes file content** in immediate context; bare paths are “read if needed”
- Loaded at session start (plus nested later); **can be forgotten** as context fills
- Uses tokens; keep short
- Local overrides global on conflict
- Needs Developer extension

**Implication:** 5–15 lines in global hints pointing at RFC 23 `shell.md` via `@` is OK. Do **not** `@` generated `bimhaw explain` output (stale after `profile load`).

### Persistent instructions / MOIM (every turn)

Source: [Persistent Instructions](https://goose-docs.ai/docs/guides/context-engineering/using-persistent-instructions)

- `GOOSE_MOIM_MESSAGE_TEXT` / `GOOSE_MOIM_MESSAGE_FILE` injected **every turn** (64 KB cap)
- For critical guardrails, not project encyclopedias
- vs goosehints: cannot be forgotten; costs tokens **per turn**

**Implication:** **do not** put bimhaw explain or prompt legends here.

### Prompt templates (`system.md` etc.)

Source: [Customizing Prompt Templates](https://goose-docs.ai/docs/guides/context-engineering/prompt-templates)

- Overrides in `~/.config/goose/prompts/`
- Affects all sessions

**Implication:** do not customize `system.md` for bimhaw.

### Hooks

Source: [Hooks](https://goose-docs.ai/docs/guides/context-engineering/hooks)

- `UserPromptSubmit` etc. via plugins under `~/.agents/plugins/`
- Could theoretically prepend explain text — overkill, runs local commands, trust issues

**Implication:** out of scope.

### `@` in this product (Goose vs user prompt)

Goose `@file` in **hints** includes that file. Unrelated to the user’s shell prompt `*** user@host`. The user said they like `@goose` **integration** — meaning they want Goose to understand shell metadata, not that bimhaw should implement Goose’s `@` syntax in PS1.

## RFC 23 overlay

Host files: `$XDG_CONFIG_HOME/agents` then `~/.agents`. Recommended `shell.md`. Goose does not read RFC 23 natively unless:

- `CONTEXT_FILE_NAMES` includes those names, or
- `.goosehints` `@~/.config/agents/shell.md`, or
- a skill tells Goose to read that path.

The plan therefore **bridges**: RFC 23 file is the canonical short host text; Goose hints `@` it; skill carries the workflow (`bimhaw explain`).

## What Goose already injects (do not duplicate)

Persistent/MOIM already includes timestamp, cwd, todos (docs: “current timestamp, working directory, and your todo list”). The **structured PS1** still matters because:

- Pasted transcripts are not a live Goose session
- Fields like histnum, job count, exit code, Lustre path, profile marker are **not** in MOIM
- Other agents (non-Goose) see only the paste

## Docs used

- https://goose-docs.ai/docs/guides/context-engineering/using-skills
- https://goose-docs.ai/docs/guides/context-engineering/using-goosehints
- https://goose-docs.ai/docs/guides/context-engineering/using-persistent-instructions
- https://goose-docs.ai/docs/guides/context-engineering/index
- https://goose-docs.ai/docs/guides/context-engineering/hooks
- https://goose-docs.ai/docs/guides/context-engineering/prompt-templates
