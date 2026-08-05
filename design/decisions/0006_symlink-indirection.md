# ADR-0006: Use of Symlinks for Profile Activation and Dotfile Replacement

**Status**: Accepted (Current State)

**Date**: 2026-07-28 (documented retrospectively)

**Deciders**: Original author (Samuel D. Lotz)

## Context

To support profile switching without modifying the user's primary dotfiles on every switch, and to allow the tool to control the actual startup scripts, some form of indirection is required between:

- The user's real `$HOME` dotfiles (`.profile`, `.bashrc`, etc.)
- The currently selected profile's generated scripts
- The tool's generated content in `~/.bimhaw`

Directly overwriting dotfiles on each switch would be destructive and error-prone. Embedding the active profile name inside the dotfiles would require regenerating them on every switch.

## Decision

bimhaw uses **symlinks** at two levels:

1. **Profile activation**: `~/.bimhaw/active` is a symlink pointing to the directory of the currently active profile (e.g. `~/.bimhaw/profiles/bimhaw`).

2. **Dotfile replacement**: The user's traditional dotfiles are replaced (via `bimhaw link-shells`) with symlinks pointing into `~/.bimhaw/shell_dotfiles/`.

The files in `shell_dotfiles/` contain the logic to source the appropriate generated script from the `active` profile directory, taking into account login vs non-login and `$BASH_ENV` / `$ENV` cases.

## Rationale

- Symlinks provide lightweight, atomic switching of the active profile (just change one symlink).
- Replacing the real dotfiles with symlinks once (during initial setup) means subsequent profile changes do not touch `$HOME` dotfiles again.
- This supports the "generation" model: the dotfile wrappers can be updated by the tool without the user having to re-link every time.
- It makes the runtime directory the single point of control for what is currently active.

## Consequences

**Positive**:
- Profile switching is fast and safe.
- User's actual dotfiles in `$HOME` become stable pointers after initial linking.
- Clear separation between "what the shell sees" and "what the user edits."

**Negative / Trade-offs**:
- Requires an explicit one-time linking step (`bimhaw link-shells`).
- Users must back up existing dotfiles before linking (documented in README).
- Symlinks can be confusing or break if the target is moved or deleted.
- Some tools or environments may not follow symlinks as expected (rare but possible).
- Debugging can require following multiple layers of links.

## Related Decisions

- ADR-0004: Generation and Templates
- ADR-0005: Runtime Directory Separation
- ADR-0002: Profiles as Primary Unit

## References

- README.org: "linking libs to profiles", "bimhaw link-shells"
- `src/bimhaw/shell_dotfiles/` (the template dotfiles)
- `src/bimhaw/init.py` and profile loading commands
