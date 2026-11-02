# Step 0006: Optional `bimhaw context install`

**Status**: Not started — execution pending explicit user request

**Dependencies**: 0004 content exists as package data

## Context

Copy-paste of skills into `~/.agents/skills/` is enough for v1. An installer reduces drift for the operator who wants Goose + RFC 23 wired on every host.

## Concrete actions

1. `bimhaw context install [--dry-run] [--goose-hints]`:
   - write `~/.config/agents/shell.md` if missing; if present, skip or `--force`
   - write `~/.agents/skills/bimhaw-shell/SKILL.md` from package
   - if `--goose-hints` and `~/.config/goose/.goosehints` exists, append a marked block (idempotent, do not duplicate)
2. Never overwrite user-edited skill without `--force`.
3. Not required for the makeover.

## Verification

- Dry-run prints paths
- Second run is a no-op
