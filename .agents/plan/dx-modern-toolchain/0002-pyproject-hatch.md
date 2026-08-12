# DX Step 0002: Add `pyproject.toml` with hatchling

**Status**: Not Started

**Dependencies**: 0001 (mise provides `uv` for later build verification; packaging file can be written without uv, but verify with mise-activated `uv`)

## Context

Packaging is setuptools-only via `setup.py` + `MANIFEST.in`. Metadata, dependencies, and scripts must move to PEP 621 + hatchling so **uv** (installed via mise) can build/publish consistently. Package data under `src/bimhaw/` (templates, shell_dotfiles, env script, profile config) must keep shipping.

## Concrete actions

1. Read current `setup.py`, `MANIFEST.in`, `_version.py`, package tree under `src/bimhaw/` (non-Python assets).
2. Create root `pyproject.toml` with:
   - `[build-system]`: `requires = ["hatchling"]`, `build-backend = "hatchling.build"`
   - `[project]`: name, description, license MIT, authors, requires-python (conservative honest floor), classifiers, urls
   - `[project.dependencies]`: `jinja2`, `click`, and **`invoke` (still runtime for product CLI)**
   - `[project.scripts]`:
     - `bimhaw = "bimhaw.cli:program.run"`
     - `bimhaw_init = "bimhaw.init:cli"`
   - Dependency groups deferred detail to step 0003 (uv groups)
   - `[tool.hatch.version]`: single source — path/regex on `src/bimhaw/_version.py` **or** static once aligned
   - `[tool.hatch.build.targets.wheel]` / sdist: ensure package data included
3. Unify version: pick `_version.py` as canonical (or hatch version); stop triple-defining versions.
4. Remove or stop using `setup.py` as source of truth (prefer delete after `uv build` verified in later step).
5. Keep `MANIFEST.in` only if still required; prefer hatch config and delete when redundant.
6. Do **not** delete `tasks/` yet. Do **not** change product CLI code except entry-point string if required.
7. No hatch env configuration — uv remains the env tool (under mise).

## Expected artifacts

- `pyproject.toml` (complete enough to build)
- Version single-sourced
- Notes on package-data mapping for templates/dotfiles

## Verification

- `summarize pyproject.toml`
- Under mise-activated shell: `uv build` (step 0003+) and inspect wheel contents for non-Python data
- Confirm scripts table matches current entry points

## References

- Current `setup.py`, `MANIFEST.in`, `src/bimhaw/_version.py`
- hatchling metadata / version / build target docs (cache if fetched)
- Step 0001 mise (uv on PATH)
