# DX Step 0002: Add `pyproject.toml` with hatchling

**Status**: Completed (2026-08-12)

**Dependencies**: 0001 (mise provides `uv` for build verification; packaging file can be written without uv, but verify with mise-activated `uv` → **`mise exec -- uv`**)

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
4. Remove or stop using `setup.py` as source of truth (prefer delete after `uv build` verified).
5. Keep `MANIFEST.in` only if still required; prefer hatch config and delete when redundant.
6. Do **not** delete `tasks/` yet. Do **not** change product CLI code except entry-point string if required.
7. No hatch env configuration — uv remains the env tool (under mise).

## Expected artifacts

- `pyproject.toml` (complete enough to build)
- Version single-sourced
- Notes on package-data mapping for templates/dotfiles

## Verification

- `summarize pyproject.toml`
- Under mise: `mise exec -- uv build` and inspect wheel contents for non-Python data
- Confirm scripts table matches current entry points

## Execution (2026-08-12)

### Artifacts
- **`pyproject.toml`** — hatchling backend; PEP 621 metadata; scripts; dynamic version from `_version.py`; wheel `packages = ["src/bimhaw"]`
- **`src/bimhaw/_version.py`** — normalized to PEP 440: `2020.3.6a0.dev0` (was invalid `2020-03-06a0.dev0`)
- **Removed** `setup.py` and `MANIFEST.in` after successful `uv build` (hatch is sole packaging SoT)
- **`tasks/`** untouched; product CLI untouched; runtime deps still include **invoke**

### Version
| Former | New |
|--------|-----|
| `setup.py` `0.1` | dropped |
| `_version.py` `2020-03-06a0.dev0` (not PEP 440) | **`2020.3.6a0.dev0`** via hatch path |

### Verify log
```text
mise exec -- uv build
→ dist/bimhaw-2020.3.6a0.dev0.tar.gz
→ dist/bimhaw-2020.3.6a0.dev0-py3-none-any.whl
```
Wheel contains:
- `bimhaw/shell_dotfiles/*` (bashrc, profile, …)
- `bimhaw/env_script/env.sh`
- `bimhaw/profile_config/config.py`
- `bimhaw/profile_templates/**/*.j2`
- entry points: `bimhaw`, `bimhaw_init`
- Requires-Dist: click, invoke, jinja2

### Notes
- `requires-python = ">=3.8"` conservative floor (no tighter claim in old metadata)
- No LICENSE file in repo — omitted from sdist include
- Dependency groups / `uv.lock` → step 0003
- `dist/` build products are gitignored (python template); not committed

## References

- Current packaging history: former `setup.py`, `MANIFEST.in`, `src/bimhaw/_version.py`
- hatchling metadata / version / build target docs
- Step 0001 mise (`mise exec -- uv`)
