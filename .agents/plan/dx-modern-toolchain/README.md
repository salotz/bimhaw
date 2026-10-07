# Plan: Modern Developer Experience (mise + uv + hatch + just)

**Status**: In Progress — Steps 0001–0002 Complete; Remaining Execution Pending Explicit User Request

**Date**: 2026-08-10

**Owner**: AI-assisted work

**Related plans**: Structure/agent-guidelines upgrade (`.agents/plan/README.md`, steps 0001–0010). This is a **separate** plan series for packaging and maintainer DX.

## Purpose

Replace the legacy setuptools + invoke/jubeo maintainer stack with a small modern toolchain:

| Concern | From | To |
|---------|------|-----|
| Host tool installs + versions | ad-hoc system packages / “install uv and just yourself” | **mise** (`.mise.toml`) pins and installs **uv**, **just**, and related CLIs |
| Project / shell environment variables | undocumented, ad-hoc exports, old `env.bash` | **mise** `[env]` (+ gitignored `.mise.local.toml` for secrets) |
| Package metadata / build | `setup.py` + `MANIFEST.in` + loose requirements files | **hatch** (hatchling) via `pyproject.toml` |
| Python deps, lock, install, build, publish | ad-hoc pip + invoke `py.*` tasks | **uv** (provided via mise) |
| Maintainer task runner | **invoke** + `tasks/` (jubeo scaffolding) | **just** (`justfile`) — tasks only (just provided via mise) |
| Contributing docs surface | planned around `inv py.*` (structure step 0003) | document **mise** → **uv** / **just** instead |

### Layering (do not collapse these roles)

```
mise          → install/pin host CLIs (uv, just, …); project env vars
  uv          → Python version (as chosen), venv, lockfile, run, build, publish
  hatchling   → build backend only (pulled by uv when building) — not a second env manager
  just        → thin task recipes that call uv/git/rm — not a package manager
```

**mise does not replace just** for maintainer tasks (no competing task runners).  
**mise does not replace uv** for Python dependencies or publishing.  
**hatch envs are out of scope** — uv owns the Python env story.

### Invocation policy (project tooling vs operator shell)

| Who | How tools are run |
|-----|-------------------|
| **In-repo project tooling** (justfile, scripts, CI, agent-run commands, docs “copy-paste” happy path) | Call **`mise exec -- …`** (or equivalent) so pinned uv/just/env apply **without** requiring shell activation |
| **Operator interactive shell** | Optional: `mise activate` / shims / nothing — **operator choice**. Never required for project recipes to work |

Rationale: auto-activation is a personal shell preference. Internal tooling must not assume PATH was mutated by activate hooks.

Goals:

- One declarative project file for packaging (`pyproject.toml`) and one for host DX (`.mise.toml`).
- Reproducible **tool** versions via mise; reproducible **Python deps** via `uv.lock`.
- Thin `justfile` that only orchestrates commands (no Python task package).
- Delete jubeo `tasks/` and stop using invoke as a **dev** task runner.
- Keep the bare-minimum maintainer surface (clean, build, publish, tag) — do not revive tests/docs/env scaffolding that never existed in-repo.
- Clear story for env vars (committed defaults vs local secrets).

Non-goals (this plan):

- Migrating the **product** CLI off invoke (see “Runtime invoke” below).
- Adding a test suite, Sphinx, CI, or conda.
- Inventing a large release ceremony or multi-role contributor ladder.
- Changing bimhaw’s shell-profile product behavior.
- Using mise **tasks** as the primary task runner (just remains).
- Committing secrets (tokens) into `.mise.toml`.

## Runtime invoke (important scope boundary)

`invoke` is used in **two** places today:

1. **Dev task runner** — `tasks/` (jubeo). **In scope: remove.**
2. **Product CLI** — `bimhaw` entry point is `bimhaw.cli:program.run` (`invoke.Program` + tasks in `bimhaw.main`). `bimhaw_init` already uses **click**.

This plan removes invoke **as the task runner** only. Until a separate CLI migration, `invoke` remains a **runtime** dependency of the `bimhaw` command. Optional follow-up: reimplement `main.py` commands on click and drop runtime invoke.

ADR-0008 documents dual entry points but does not mention invoke; a small ADR is recommended when packaging/CLI wiring changes (step 0006).

## Current baseline (analysis summary)

### Packaging

