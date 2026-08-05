# ADR-0008: CLI Entry Points and Initial User Workflow

**Status**: Accepted (Current State)

**Date**: 2026-07-28 (documented retrospectively)

**Deciders**: Original author (Samuel D. Lotz)

## Context

To use bimhaw, a user must perform several distinct operations:

1. Initialize a bimhaw-managed area in their home (or point to external config).
2. Edit their configuration (`config.py` + modules in `lib/`).
3. Generate the concrete shell scripts for one or more profiles.
4. Activate a profile.
5. Replace their traditional shell dotfiles with bimhaw-managed versions (once).

These operations are not all the same kind of activity:
- Initialization is a one-time (or rare) setup step.
- Generation and activation are frequent during normal use.
- Dotfile linking is a privileged, one-time, potentially destructive operation.

## Decision

The project provides **two separate console entry points**:

- `bimhaw` — The main user CLI for ongoing operations:
  - `bimhaw profile gen`
  - `bimhaw profile load`
  - `bimhaw current`
  - `bimhaw link-shells`
  - Other profile-related and query commands

- `bimhaw_init` — A dedicated entry point for the one-time initialization of the `~/.bimhaw` directory and wiring it to user configuration locations.

This separation is reflected in `setup.py`:

```python
entry_points={
    'console_scripts' : [
        'bimhaw = bimhaw.cli:program.run',
        'bimhaw_init = bimhaw.init:cli',
    ],
},
```

The normal workflow after initial setup is:
1. Edit `config.py` / modules
2. `bimhaw profile gen --name <profile>`
3. `bimhaw profile load --name <profile>` (or equivalent)
4. Open new shells to pick up the active profile

## Rationale

- Initialization is conceptually different and potentially more interactive or one-shot.
- Separating `bimhaw_init` makes it harder to accidentally re-initialize or clobber an existing setup.
- The main `bimhaw` command can focus on the profile lifecycle and common operations.
- This mirrors patterns in other tools where setup vs daily use have different interfaces.

## Consequences

**Positive**:
- Clear separation of concerns in the user interface.
- `bimhaw_init` can evolve independently (e.g., become more wizard-like) without complicating the main CLI.
- Reduces risk of destructive operations being too easily accessible.

**Negative / Trade-offs**:
- Two commands to remember (though `bimhaw_init` is rarely used after setup).
- The current CLI implementation (using Click for the main program) and the init CLI may have different styles and levels of polish.
- Documentation must clearly explain when to use which command.

## Related Decisions

- ADR-0005: Runtime Directory Separation (initialization sets up the mapping)
- ADR-0006: Symlink Indirection (link-shells is part of the one-time setup)

## References

- `setup.py` entry points
- README.org workflow description
- `src/bimhaw/cli.py` and `src/bimhaw/init.py` (high-level structure only)
