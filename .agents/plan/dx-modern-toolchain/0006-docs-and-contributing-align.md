# DX Step 0006: Docs, contributing plan alignment, ADR

**Status**: Not Started

**Dependencies**: 0001–0005 (toolchain real); coordinate with structure plan step 0003

## Context

Structure plan step 0003 (`create-contributing-dir`) was rewritten around **current** `inv py.*` commands, then noted DX supersession. Contributing docs, README pointers, and design decisions must describe **mise + uv + hatch + just**. Record the toolchain choice as an ADR.

## Concrete actions

### A. Align structure plan step 0003 (if contributing/ not written yet)

Update `.agents/plan/0003-create-contributing-dir.md` so bare-minimum setup is:

1. Install **mise** (host bootstrap)
2. `mise install` + activate
3. `uv sync`, `uv build`, `uv publish` / TestPyPI
4. `just clean`, `just build`, `just publish-test`, `just publish`, `just tag`
5. Env vars: committed `.mise.toml` `[env]`; secrets in gitignored `.mise.local.toml`
6. Explicit: invoke `tasks/` removed; invoke may remain **runtime** for `bimhaw` CLI only

If `contributing/` already exists, edit those files instead of only the plan.

### B. Write or update contributor docs (bare minimum only)

Still only:

```
contributing/README.md
contributing/development.md
```

Content:

- **Prereq**: install mise once on the host
- **Enter project**: `mise install`, `mise activate` (shell-specific)
- **Python deps**: `uv sync`
- **Optional**: just is provided by mise (no separate install story)
- **Layout**: `src/bimhaw/`, `pyproject.toml`, `uv.lock`, `justfile`, `.mise.toml`
- **Env vars**: what may live in `.mise.toml` vs `.mise.local.toml` (tokens, indexes)
- **Commands table** (just + uv)
- **Version**: single source (`_version.py` or as chosen)
- **Publish caution** + token via local mise env
- Point product usage at `README.org`; design at `design/`
- Honest: no test suite yet (ADR-0009); no sphinx task port
- Do not document hatch as something to install globally

### C. User-facing / agent pointers

- Root `README.org`: short “Development” note → `contributing/development.md`
- Root `AGENTS.md`: point at contributing + this DX plan; mention mise for tools/env if needed
- `.agents/plan/README.md` (structure): keep link to this DX plan

### D. ADR

Add `design/decisions/NNNN_modern-dx-mise-uv-hatch-just.md` (next free number):

- Context: setuptools + jubeo invoke debt; dual use of invoke; ad-hoc host tool installs
- Decision:
  - **mise** for pinned host tools (uv, just) and project env vars (local file for secrets)
  - **hatchling** + pyproject for build/metadata
  - **uv** for lock/venv/build/publish
  - **just** for maintainer tasks only
  - remove `tasks/` and `env.bash`
  - runtime invoke retained until CLI migration
- Consequences: one host bootstrap (mise); reproducible tool versions; clearer secrets boundary; need mise trust/activate; product still tied to invoke

## Expected artifacts

- Updated structure plan 0003 and/or `contributing/*`
- Minimal README.org / AGENTS.md cross-links
- New ADR (name includes mise)
- DX plan README status notes

## Verification

- `summarize` contributing docs — setup path is mise-first; no `inv` for maintainer tasks; no “brew install uv and just” as the primary story
- Secrets guidance present
- ADR present and linked
- Commands match justfile + pyproject + `.mise.toml` reality

## References

- `.agents/plan/0003-create-contributing-dir.md`
- `design/decisions/0008_*.md`, `0009_*.md`
- DX steps 0001–0005 artifacts
