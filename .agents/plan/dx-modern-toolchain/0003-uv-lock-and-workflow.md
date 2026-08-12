# DX Step 0003: uv workflow and lockfile (via mise)

**Status**: Not Started

**Dependencies**: 0001 (mise installs uv), 0002 (`pyproject.toml` exists)

## Context

Today installs are loose `pip install -r requirements*.txt` plus editable `-e .`. **uv** should own Python env creation, locking, running tools, building, and publishing. uv itself is **installed and version-pinned by mise**, not by a random host bootstrap.

Shell env vars that affect uv/publish come from **mise** `[env]` / `.mise.local.toml`, not from a checked-in `env.bash`.

## Concrete actions

1. Ensure shell is mise-activated (`mise install` + activate) so `uv` matches `.mise.toml`.
2. Define dependency groups in `pyproject.toml` (uv `[dependency-groups]`), e.g.:
   - project deps: click, jinja2, invoke (runtime CLI)
   - `dev`: optional interactive debug (ipython, pdbpp) — keep minimal
   - Do **not** re-add invoke as a “task runner” dev dep; do **not** port jubeo env.make/pin flows
3. Decide Python pin approach and document in contributing later:
   - Default: `uv python` pin / `.python-version` if needed, coordinated with `requires-python`
   - Avoid also pinning python in mise unless deliberately chosen in step 0001
4. Generate `uv.lock` via `uv lock` / `uv sync`.
5. Document canonical commands (all assume mise tools on PATH):
   - `uv sync` — create/sync `.venv` + editable project
   - `uv run bimhaw …` / `uv run bimhaw_init …`
   - `uv build`
   - `uv publish` (+ TestPyPI; tokens via mise local env, not committed files)
6. Retire as **sources of truth**:
   - `requirements.txt`
   - `dev.requirements.txt`
   - `tools.requirements.txt`
7. Update `.gitignore` for `.venv/`, uv caches; keep **`uv.lock` tracked**.
8. Drop bumpversion/twine/wheel from the “must install” story — uv/hatch replace that path.
9. If any non-secret `UV_*` defaults help the project, add them to `.mise.toml` `[env]` (step 0001 file); secrets only in `.mise.local.toml`.

## Expected artifacts

- `uv.lock` (committed)
- Updated `pyproject.toml` groups
- Removal or demotion of loose requirements files
- `.gitignore` tweaks if needed
- Alignment notes with mise env for publish-related vars

## Verification

- `mise which uv` points at mise-managed binary
- `uv sync` succeeds
- `uv run python -c "import bimhaw; print(bimhaw.__version__)"`
- `uv run bimhaw` / help path works (invoke still runtime)
- `uv build` produces sdist + wheel

## References

- uv project docs; steps 0001–0002
- Old `dev.requirements.txt` for what *not* to cargo-cult
