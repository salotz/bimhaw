# Plan Step 0003: Create Top-Level `contributing/` Directory

**Status**: Not Started (plan updated 2026-08-10 after repo analysis)

**Dependencies**: 0001, 0002 (AGENTS.md already points at `contributing/`)

## Context

Per RFC 22, contributor processes live in top-level `contributing/` (with `README.md`; no root `CONTRIBUTING.md`).

Current repo has **no** `contributing/` and almost no maintainer-facing docs beyond `README.org` (user-oriented) and `design/` (architecture). ADR-0009 notes: informal versioning, no automated tests, basic setuptools packaging, and that `tasks/` is development tooling (jubeo-style scaffolding), not product code.

This step was revised after analyzing packaging metadata and `tasks/` so the contributing docs are a **bare minimum for working on this Python package** — document what exists and what is needed to develop/build it. **Do not invent** new processes, roles, CI, test suites, or release ceremonies that are not already present or implied by working packaging tools.

## Repo Analysis (baseline for this step)

### Packaging / metadata

| Item | Reality |
|------|---------|
| Layout | `src/` (`find_packages(where='src')`) |
| Package | `bimhaw` 0.1, MIT, setuptools |
| Runtime deps | `invoke`, `jinja2`, `click` (`requirements.txt` / `setup.py`) |
| Entry points | `bimhaw` → `bimhaw.cli:program.run`; `bimhaw_init` → `bimhaw.init:cli` |
| Package data | `MANIFEST.in`: `graft src`; `include_package_data=True` |
| Dev deps | `dev.requirements.txt`: pip, wheel, twine, bumpversion, invoke, gitpython, ipython, pdbpp, `-e .` |
| Tools deps | `tools.requirements.txt`: invoke, gitpython, joblib |
| Shell helper | `env.bash` — sources `inv` bash completion |
| User docs | `README.org` (install from git, init, profile gen/load, link-shells) |
| Design | `design/` (goals, glossary, ADRs, architecture) |
| Tests | **None** (no `tests/`, no pytest/tox config) — ADR-0009 |
| Sphinx / docs build tree | **None** (`docs/` is diagrams + `example_config.py` only) |
| Env specs for `env.*` tasks | **None** (no `envs/` directory) |
| pyproject.toml / setup.cfg | **None** (setup.py only) |

### Invoke tasks (`tasks/`) — keep vs drop

Scaffolding is jubeo-style (`core`, `clean`, `env`, `git`, `py` + empty `toplevel` / `plugins.custom`). Many tasks are broken stubs or assume missing trees (tests, Sphinx, `envs/`).

#### Document and treat as the real maintainer surface

These match actual packaging and hygiene for this repo:

| Task | Why keep |
|------|----------|
| `py.clean_dist`, `py.clean_cache`, `py.clean` | Real build/cache hygiene (`setup.py clean`, rm dist/build/egg-info, `__pycache__`) |
| `py.update_tools` | pip/setuptools/wheel/twine upgrade before build |
| `py.build_sdist`, `py.build_bdist`, `py.build` | Actual sdist/wheel via setuptools |
| `py.publish_test_pypi` / `py.publish_test` | twine → TestPyPI (dry-run release path that exists in code) |
| `py.publish_pypi` | twine → PyPI |
| `clean.clean` (and optional `clean.ls`) | Simple junk-file cleanup (`*~` etc.); complementary to `py.clean` |
| `git.release_tag` | Annotated version tag (`git tag -a v…`) — only git task that is coherent |

Also document **non-invoke** bare-minimum commands that already exist outside tasks:

- Editable install: `pip install -r dev.requirements.txt` (includes `-e .`)
- Smoke the installed CLI: `bimhaw --help` / `python -m bimhaw.init --help` (as applicable)
- Optional: `source env.bash` for `inv` completion
- Point at `README.org` for **product** usage (profiles, link-shells); do not duplicate it
- Point at `design/` and root `AGENTS.md` for architecture / agent context

#### Do not document as supported workflows (ignore, fix later, or remove)

