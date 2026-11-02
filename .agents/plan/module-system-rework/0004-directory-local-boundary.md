# Step 0004: Directory-local boundary (mise / direnv)

**Status**: Not started — execution pending explicit user request

**Dependencies**: 0003 (post-prompt phase exists); research note

## Context

See [research-mise-directory-local.md](research-mise-directory-local.md) and the plan README “Directory-local tools” section.

v2 default is **strict layering**. bimhaw does not parse `mise.toml`. It must (1) make activate *possible* in the right phase, (2) make static global autocomplete *honest*, (3) warn on known footguns.

## Concrete actions

1. Document in user-facing docs (when 0009-style doc updates happen) and in skills (0005):
   - Interactive: user module in `post_prompt` runs `eval "$(mise activate bash)"` (absolute path to mise if needed).
   - Never mise activate + direnv hook in the same profile.
   - Never `source <(tool completion bash)` in bimhaw for tools listed in project `mise.toml`.
   - Project-only shell snippets → mise `[hooks.enter] script`, not bimhaw lib.
   - Project recipes / agents in-repo → `mise exec` (already DX policy); unrelated to this product hook.
2. `bimhaw_have` (from 0003): if `command -v` hits a path under mise shims (`$MISE_SHIMS` / `~/.local/share/mise/shims`), treat as **not** a stable global install; log debug. Do not auto-install via shim.
3. Doctor checks (can land with 0007; specify them here so 0007 implements):
   - Both `direnv hook` and `mise activate` appear in generated/sourced post-prompt files → error/warn.
   - Static autocomplete slot files whose names match common mise-managed CLIs (`node`, `python`, `kubectl`, `rg`, `uv`, …) → warn “may be stale under directory-local tools.”
   - `eval "$(mise activate … --shims)"` in interactive profile → warn that `[env]` and packslip completions will not follow cd.
   - Duplicate mise activate (env slot *and* post-prompt) → warn.
4. Do **not** ship a `lib/mise` module. A skill (0005) may contain an *example snippet* clearly marked as copy-paste into the user’s lib.
5. Do **not** implement `bimhaw_complete_lazy` as a product feature. Optionally mention the pattern in the research note / skill as future.

## Expected artifacts

- Helper behavior for shims
- Doctor rules specified (implemented in 0007 if doctor is not yet built)
- Docs pointers (implementation of prose may wait for a docs step)

## Verification

- Unit test: `bimhaw_have` with PATH containing a fake shims dir.
- Snapshot or string test: generated post-prompt does not itself contain `mise activate` unless a **user** module does (templates stay empty).

## Explicit non-actions

- No cwd hook in bimhaw
- No packslip client
- No `.bimhaw/` overlay inside git projects
- No supporting direnv `use mise` (deprecated upstream)