- `setup.py`: name `bimhaw`, version **`0.1`** (hardcoded), `src/` layout, `install_requires = [invoke, jinja2, click]`, console scripts `bimhaw` / `bimhaw_init`, `include_package_data=True`.
- `MANIFEST.in`: `graft src` (package data under `src/bimhaw/`).
- Loose `requirements.txt` / `dev.requirements.txt` / `tools.requirements.txt`.
- **Version drift**: `setup.py` → `0.1`; `_version.py` → `2020-03-06a0.dev0`; `tasks/sysconfig.py` → `0.0.0a0.dev0`.
- No `pyproject.toml`, no lockfile, no `tests/`, no mise config.

### Dev tasks worth keeping (from structure step 0003 analysis)

- Clean: dist/build/egg-info, `__pycache__`, editor junk (`*~`)
- Build: sdist + wheel
- Publish: TestPyPI / PyPI
- Tag: annotated `v*` release tag

Everything else in `tasks/` is **not** migrated — deleted with the scaffolding.

### Files to remove when invoke-as-tasks goes away

- Entire `tasks/` tree
- `env.bash` (only wraps `inv` completion) — replaced by mise activation + optional just completions
- Dev dependency on invoke **for tasks** (runtime invoke stays until CLI migration)
- Loose requirements files once uv groups + lock exist

## Tool choices

### mise (host tools + env vars)

- **Bootstrap**: one-time install of mise on the host (only hard precondition not provided by the repo).
- **`.mise.toml`** (committed):
  - `[tools]`: pin **uv**, **just** (and optionally **python** if we want mise to supply the interpreter uv uses — see step 0001 for the chosen default).
  - `[env]`: non-secret project env defaults (e.g. helpful `UV_*` non-secret settings, project markers, documentation-oriented vars).
  - Do **not** put PyPI tokens in committed config.
- **`.mise.local.toml`** (gitignored): developer-local overrides and secrets (e.g. `UV_PUBLISH_TOKEN`, personal index URLs).
- **Trust + install**: `mise trust` (if needed) then `mise install` for pinned tools.
- **Default invocation for anything in-repo**: `mise exec -- <tool> …` (does not depend on activate).
- **Activation / shims**: optional operator shell integration only — not assumed by justfile, scripts, or contributing “run this” commands.
- Replaces the “install uv and just yourself from random docs” story and replaces inv-centric `env.bash`.

### uv (Python package workflow)

- Provided **by mise** (version pinned in `.mise.toml`).
- `uv sync` / `uv run` / `uv build` / `uv publish` / `uv.lock`.
- Owns the project virtualenv (`.venv`), not mise.

### hatch (hatchling)

- Build backend only in `[build-system]`.
- Metadata, scripts, package data, single version source.
- **No** hatch env/matrix workflow in this plan.

### just (task runner)

- Provided **by mise** (version pinned).
- Root `justfile`: thin recipes over `uv` / `git` / filesystem cleans.
- Not responsible for installing tools or setting env (mise does that before `just` runs).

### git

- Remains a normal host/system tool (not required to be mise-managed).
- Used by `just tag` for annotated release tags.

## Target maintainer surface

```bash
# one-time host bootstrap
# install mise (https://mise.jdx.dev) — only global prerequisite

# once per clone (or when pins change): trust if prompted, install tools
mise trust                       # if config not trusted yet
mise install                     # installs pinned uv + just from .mise.toml

# --- happy path: no shell activation required ---
# python deps / packaging (always via mise exec in docs & automation)
mise exec -- uv sync
mise exec -- uv build
mise exec -- uv publish --index testpypi

# maintainer tasks: just is also under mise
mise exec -- just clean
mise exec -- just build
mise exec -- just publish-test
mise exec -- just publish
mise exec -- just tag VERSION=x.y.z

# product CLI (runtime invoke until CLI migration)
mise exec -- uv run bimhaw ...
mise exec -- uv run bimhaw_init ...

# --- optional operator QoL (not required by project tooling) ---
# eval "$(mise activate bash)"   # or shims; then bare `uv` / `just` may work in that shell
```

**Writing project tooling:** justfile recipes, scripts, and CI should invoke `uv` (and any other mise-managed CLI) as `mise exec -- uv …` (or document a single entrypoint that does). Do **not** require `mise activate` for those paths.

Local secrets / overrides:

