# Step 0007: Introspection — doctor, module list, profile show

**Status**: Not started — execution pending explicit user request

**Dependencies**: 0002–0004 (there is something true to report)

## Context

ADR-0009: weak “what is actually active?” Generation + symlinks are survivable only with introspection. Bash-it’s `doctor` is the operability borrow; there is no enable/disable catalogue.

## Concrete actions

1. `bimhaw module list` — scan user `lib/`, print name, slots, shells, manifest errors.
2. `bimhaw profile show [--name]` — resolved modules after extends; files that will be sourced per phase; options.
3. `bimhaw doctor`:
   - `~/.bimhaw` exists, `active` symlink target, config path (real vs symlink)
   - generated profile hash vs current resolver output (stale gen)
   - shell dotfile symlinks point at bimhaw
   - missing slot files
   - directory-local rules from 0004
4. Keep output grep-friendly (no only-TUI).
5. No network, no `mise doctor` wrapper required; if `mise` is on PATH, optionally note `mise doctor` as a hint (do not parse it).

## Expected artifacts

- CLI commands + tests with fixtures

## Verification

- Stale gen is detected after editing config without gen.
- Duplicate mise activate warning fires on a fixture profile.
