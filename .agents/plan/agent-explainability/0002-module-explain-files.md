# Step 0002: Per-module explanation files

**Status**: Not started — execution pending explicit user request

**Dependencies**: 0001; richer on module-system layout (v2 `explain.md` in package dir)

## Convention

**v2 (canonical):** `lib/<module>/explain.md` plus optional `summary` in `module.toml`.

**v1 fallback** (until migrate):

- `lib/<shell>/<category>/<name>.explain.md` beside the script, or
- `lib/explain/<name>.md`

Pick **one** v1 fallback in implementation and document it. Prefer beside-the-script so migrate can move it with the file.

## Content rules (skill + docs, not a schema)

- What the module changes (PATH, aliases, PS1, completions)
- Side effects / order needs (`after`)
- Whether it assumes a **global** tool (mise-safety)
- No secrets

## Concrete actions

1. `bimhaw explain module <name>` appends `explain.md` if found, else says how to add one.
2. Teach `bimhaw-write-module` (module-system 0005) to create a stub `explain.md`.
3. Doctor (when it exists) **warns** only if the **prompt** module has no explain file (PS1 is the paste surface). Other modules stay silent.

## Expected artifacts

- Resolver for explain files
- Fixture module with explain.md in tests

## Verification

- Missing file → not an error
- Present file appears in md output under a heading
