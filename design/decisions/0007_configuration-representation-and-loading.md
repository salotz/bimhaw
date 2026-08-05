# ADR-0007: Configuration Representation and Loading via Python exec()

**Status**: Accepted (Current State) — Acknowledged as Temporary

**Date**: 2026-07-28 (documented retrospectively)

**Deciders**: Original author (Samuel D. Lotz)

## Context

The tool needs a way for users to declare:
- The set of profiles
- For each profile, which modules belong in which categories
- Distinctions for sh vs bash, login vs non-login, interactive vs non-interactive in some cases
- Prompt choices

The original implementation chose to express this directly in Python as a `config.py` file containing a large number of dictionaries (one per category/mode combination). This file is loaded at runtime using `exec()`.

This approach was chosen for rapid development and because the author was already comfortable expressing configuration in Python.

## Decision

- User configuration lives in a single `config.py` file.
- The file is expected to define a set of top-level variables (e.g. `PROFILES`, `SH_LOGIN_ENVS`, `BASH_NONLOGIN_ENVS`, `SH_PROMPT`, etc.).
- Loading is performed via `exec(open(config_path).read())` in the appropriate context.
- The structure is flat and explicit: each category and mode combination has its own dictionary mapping profile name → list of module names (or special values like prompt names).

The author explicitly documented this as a pragmatic, temporary solution.

## Rationale

- Python is already the implementation language; using it for configuration avoids introducing a new DSL or parser.
- Explicit dictionaries are simple to understand and grep.
- `exec()` was the fastest way to get a working prototype that could be edited directly by the author.
- It allows the configuration to contain arbitrary Python expressions if needed (though this is not heavily used).

## Consequences

**Positive**:
- Very flexible in the short term.
- No additional parser or schema to maintain initially.
- Easy for the original author to evolve the configuration shape quickly.

**Negative / Trade-offs**:
- Verbose and repetitive: many similar dictionaries must be maintained.
- Error-prone: typos in profile names or module names are only caught at generation time or runtime.
- Security / safety concerns with `exec()` of user-controlled files (mitigated by the fact that it is the user's own config).
- Hard to validate, provide IDE support, or offer good error messages.
- Difficult to support advanced features like profile inheritance or DRY configuration without extending the representation.
- The "temporary" nature has persisted, creating technical debt.

## Related Decisions

- ADR-0002: Profiles as Primary Unit (the dictionaries are keyed by profile)
- ADR-0003: Modular Layers (separate dictionaries for sh vs bash)
- Future work will likely involve replacing or layering a better configuration representation on top of or instead of raw `exec()`.

## References

- README.org: "Uses Python `exec` (explicitly noted as a temporary approach)"
- `docs/example_config.py` (canonical example of the current shape)
- `src/bimhaw/profile_config/config.py` (loading logic)
- `src/bimhaw/config.py`
