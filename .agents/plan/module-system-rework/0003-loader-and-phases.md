# Step 0003: Generated loader and phases

**Status**: Not started — execution pending explicit user request

**Dependencies**: 0002 (resolved module/slot lists exist)

## Context

Current templates are per-category `for lib in $libs` loops. ADR-0009: interactive envs run before prompt; no post-prompt; `PROMPT_COMMAND` wrappers lose. mise activate **must** live after prompt.

Keep generation (ADR-0004). Change what is generated: a small `bimhaw_load` plus phase scripts.

## Concrete actions

1. Put POSIX helpers in tool-owned `env.sh` (or a generated `runtime.sh` sourced from it): `bimhaw_have`, `bimhaw_log`, `bimhaw_is_login`, `bimhaw_is_interactive`, `bimhaw_load`.
2. `bimhaw_load module slot` sources `lib/<module>/<shell>/<file>` if present, skips if already loaded, logs if missing when the manifest declared it (should have failed at gen).
3. Rewrite templates so each phase is one call sequence, not a unique loop:
   - sh login: env (login) → funcs
   - sh interactive: aliases → prompt → post-prompt
   - bash login: sh login + bash env/funcs (inheritance)
   - bash interactive: sh interactive pieces as today + bash aliases/funcs/env-interactive? → prompt → **post-prompt** → autocomplete
   - logout: logout slot
4. **Always generate an empty post-prompt script** so users can add a mise module without a template bump.
5. `bimhaw_have`: do not treat a mise shim as a real binary (see 0004). A stub that uses `command -v` is acceptable only until 0004.
6. Preserve `$ENV` / `$BASH_ENV` behavior of current dotfiles unless an ADR says otherwise. Do not expand shell coverage.
7. Generated files remain auditable (comments listing module names per phase).

## Expected artifacts

- Updated Jinja under `src/bimhaw/profile_templates/`
- Runtime helpers in `env_script/`
- `profile.py` rendering phase membership from resolver output

## Verification

- Generated `interactive.bash` sources prompt then post-prompt then autocomplete (order test / snapshot).
- Empty post-prompt is present for a profile with no such modules.
- sh files of a module load before bash files of the same module.

## Notes

Do not implement cwd watching. Do not eval `mise activate` in templates; only provide the phase a user module will use.
