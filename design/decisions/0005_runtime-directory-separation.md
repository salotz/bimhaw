# ADR-0005: Separation of User Configuration from Runtime Directory (~/.bimhaw)

**Status**: Accepted (Current State)

**Date**: 2026-07-28 (documented retrospectively)

**Deciders**: Original author (Samuel D. Lotz)

## Context

Early experiments and traditional dotfile setups often placed all configuration directly in `~/.config/...` or even directly under `$HOME` as dotfiles. This creates problems:

- The "live" configuration is mixed with generated or transient state.
- It is hard to keep configuration under version control cleanly when the runtime directory contains both source and artifacts.
- Users may accidentally commit or edit generated files.
- Different machines or contexts may need different "build" outputs even from the same source configuration.

The author wanted a clear separation between what the user edits and what the tool produces at runtime.

## Decision

bimhaw designates `~/.bimhaw` (the `CONFIG_DIR`) as a **runtime / build / cache directory**, not the primary source of truth.

- User configuration lives in a separate location: typically a `config.py` and `lib/` tree, often kept inside a personal dotfiles repository (e.g. `~/.salotz.d`).
- `bimhaw_init` can initialize `~/.bimhaw` while pointing it at external configuration locations.
- The runtime directory contains generated profile scripts, the `active` symlink, and the shell dotfile symlinks.
- Users are expected to treat `~/.bimhaw` as disposable or regenerable.

## Rationale

- Makes it safe to regenerate or wipe the runtime directory without losing user intent.
- Supports the use case of keeping personal configuration in a separate, version-controlled repo.
- Clarifies the mental model: "edit here, generate and activate there."
- Reduces the risk of users editing generated files directly.

## Consequences

**Positive**:
- Clear ownership: user edits config + lib; tool owns `~/.bimhaw`.
- Supports multiple machines sharing the same configuration source.
- Easier to implement "reset" or "re-init" operations in the future.

**Negative / Trade-offs**:
- Requires an explicit initialization step to set up the link between source config and runtime dir.
- Users must understand there are two locations involved.
- The `~/.bimhaw` directory still ends up in the user's home, which can be surprising if not documented.

## Related Decisions

- ADR-0004: Generation via Templates
- ADR-0006: Symlink Indirection
- ADR-0007: Configuration Representation

## References

- README.org: "Indirection and Generation", "~/.bimhaw/ acts as a build/cache directory"
- `src/bimhaw/__init__.py`: `CONFIG_DIR`
- `bimhaw_init` command
