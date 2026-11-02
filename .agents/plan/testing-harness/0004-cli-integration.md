# Step 0004: CLI integration against isolated dir

**Status**: Not started — execution pending explicit user request

**Dependencies**: 0001–0002; product CLI still invoke-based

## Concrete actions

1. Invoke `bimhaw.init.initialize(config=..., lib=...)` or `bimhaw_init` via `uv run` with `BIMHAW_DIR` set — prefer calling the Python API to avoid PATH/entry-point noise, plus one subprocess test of the console script if cheap.
2. Assert created layout: `shell_dotfiles/{profile,bash_profile,bashrc,bash_logout}`, `lib/` + `LIB_DIRS`, `config.py`, `env.sh`, `profiles/`.
3. `--lib` / `--config` create symlinks, not copies.
4. `profile gen` / `profile load` / `profile ls` / `current` against fixture config:
   - unknown profile → error
   - load updates `active` symlink target
   - gen writes `profiles/<name>/shells/...` and links `lib`
5. **Do not** run `link-shells` against the real home. If tested, only with `HOME=tmp_path` and assert four symlinks under that fake home.
6. Subprocess tests must pass `env` with `BIMHAW_DIR` and a copy of `PATH` that includes `uv run`’s scripts, without inheriting a real `BIMHAW_DIR` from the operator.

## Expected artifacts

- `tests/test_cli/`

## Verification

- Isolated; real `~/.profile` unchanged (optional assert).
