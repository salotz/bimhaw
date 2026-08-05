# ADR-0004: Configuration via Generated Scripts from Jinja2 Templates

**Status**: Accepted (Current State)

**Date**: 2026-07-28 (documented retrospectively)

**Deciders**: Original author (Samuel D. Lotz)

## Context

Directly editing the final shell dotfiles or profile scripts leads to several problems:
- Changes to the tool's logic require users to manually update their scripts or risk divergence.
- It is easy to accidentally customize generated content in ways that get overwritten or conflict with future versions.
- Supporting profile switching cleanly is difficult if the "active" logic is baked into user-edited files.

At the same time, the final shell scripts need to contain the correct module sourcing order and some bootstrap logic that depends on the chosen profile and shell mode.

## Decision

bimhaw uses **Jinja2 templates** to generate the runtime shell scripts for each profile.

- The core logic for how modules are organized and sourced lives in the tool's templates.
- `bimhaw profile gen` renders the templates for a specific profile using data from `config.py`.
- The generated files are placed in `~/.bimhaw/profiles/<name>/`.
- Generated files are intended to be **read-only artifacts** from the user's perspective; they should be regenerated rather than hand-edited when the tool or configuration changes.

The templates deliberately keep the generated output relatively thin and auditable (mostly lists of modules to source).

## Rationale

- Generation decouples the tool's implementation details from user configuration.
- It allows improvements to startup logic, ordering, or new features to be rolled out by regenerating profiles rather than requiring manual migration.
- It supports the principle of keeping user intent (which modules belong where) separate from the mechanics of how they are loaded.
- Jinja2 was a pragmatic choice given its maturity and the existing Python ecosystem of the tool.

## Consequences

**Positive**:
- Tool evolution does not force users to edit low-level scripts.
- Profile scripts can be regenerated safely and consistently.
- The generated files serve as a clear, inspectable record of what the profile will do.

**Negative / Trade-offs**:
- Users must remember to re-run generation after configuration changes.
- There is an extra step in the workflow (`gen` before or after editing).
- Debugging sometimes requires looking at both the source configuration and the generated output.

## Related Decisions

- ADR-0005: Runtime Directory Separation
- ADR-0006: Symlink Indirection

## References

- README.org: "Indirection and Generation"
- `src/bimhaw/profile.py` (generation logic, not deeply indexed yet)
- Jinja2 usage in the package
