# Step 0002: New lib layout and profile schema

**Status**: Not started — execution pending explicit user request

**Dependencies**: 0001 (ADRs frozen); **[testing-harness gate](../testing-harness/0006-gate.md)** (v1 characterization green)

## Context

Today `LIB_DIRS` is a list of category folders and `get_profile_data()` reads 14 global dicts. Generation cannot start until identity of a module and shape of a profile are loadable and validatable.

This step is **data model only**: accept the new layout and config, emit the same *kind* of profile_data the old templates understand *or* a parallel structure. Prefer not to rewrite every Jinja file here; a shim that still produces list-of-names per slot is acceptable so 0003 can own the loader.

## Concrete actions

1. Define on-disk module layout (`lib/<name>/{module.toml,sh/,bash/}`) and allowed slot filenames. Document in design + init scaffolding.
2. Change `init` to create the new empty skeleton (not old `sh/aliases` etc.), or create both during migration window (prefer new-only + migrate command in 0006).
3. Replace `profile_config/config.py` default with the `PROFILES = { name: {extends, modules, prompt, options} }` shape.
4. Implement load + schema validation (dataclasses or pydantic). Unknown module names, missing manifests, missing declared slot files, cycles in `extends` / `after` → hard error at gen time.
5. Resolver: flatten `extends`, apply exclude/reorder rule (as ADR’d), produce an ordered module list and per-slot file lists.
6. Keep `exec()` of user `config.py` if that is the ADR, but **only** after validation.
7. Do not invent a module catalogue or extra search path.

## Expected artifacts

- Schema / resolver code
- New default config stub
- Init scaffolding for new `lib/`
- Tests for resolver (extends, exclude, missing module, sh-inheritance file pick)

## Verification

- A tiny fixture lib with two modules and `extends` resolves to the expected slot file lists.
- Old 14-dict config fails with a migration pointer (or is still accepted only if 0006 dual-read is explicitly chosen — default: reject).

## Notes

Prompt sugar: `"prompt": "salotz-dark"` means that module is included in the prompt phase even if omitted from `modules`. Do not keep a parallel `BASH_PROMPT` dict.
