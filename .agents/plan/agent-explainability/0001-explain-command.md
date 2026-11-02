# Step 0001: `bimhaw explain` CLI (v1)

**Status**: Not started — execution pending explicit user request

**Dependencies**: Testing-harness isolation (`BIMHAW_DIR`) if tests are added in the same change; otherwise CLI can land after harness gate. Does **not** require module-system 0002.

## Context

Agents and humans need a **generated** description of the *current* setup. Static docs go stale; `explain` reads live `BIMHAW_DIR` / config / active symlink.

v1 config is still the 14 dicts. Output lists those honestly. v2 resolver output is a later drop-in.

## Concrete actions

1. Subcommands under `bimhaw explain` (invoke collection, matching current CLI):
   - default: 15–30 line stack (what bimhaw is, `BIMHAW_DIR`, active profile, pointer to `explain prompt|profile|startup`)
   - `profile [name]` (default active)
   - `module <name>` (search lib paths; v1: find files named `<name>.*` in category dirs)
   - `startup` (prose + paths of generated scripts for this profile)
   - `prompt` stub that points at the prompt filename until 0003
2. `--format text|md` (md default).
3. Do not print env var **values**. Do not cat entire module source unless `--source`.
4. Tests: isolated dir fixture; `explain` mentions the fixture profile name.

## Expected artifacts

- CLI + tests
- Help text that agents can discover (`bimhaw explain --help`)

## Verification

- `BIMHAW_DIR=tmp mise exec -- uv run bimhaw explain` does not read `~/.bimhaw`
- Missing active symlink → clear error, not a traceback dump
