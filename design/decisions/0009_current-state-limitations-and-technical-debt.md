# ADR-0009: Current State Limitations and Acknowledged Technical Debt

**Status**: Accepted (Current State)

**Date**: 2026-07-28 (documented retrospectively)

**Deciders**: Original author (Samuel D. Lotz)

## Context

bimhaw was developed as a practical personal tool. It was extracted from the author's real dotfiles usage after approximately a year of evolution. The focus was on solving immediate problems rather than building a polished, general-purpose, or future-proof system.

As part of the decision to treat the project more professionally (including the creation of this `design/` folder), it is valuable to explicitly capture the known limitations and areas of technical debt before planning any modernization.

## Current Limitations (as of 2026-07)

### Configuration System
- Heavy reliance on a large number of explicit dictionaries in `config.py`.
- Loading via `exec()` with no validation or schema.
- Repetitive and error-prone (ADR-0007).
- No support for DRY constructs such as profile inheritance, mixins, or defaults.
- Distinctions like login/non-login are still visible in the configuration surface even though one goal is to hide such complexity.

### Shell Coverage and Assumptions
- Primarily designed around bash on Linux.
- POSIX `sh` layer is supported via inheritance, but other shells (zsh, fish, etc.) are not first-class citizens.
- Some logic around `$ENV` / `$BASH_ENV` and remote shells may be incomplete or brittle.

### Architecture and Implementation
- Multiple layers of indirection (generation, symlinks, runtime directory) that can be confusing.
- Generated files must be manually regenerated after config changes.
- Limited introspection and debugging support ("what is actually active?").
- The original `invoke` / task-oriented code in `tasks/` appears to be development tooling rather than part of the delivered product.
- Code quality and structure reflect its origins as a personal extraction; not yet refactored for maintainability at larger scale.

### Documentation and Onboarding
- User documentation exists and is opinionated, but is tied to the current (imperfect) configuration model.
- No formal specification of the configuration format or module contract.
- Diagrams exist for the problem space but may need updating.

### Process and Packaging
- Versioning has been informal (recently normalized).
- No automated tests visible at a quick glance.
- Packaging is basic setuptools with entry points.
- The project has not been exercised as a multi-contributor or AI-assisted codebase before the creation of `design/`.

## Decisions Made Regarding These Limitations

- We are **documenting** them explicitly rather than immediately fixing them.
- Future changes will be guided by Architecture Decision Records.
- We will establish principles (see `goals.md`) so that improvements are made consistently rather than opportunistically.
- The creation of the `design/` folder itself is the first step in shifting from "personal prototype" to "treat like a serious project."

## Rationale for Capturing This Now

When using AI coding agents on larger projects, it is critical that they (and human developers) understand:
- What the system is *trying* to be.
- Where it currently falls short.
- Which imperfections are intentional pragmatic choices vs. accidental debt.

This ADR serves as a baseline. Subsequent ADRs or design documents can reference it when proposing changes.

## Consequences

- Any refactoring or feature work should be able to point back to this document to justify why certain areas need attention.
- It sets expectations that the current implementation is not the final word on configuration representation, architecture, or scope.
- It provides a clear "before" picture against which future improvements can be measured.

## Related Decisions

- All other ADRs in this directory (they describe the "why" behind current choices).
- Future ADRs will likely address specific items listed here (e.g., configuration system redesign, test strategy, shell portability).

## References

- README.org (acknowledgments of temporary approaches)
- `docs/example_config.py`
- Git history (pragmatic, iterative development)
- This `design/` folder as a whole