| Area | Reason |
|------|--------|
| `py.tests_*`, `py.tests_tox` | No test suite; tox stub is `NotImplemented` |
| `py.docs_*`, `py.website_*` | No Sphinx/Jekyll tree; paths/template bugs |
| `py.benchmark_*`, `py.profile` | No benchmarks practice; profile stub; dated compare paths |
| `py.lint` / `py.complexity` / `py.quality` | No flake8/lizard config or metrics dirs in repo; optional later — **omit from bare minimum** |
| `env.*` (`make`, `deps_pin`, `ls`, …) | No `envs/` specs; `deps_pin_update` and `specs` are broken |
| `core.sanity` | Prints a string only |
| `git.init`, `git.lfs_track` | One-time / unused (empty LFS targets) |
| `git.publish_tags` | Broken (`CURRENT_VERSION` undefined) |
| `py.release`, `py.publish` umbrella | Cross-calls broken/unwired (`publish_tags`, bad imports) |
| `py.version_which` | Command string not formatted for `PROJECT_SLUG` |
| `py.conda_build` | No `conda-recipe` |
| Empty `toplevel` / `plugins.custom` | Placeholders |

**Plan stance on tasks code:** Contributing docs should list the **supported** `inv` commands above and explicitly say the rest of `tasks/` is legacy jubeo scaffolding not required for day-to-day work. Optionally note (one line) that cleaning out broken task modules is future cleanup — **do not** expand this step into a tasks refactor unless separately requested.

### Existing “contributing” material

- None in-repo (`contributing/`, `CONTRIBUTING.md`).
- `.agents/references/agent-guidelines/contributing/{collation,editing}.md` are about maintaining **agent-guidelines** docs, not this package — **do not** copy them in as bimhaw processes.
- ADR-0009 + `design/` are the right cross-links for “how we make decisions” and known gaps (tests, etc.).

## Bare-minimum starting point (what to create)

Create only:

```
contributing/
├── README.md           # index + purpose + links
└── development.md      # dev env, layout, supported commands, task keep/ignore
```

No `contributing/AGENTS.md` unless a single short pointer proves necessary (default: **skip**).
No `releases.md`, role files, collation/editing copies, CI docs, or test guides — those would invent process.

### `contributing/README.md` (outline)

1. Purpose: dual-use human + agent maintainer docs for **bimhaw the package**.
2. Start here: link `development.md`.
3. Related (do not duplicate):
   - User/product: `README.org`
   - Design/ADRs: `design/README.md`, especially ADR-0009
   - Agent bootloader: root `AGENTS.md`, plans in `.agents/plan/`
4. Scope: bare minimum to install editable, build, clean, and (if needed) publish; not a full OSS contributor ladder.
5. How to extend later: add a focused `contributing/<topic>.md` only when a real process exists (e.g. after tests are added).

### `contributing/development.md` (outline)

1. **Prerequisites**: Python 3; git; working directory = repo root.
2. **Dev install**:
   - `pip install -r dev.requirements.txt` (editable `-e .`, wheel/twine/bumpversion, invoke, …)
   - Optional: `source env.bash` for invoke completion
3. **Layout** (short):
   - `src/bimhaw/` — package
   - `setup.py`, `requirements.txt`, `dev.requirements.txt`, `MANIFEST.in`
   - `tasks/` — invoke maintainer tasks (partially legacy)
   - `design/`, `docs/` (examples/diagrams only), `README.org`
4. **Day-to-day commands** (document only these):
   - `inv py.clean` / `inv py.clean_dist` / `inv py.clean_cache`
   - `inv clean.clean` — editor backup junk
   - `inv py.update_tools` then `inv py.build` (sdist + wheel)
   - `inv py.publish_test` / `inv py.publish_pypi` — only when intentionally releasing
   - `inv git.release_tag --release=<ver>` — tagging (coordinate with version in package)
5. **Task inventory**: short “supported” vs “ignore (scaffolding/broken/missing trees)” tables matching the analysis above. Do not present tests/docs/env tasks as working.
6. **Version / release reality**: version is informal (`setup.py` / `_version.py`); bumpversion is in dev deps but no `.bumpversion` config called out — document “update version sources then tag/build/twine” without inventing a full release playbook. Point at broken `py.publish` umbrella → use the concrete twine tasks + `git.release_tag` instead.
7. **What not to expect**: no test runner yet (ADR-0009); no Sphinx build; `~/.bimhaw` is runtime/cache for the **product**, not the dev tree.
8. **Design changes**: non-trivial behavior changes → read/add ADRs under `design/decisions/`.

## Concrete Actions (when executing this step)

