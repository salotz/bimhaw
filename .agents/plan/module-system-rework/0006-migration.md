# Step 0006: Migrate v1 lib and config

**Status**: Not started — execution pending explicit user request

**Dependencies**: 0002 (new layout/schema exist)

## Context

Real user config lives outside the repo (e.g. `~/.salotz.d` lib + config.py). The makeover fails if those trees must be rewritten by hand without a mechanical mapping.

v1: `lib/sh/aliases/git.sh` + name `git` in `SH_ALIASES`.  
v2: `lib/git/module.toml` + `lib/git/sh/aliases.sh`.

## Concrete actions

1. `bimhaw migrate lib [--from] [--to] [--dry-run]`:
   - Walk old `LIB_DIRS`.
   - Group files by stem (`git.sh`, `git.completion.bash` → module `git`).
   - Write `module.toml` with detected `shells` and `slots`.
   - Move/copy files to new paths. Do not delete old tree unless `--delete-old`.
   - Collision: two different categories already using different identities — keep separate modules (`git` vs `git-completion` only if stems differ).
2. `bimhaw migrate config`:
   - Read old 14 dicts.
   - For each profile, union of names → `modules` list (stable order: env, funcs, aliases, prompt, autocomplete, logout as first seen).
   - Prompts become `prompt` field.
   - Emit new `PROFILES` mapping; write beside old file or `--in-place` with backup.
   - Login vs nonlogin env lists that differ: put those module names in the module’s manifest `slots` still as `env` and **warn** that v2 env is idempotent and always loaded on both paths; user must split modules if they truly need login-only (rare; keychain-on-GUI was the old comment in `login.bash.j2`). Capture that as a migrate warning, not a new config axis, unless an ADR reintroduces a `login_only` slot flag.
3. Dual-read: only if migrate cannot be one-shot. Prefer fail-fast with message to run migrate.
4. Document the GUI-login keychain case: a module can test `bimhaw_is_login` / SSH/GUI itself rather than a separate config list.

## Expected artifacts

- migrate subcommands
- Tests with a fixture mini-lib and example_config.py

## Verification

- `docs/example_config.py` (old) converts to a new PROFILES that lists the same stems.
- Round-trip not required; new config is the source after migrate.
