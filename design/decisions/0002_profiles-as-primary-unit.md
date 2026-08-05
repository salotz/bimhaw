# ADR-0002: Profiles as the Primary Unit of Configuration and Switching

**Status**: Accepted (Current State)

**Date**: 2026-07-28 (documented retrospectively)

**Deciders**: Original author (Samuel D. Lotz)

## Context

Traditional shell configuration is organized around individual dotfiles (`.profile`, `.bashrc`, etc.). Users who want different environments (work vs personal, different machines, experimental vs stable) typically resort to manual copying, heavy conditionals, or maintaining entirely separate home directories or repos with duplicated logic.

The author needed a clean way to maintain multiple distinct shell setups without duplication or fragile conditional logic inside the dotfiles themselves.

## Decision

bimhaw treats **named profiles** as the primary unit of configuration and selection.

- A profile is a named collection of modules and settings.
- Users define profiles in `config.py` (e.g., `['bimhaw', 'common']`).
- Each profile has its own lists of modules for different categories and shell modes.
- Only one profile is active at a time.
- Profile switching is performed by updating the `active` symlink.

Profiles are intended to be coarse-grained and semantically meaningful to the user (e.g., "work-laptop", "minimal", "demo").

## Rationale

- Profiles provide a clear mental model: "I am using the X profile."
- They enable separation of concerns at a higher level than individual modules.
- They make it practical to maintain multiple environments without polluting a single set of scripts with conditionals.
- Switching via symlink is simple, fast, and does not require rewriting files or restarting the shell in most cases (new shell sessions pick up the new active profile).

## Consequences

**Positive**:
- Clear, user-facing concept for environment selection.
- Supports use cases like safe fallbacks, experimentation, and machine-specific setups.
- Reduces the temptation to put machine- or context-specific logic inside shared modules.

**Negative / Trade-offs**:
- Profiles are currently independent; there is no built-in inheritance or composition between profiles.
- Users must duplicate module lists across profiles when they share most configuration.
- The configuration format makes adding or renaming profiles somewhat tedious (manual edits to many dictionaries).

## Related Decisions

- ADR-0003: Modular Configuration: sh and bash Layers with sh Inheritance
- ADR-0005: Separation of User Configuration from Runtime Directory
- ADR-0006: Indirection via Symlinks for Activation and Dotfiles

## References

- README.org section on Profiles
- `docs/example_config.py` (shows per-profile dictionaries)
- Current `src/bimhaw/profile.py` and CLI profile commands
