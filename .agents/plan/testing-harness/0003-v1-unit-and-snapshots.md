# Step 0003: v1 unit tests and generation snapshots

**Status**: Not started — execution pending explicit user request

**Dependencies**: 0002

## Context

Lock current `profile.py` + Jinja output **before** module-system 0002/0003 rewrite templates.

## Concrete actions

1. Unit tests for `get_profile_data` / `format_profile_data` (string quoting, space-joined lists, `NONE_PROFILE` when prompt is `None`).
2. `gen_profile` returns the expected script names (`SH_TEMPLATES` / `BASH_TEMPLATES` minus `.j2`).
3. `write_profile` into `tmp_path`: files exist; `lib` linking is CLI-side — unit test only writes scripts.
4. Snapshot or stable substring tests:
   - bash interactive: sources sh funcs, sh aliases, sh nonlogin_env, then bash interactive envs loop, then prompt, then autocomplete. **No** post-prompt file sourced (v1 fact).
   - bash login: sources sh login, then `bash_login_sh_envs` / `bash_login_bash_envs` loops, then bash funcs.
   - sh login: sets `ENV=` to interactive.sh, sources funcs, login_env.
5. Prefer substring/order assertions over huge golden files if Jinja whitespace is noisy; if using goldens, store under `tests/snapshots/` and require an explicit regen comment.

## Expected artifacts

- `tests/test_unit/` and `tests/test_generation/`
- Snapshots optional

## Verification

- Tests fail if someone inserts post-prompt **without** updating assertions (this is desired: 0003 of the module rework must update these).