1. Re-skim this plan file + `setup.py` / `dev.requirements.txt` / `tasks/modules/py.py` headers via `summarize` if anything drifted.
2. `write` `contributing/README.md` per outline (create parents).
3. `write` `contributing/development.md` per outline — keep factual and short; quote real task names only.
4. Do **not** add root `CONTRIBUTING.md`.
5. Do **not** invent CI, tests, env pinning, or role docs.
6. Do **not** copy agent-guidelines collation/editing as bimhaw process files.
7. Cross-links: root `AGENTS.md` already points at `contributing/`; deeper design/README updates stay in steps 0005/0009 unless a one-line fix is trivial.
8. Verify with `tree contributing` and `summarize` on both new files. Task tools only.

## Expected Artifacts

- `contributing/README.md`
- `contributing/development.md`
- Updated status on this plan step (+ plan README summary if the one-liner changes)
- Session TODO updated during execution

## Verification

- `tree contributing`
- `summarize contributing/README.md` and `contributing/development.md`
- Confirm: no root `CONTRIBUTING.md`; no invented processes; supported `inv` list matches analysis; tests/docs/env not claimed working
- Confirm packaging facts match `setup.py` / requirements files

## Related

- Step 0002 already links `contributing/` from `AGENTS.md`
- Step 0006: issue for this work
- Step 0009: README.org / design cross-links if needed
- ADR-0009: honest about missing tests and basic packaging
- Future (out of scope here): add tests → then a real `contributing` testing note; prune broken `tasks/` modules

## References

- `setup.py`, `requirements.txt`, `dev.requirements.txt`, `tools.requirements.txt`, `MANIFEST.in`, `env.bash`
- `tasks/` (especially `modules/py.py`, `clean.py`, `git.py`, `env.py`, `core.py`)
- `README.org` (user install/usage only)
- `design/decisions/0009_current-state-limitations-and-technical-debt.md`
- RFC 22 via `.agents/references/agent-guidelines/summaries/salotz-rfc-022-ai-coding-structure.md`
- Root `AGENTS.md`

## Notes

Prior version of this step suggested optional `AGENTS.md`, role/workflow seeds, and agent-guidelines collation/editing examples. That was too generic. **Revised scope** is package-maintainer bare minimum only, driven by the analysis above.

### Supersession: DX toolchain plan (2026-08-10)

A separate plan, [`.agents/plan/dx-modern-toolchain/`](dx-modern-toolchain/README.md), modernizes maintainer DX as:

| Layer | Tool |
|-------|------|
| Host tool installs + env vars | **mise** (`.mise.toml`; secrets in gitignored `.mise.local.toml`) |
| Package build / metadata | **hatch** (hatchling) + `pyproject.toml` |
| Python lock / venv / build / publish | **uv** (installed via mise) |
| Task runner | **just** (installed via mise; not mise tasks) |
| Remove | invoke **`tasks/`**, `env.bash`, setuptools-as-SoT |

**When executing this contributing step:**

- If the DX plan is accepted or already executed, document **mise → uv / just** (plus `pyproject.toml` / `uv.lock` / `.mise.toml`) — do **not** teach `inv py.*` as the happy path.
- Host bootstrap is **install mise once**; then `mise trust` (if needed) + `mise install`. Do not primary-path “brew install uv and just” separately.
- **Happy path for all project commands:** `mise exec -- uv …` / `mise exec -- just …`. Do **not** require `mise activate`.
- **Writing project tooling** (document explicitly): justfile, scripts, CI, and agent commands must call mise-managed tools via `mise exec` (or an entrypoint that does). Ambient PATH / activate hooks are operator choice only.
- Optional operator QoL: `mise activate` or shims — mention briefly; never as a prerequisite for recipes.
- Env vars: non-secret defaults in `.mise.toml` `[env]`; publish tokens etc. in `.mise.local.toml` only.
- If contributing docs must land *before* DX execution, either (a) briefly document current inv commands as transitional, or (b) document the **target** mise exec surface and point at the DX plan.
- Runtime **`invoke` may remain** as a dependency of the product `bimhaw` CLI (`bimhaw.cli` / `main.py`) even after `tasks/` is deleted — call that out so contributors do not “remove invoke entirely” by mistake.

Keep/drop **intent** from the analysis above still applies (clean/build/publish/tag only; no tests/docs/env ghosts). Only the **tooling stack** changes under DX.
