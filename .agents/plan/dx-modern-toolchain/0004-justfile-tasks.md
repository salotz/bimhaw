# DX Step 0004: Add `justfile` (task runner only)

**Status**: Not Started

**Dependencies**: 0001 (mise provides `just` + `uv`), 0003 (uv commands known)

## Context

Maintainer orchestration today is invoke + `tasks/` (jubeo). Replace with **just**, scoped strictly to running tasks — thin recipes over `uv` and shell cleans. **just is installed via mise**; recipes assume a mise-activated environment (PATH + env vars). just does not install tools or own env vars.

## Bare-minimum recipes (only these)

| Recipe | Intent | Implementation sketch |
|--------|--------|------------------------|
| `clean` | Remove build artifacts + caches + editor junk | rm -rf dist build *.egg-info …; find `*~` |
| `build` | Build sdist + wheel | `uv build` |
| `publish-test` | Upload to TestPyPI | `uv publish` with test index (tokens from mise local env) |
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
- mise task clones of every recipe (one task runner: just)
- umbrella “release” that fails half-way (old `py.publish` / `py.release` bugs)

## Concrete actions

1. Add root `justfile` with the recipes above; set `set shell` if needed for portability.
2. Prefer calling `uv` rather than raw `python setup.py` / twine (uv from mise PATH).
3. Document that contributors run `mise install` + activate **before** `just …`.
4. Completions: optional `just --completions bash`; primary shell integration is **mise activate** (replaces `env.bash`).
5. Publish recipes should rely on env vars supplied by mise (e.g. token in `.mise.local.toml`), documented in step 0006 — not hard-coded secrets.
6. Keep recipes boring and readable.

## Expected artifacts

- `justfile` at repo root
- No new Python packaging under `tasks/`
- No mise `[tasks]` block required

## Verification

- mise-activated shell: `just --list`
- `just clean` then `just build`
- Confirm no dependency on `inv` or `tasks/`
- `mise which just` resolves

## References

- Structure plan step 0003 bare-minimum surface — command names are just/uv under mise
- just documentation; mise activation
