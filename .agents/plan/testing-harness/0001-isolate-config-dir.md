# Step 0001: Isolate CONFIG_DIR for tests

**Status**: Not started — execution pending explicit user request

**Dependencies**: None on pytest yet; this is the only product `src/` change allowed before characterization tests.

## Context

`src/bimhaw/__init__.py` sets `CONFIG_DIR` to `$HOME/.bimhaw` at import. `src/bimhaw/config.py` immediately `exec`s that path. Any `import bimhaw.config` against a developer machine is unsafe and unreproducible.

This is **testability**, not the module makeover. Keep the default identical for users.

## Concrete actions

1. Honor `BIMHAW_DIR` (or equivalent) when resolving `CONFIG_DIR`. Expand user/vars after reading the env.
2. Replace module-level `exec(open(config_path))` with `load_config(path=None)` that:
   - defaults to `CONFIG_DIR/config.py`
   - `exec`s into a dict or namespace
   - assigns the expected module globals (`PROFILES`, `SH_LOGIN_ENVS`, …) for current CLI
3. CLI and `profile.py` keep working with no user-visible change when `BIMHAW_DIR` is unset.
4. `env.sh` currently hardcodes `HOME/.bimhaw`. For tests that source generated scripts, either:
   - generate/test with a patched env.sh, or
   - make `env.sh` respect `BIMHAW_DIR` if already set, else default. Prefer: `BIMHAW_DIR="${BIMHAW_DIR:-$HOME/.bimhaw}"` so isolation works in shell tests too.
5. Do not change template module lists, profile dicts, or CLI verbs.

## Expected artifacts

- `CONFIG_DIR` / `BIMHAW_DIR` override
- `load_config()`
- `env.sh` respects existing `BIMHAW_DIR`

## Verification

- Unset env: behavior matches today (manual or a later test).
- Set `BIMHAW_DIR` to a tmp path: `bimhaw.config` does not read `~/.bimhaw`.
- No writes to `$HOME` in this step.

## Risk

`env.sh` is copied into `~/.bimhaw` at **init**, not sourced from the package at runtime (init writes it once). Changing the packaged `env.sh` does not update existing user dirs. Acceptable; tests use init or write their own `env.sh`. Document that existing installs keep the old one-liner until re-init.