```bash
# gitignored — not committed
# .mise.local.toml  → [env] UV_PUBLISH_TOKEN=… etc.
```

## Plan steps

| Step | File | Summary |
|------|------|---------|
| 0001 | [0001-mise-tooling-and-env.md](0001-mise-tooling-and-env.md) | Add `.mise.toml` (tools: uv, just; env defaults); gitignore `.mise.local.toml`; document activation | **Completed** |
| 0002 | [0002-pyproject-hatch.md](0002-pyproject-hatch.md) | Add `pyproject.toml` (hatchling); metadata/deps/scripts/package data; unify version | **Completed** |
| 0003 | [0003-uv-lock-and-workflow.md](0003-uv-lock-and-workflow.md) | uv workflow via mise-provided uv; groups + `uv.lock`; retire loose requirements |
| 0004 | [0004-justfile-tasks.md](0004-justfile-tasks.md) | `justfile` bare-minimum recipes; assume mise activated PATH |
| 0005 | [0005-remove-invoke-tasks.md](0005-remove-invoke-tasks.md) | Delete `tasks/`, `env.bash`; drop invoke-as-dev-runner |
| 0006 | [0006-docs-and-contributing-align.md](0006-docs-and-contributing-align.md) | Contributing/docs + ADR: mise → uv/hatch/just |
| 0007 | [0007-verify.md](0007-verify.md) | Verify mise install/activation, uv, just, packaging, docs |

## Execution guidelines

- **Plan only until the user explicitly requests execution** of this plan or a step.
- Prefer task-specific tools (`write`, `edit`, `tree`, `summarize`, …) over shell for repo edits; use shell when running `mise`/`uv`/`just`/`git` is the actual verification.
- Do not migrate tests/docs/env task ghosts.
- Keep product behavior stable; packaging/DX only.
- Do not commit secrets; use `.mise.local.toml` pattern.
- **Config files stay content-focused** (`.mise.toml`, `justfile`, `pyproject.toml`, etc.): no long usage/bootstrap preambles—only brief comments on specific choices. Usage belongs in `contributing/` (enforced when writing those docs in step 0006).
- Update this README statuses as steps complete.
- Track actionable work in `.issues/` when executing.
- Structural decision → ADR in `design/decisions/` (step 0006).

## Relationship to structure upgrade plan

- Structure plan step **0003** (contributing) described an `inv`-based bare minimum. **This DX plan supersedes that command surface.** When writing `contributing/development.md`, document **mise + uv + just**.
- Structure plan steps 0009/0010 may cross-link this plan.
- Do **not** append these as 0011+ on the structure plan; keep this directory as the DX series.

## Success criteria

- [ ] `.mise.toml` pins at least **uv** and **just**; `mise install` installs them for `mise exec` / `mise which`
- [ ] Non-secret env defaults live in `.mise.toml` `[env]`; secrets documented for `.mise.local.toml` (gitignored)
- [ ] In-repo tooling and docs happy path use **`mise exec -- …`**; shell activate/shims documented only as optional operator choice
- [ ] `env.bash` gone; no inv-completion bootstrap
- [ ] `pyproject.toml` is the single packaging source; `setup.py` removed (or justified stub only)
- [ ] `mise exec -- uv sync` works; `mise exec -- uv build` produces sdist+wheel including package data
- [ ] Console scripts install and run (`bimhaw`, `bimhaw_init`) via `mise exec -- uv run …`
- [ ] `mise exec -- just clean` / `just build` work without activate; publish recipes documented and dry-runnable
- [ ] `tasks/` gone
- [ ] invoke is not a **dev task** dependency; runtime dep only if CLI still uses it (called out in docs)
- [ ] Version has one source of truth
- [ ] Contributing/plan docs describe **mise + uv + hatch + just**, not jubeo; include “writing project tooling” note (`mise exec`)

## References

- `setup.py`, `MANIFEST.in`, `requirements*.txt`, `env.bash`
- `tasks/` (delete list)
- `src/bimhaw/cli.py`, `main.py`, `init.py`, `_version.py`
- `.agents/plan/0003-create-contributing-dir.md` (bare-minimum surface; tool names change)
- `design/decisions/0008_cli-entry-points-and-workflow.md`
- `design/decisions/0009_current-state-limitations-and-technical-debt.md`
- mise / uv / hatch / just docs (cache under `.agents/references/` if fetched during execution)
