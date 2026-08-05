# ADR-0003: Modular Configuration via sh and bash Layers with sh Inheritance

**Status**: Accepted (Current State)

**Date**: 2026-07-28 (documented retrospectively)

**Deciders**: Original author (Samuel D. Lotz)

## Context

Shell configuration tends to mix portable POSIX constructs with bash-specific features inside the same files. This leads to:
- Accidental use of bashisms in files intended to be portable.
- Difficulty maintaining a clean base that works across different shell contexts.
- Duplication when trying to support both minimal sh and rich bash environments.

The author wanted a structure that encourages separation while still allowing powerful bash configuration.

## Decision

Configuration is organized into **modules** grouped into two layers:

- `lib/sh/` — POSIX-compatible modules (intended to work in `sh` and as a base for bash).
- `lib/bash/` — Bash-specific modules that may use bash features.

**Inheritance rule**: When bash is active, *all* applicable `sh/` modules are loaded first (in their categories), followed by `bash/` modules.

Modules are further organized by **category**:
- `envs`
- `funcs`
- `aliases`
- `prompts`
- `logouts`
- `autocomplete` (bash only)

The order of modules within a category for a profile is defined explicitly in `config.py`.

## Rationale

- Provides a clear boundary between portable and shell-specific code.
- Allows users to maintain a strong portable base (`sh/`) while optionally adding rich interactive features.
- The "sh inheritance" model reduces duplication: bash users get the portable modules automatically.
- Categories enforce separation of concerns (environment setup vs functions vs aliases, etc.).

## Consequences

**Positive**:
- Encourages writing portable code by default.
- Makes it easier to audit what is bash-only.
- Categories provide natural grouping for prompts, logout actions, etc.

**Negative / Trade-offs**:
- Users must maintain module lists in two places conceptually (sh and bash) even when using inheritance.
- The inheritance is implicit in the loading logic rather than explicit in configuration.
- Some categories (e.g. autocomplete) only make sense for certain shells, leading to asymmetry.

## Related Decisions

- ADR-0002: Profiles as the Primary Unit
- ADR-0007: Configuration Representation (how module lists are expressed per profile)

## References

- README.org: "Module System" and "sh vs bash separation"
- `docs/example_config.py` (shows separate `SH_*` and `BASH_*` dictionaries)
- `src/bimhaw/__init__.py` (LIB_DIRS definition)
