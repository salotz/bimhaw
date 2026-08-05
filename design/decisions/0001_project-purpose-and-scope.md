# ADR-0001: Project Purpose and Scope

**Status**: Accepted (Current State)

**Date**: 2026-07-28 (documented retrospectively)

**Deciders**: Original author (Samuel D. Lotz)

## Context

Shell configuration on Unix-like systems (particularly Linux with bash) is notoriously difficult to manage:

- The interaction between login/non-login shells, interactive/non-interactive shells, `/etc/profile`, `~/.profile`, `~/.bash_profile`, `~/.bashrc`, `$ENV`, and `$BASH_ENV` is complex and poorly understood by most users.
- Traditional dotfiles tend to become monolithic and mix concerns.
- There is no native, convenient support for maintaining multiple distinct shell environments (e.g., personal vs work, minimal vs riced, different machines).

The author developed bimhaw as a personal tool after experiencing these problems while maintaining their own dotfiles over time. The project was extracted from real usage in `~/.salotz.d`.

## Decision

bimhaw exists to provide a practical, higher-level tool for managing shell configuration with the following primary goals:

- Make shell startup understandable and maintainable by introducing **profiles** and **modules**.
- Abstract away the legacy POSIX/bash startup complexity so users do not have to reason about it constantly.
- Support easy definition and switching between multiple shell profiles.
- Separate concerns through a modular system while still producing correct behavior for different shell invocation modes.

The project is deliberately scoped to shell (primarily bash with a POSIX sh base). It is not intended as a general-purpose dotfile manager for all configuration.

## Rationale

- The author found existing dotfile management approaches insufficient for the specific pain of shell startup ordering and multi-environment needs.
- A pragmatic tool that adds controlled indirection was judged better than continuing to edit raw dotfiles directly.
- The tool was built to serve an experienced user who values clarity and safety over minimalism in the configuration layer.

## Consequences

**Positive**:
- Users can think primarily in terms of "which profile am I using?" and "which modules belong here?"
- Multiple environments become practical to maintain.
- The core tool logic can be improved independently of user configuration via generation.

**Negative / Trade-offs**:
- The system introduces several layers of indirection (generation, symlinks, runtime directory).
- Initial setup and mental model are more complex than raw dotfiles.
- The tool is opinionated and not aimed at complete beginners.

**Current Limitations** (as of documentation):
- Primarily bash-focused.
- Configuration is still relatively verbose and manual.
- No formal validation of configuration.

## Related Decisions

- ADR-0002: Profiles as the Primary Unit of Configuration
- ADR-0003: Modular Configuration via sh and bash Layers with Inheritance
- ADR-0004: Configuration via Generated Scripts from Templates
- ADR-0005: Runtime Directory Separation
- ADR-0006: Symlink Indirection for Profile Activation and Dotfiles

## References

- Original README.org
- `docs/manpage_shell_startup.dot` (traditional complexity diagram)
- `docs/logical.dot` (intended logical layering)
