# DX Step 0004: Add `justfile` (task runner only)

**Status**: Not Started

**Dependencies**: 0001 (mise provides `just` + `uv`), 0003 (uv commands known)

## Context

Maintainer orchestration today is invoke + `tasks/` (jubeo). Replace with **just**, scoped strictly to running tasks — thin recipes over `uv` and shell cleans. **just and uv are installed via mise**.

**Invocation policy (see DX README):**

- Operators may use `mise activate` / shims / bare PATH — **their choice**.
- **In-repo tooling must not assume activation.** Prefer either:
  1. Documented entrypoint: always `mise exec -- just <recipe>`, and recipes call bare `uv` only because they already run *under* `mise exec -- just` (just inherits mise’s tool env when launched that way), **or**
  2. Recipes themselves call `mise exec -- uv …` so even `just build` with a system just still hits pinned uv.

**Default for this plan:** document and use **`mise exec -- just …`** as the public entrypoint; inside the justfile, call `uv` / `git` / `rm` normally **when** just was started via `mise exec -- just` (mise sets up tool PATH for the child). For defense in depth, recipes may use `mise exec -- uv …` if we want bare system-`just` to still work — prefer the simpler form first and note the entrypoint requirement in contributing.

just does not install tools or own env vars (mise does).

## Bare-minimum recipes (only these)

| Recipe | Intent | Implementation sketch |
|--------|--------|------------------------|
| `clean` | Remove build artifacts + caches + editor junk | rm -rf dist build *.egg-info …; find `*~` |
| `build` | Build sdist + wheel | `uv build` (under `mise exec -- just`) **or** `mise exec -- uv build` |
| `publish-test` | Upload to TestPyPI | `uv publish` + test index (tokens from mise env / `.mise.local.toml`) |
| `publish` | Upload to PyPI | `uv publish` (no broken umbrella tag+publish magic) |
| `tag version=…` | Annotated release tag | `git tag -a v{{version}} -m '…'` |
| `help` / default | List recipes | `just --list` |

Optional tiny helpers (only if useful):

- `sync` → `uv sync`
- `version` → print canonical version via `uv run`
- `tools` → `mise install` / `mise ls` (optional QoL; do not duplicate mise UX)

## Explicitly do **not** add

- test/lint/docs/sphinx/website/benchmark recipes
- conda/venv jubeo `env.make` / pip-compile flows
- mise `[tasks]` clones of every recipe (one task runner: just)
- umbrella “release” that fails half-way (old `py.publish` / `py.release` bugs)
- Requirements that the operator has run `mise activate`

## Concrete actions

1. Add root `justfile` with the recipes above; set `set shell` if needed for portability.
2. Prefer calling `uv` rather than raw `python setup.py` / twine.
3. Document public entrypoint: **`mise exec -- just <recipe>`** after `mise install` (activate not required).
4. Completions / activate: optional operator QoL only; primary project story is `mise exec`.
5. Publish recipes should rely on env vars supplied by mise when using `mise exec` (e.g. token in `.mise.local.toml`), documented in step 0006 — not hard-coded secrets.
6. Keep recipes boring and readable.
7. Capture “writing project tooling” rule in contributing (step 0006): any new script/CI step that needs uv/just goes through `mise exec`.

## Expected artifacts

- `justfile` at repo root
- No new Python packaging under `tasks/`
- No mise `[tasks]` block required
- Docs entrypoint = `mise exec -- just …`

## Verification

- **Without** `mise activate`: `mise exec -- just --list`
- `mise exec -- just clean` then `mise exec -- just build`
- Confirm no dependency on `inv` or `tasks/`
- `mise which just` resolves

## References

- DX README “Invocation policy”
- Structure plan step 0003 bare-minimum surface
- just documentation; mise exec
