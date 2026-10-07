# DX Step 0006: Docs, contributing plan alignment, ADR

**Status**: Not Started

**Dependencies**: 0001–0005 (toolchain real); coordinate with structure plan step 0003

## Context

Structure plan step 0003 (`create-contributing-dir`) was rewritten around **current** `inv py.*` commands, then noted DX supersession. Contributing docs, README pointers, and design decisions must describe **mise + uv + hatch + just**, with a clear split:

- **Project tooling / docs / CI / agents** → always **`mise exec -- …`**
- **Operator shell integration** (`mise activate`, shims) → optional, operator-chosen; never required for recipes to work

## Concrete actions

### A. Align structure plan step 0003 (if contributing/ not written yet)

Update `.agents/plan/0003-create-contributing-dir.md` so bare-minimum setup is:

1. Install **mise** (host bootstrap)
2. `mise trust` (if needed) + `mise install`
3. Use tools only via **`mise exec -- …`** (no activate required):
   - `mise exec -- uv sync` / `build` / `publish` …
   - `mise exec -- just clean` / `build` / `publish-test` / `publish` / `tag`
4. Env vars: committed `.mise.toml` `[env]`; secrets in gitignored `.mise.local.toml` (applied when using mise exec)
5. Optional: operator may `mise activate` for bare `uv`/`just` on PATH — not part of the supported automation surface
6. Explicit: invoke `tasks/` removed; invoke may remain **runtime** for `bimhaw` CLI only

If `contributing/` already exists, edit those files instead of only the plan.

### B. Write or update contributor docs (bare minimum only)

Still only:

```
contributing/README.md
contributing/development.md
```

Optionally add a short third file only if it stays minimal:

```
contributing/project-tooling.md   # OR a dedicated section inside development.md
```

**Prefer one section inside `development.md`** unless it gets long — “Writing project tooling”.

#### `development.md` content

- **Prereq**: install mise once on the host
- **Enter project**: `mise trust` (once) + `mise install` (when pins change)
- **Run anything**: `mise exec -- <cmd>` — happy path for humans, agents, and CI
- **Python deps**: `mise exec -- uv sync`
- **Tasks**: `mise exec -- just …` (just provided by mise; no separate install story)
- **Layout**: `src/bimhaw/`, `pyproject.toml`, `uv.lock`, `justfile`, `.mise.toml`
- **Env vars**: `.mise.toml` `[env]` vs `.mise.local.toml` (tokens, indexes)
- **Optional shell integration**: `mise activate` / shims — operator preference; project does not depend on it
- **Version / publish caution**
- Point product usage at `README.org`; design at `design/`
- Honest: no test suite yet (ADR-0009)

#### Writing project tooling (must document)

Rules for anyone adding scripts, just recipes, CI steps, or agent-facing commands:

1. **Do not assume** `uv`, `just`, or project env vars are on the ambient PATH.
2. **Do** invoke mise-managed tools as `mise exec -- uv …`, `mise exec -- just …`, etc.
3. justfile public entrypoint is `mise exec -- just <recipe>`; recipes may call `uv` directly only under that contract (or use `mise exec -- uv` inside recipes for defense in depth).
4. **Do not** require contributors to edit shell rc or run `mise activate` for the repo to be usable.
5. Leave activate/shims to the operator (and optionally point at host RFC 23 `shell.md` prefs if present).
6. Never commit secrets; use `.mise.local.toml`.

#### Config / tooling files vs contributing docs (must document)

- Files like `.mise.toml`, `justfile`, `pyproject.toml` stay **content-focused**.
- Allowed: short comments on **why a specific value/choice** exists (pin policy, layout quirk).
- **Not** allowed: long usage/bootstrap/how-to preambles (install steps, activate vs exec, copy-paste tutorials).
- All usage, bootstrap, and operator workflow live in **`contributing/`** (e.g. `development.md`).
- Prefer linking the shared baseline rather than re-deriving rules:
  `~/tree/personal/devel/agent-guidelines/shared/project-management-and-tooling.md`
  (bimhaw `.agents/references/agent-guidelines/` may lag; prefer the devel checkout).

### C. User-facing / agent pointers

- Root `README.org`: short “Development” note → `contributing/development.md`
- Root `AGENTS.md`: point at contributing + this DX plan; **prefer `mise exec`** when running project tools; do not assume activate
- `.agents/plan/README.md` (structure): keep link to this DX plan

### D. ADR

Add `design/decisions/NNNN_modern-dx-mise-uv-hatch-just.md` (next free number):

- Context: setuptools + jubeo invoke debt; dual use of invoke; ad-hoc host tool installs
- Decision:
  - **mise** for pinned host tools (uv, just) and project env vars (local file for secrets)
  - **hatchling** + pyproject for build/metadata
  - **uv** for lock/venv/build/publish
  - **just** for maintainer tasks only
  - **In-repo invocation via `mise exec`**; shell activate/shims optional operator choice
  - remove `tasks/` and `env.bash`
  - runtime invoke retained until CLI migration
- Consequences: one host bootstrap (mise); reproducible tool versions; clearer secrets boundary; automation works without shell hooks; product still tied to invoke

## Expected artifacts

- Updated structure plan 0003 and/or `contributing/*` including tooling invocation rules
- Minimal README.org / AGENTS.md cross-links
- New ADR (name includes mise; mentions mise exec policy)
- DX plan README status notes

## Verification

- `summarize` contributing docs — setup is mise install + **`mise exec`**; activate is optional only
- “Writing project tooling” rules present
- Secrets guidance present
- ADR present and linked
- Commands match justfile + pyproject + `.mise.toml` reality

## References

- `.agents/plan/0003-create-contributing-dir.md`
- DX README “Invocation policy”
- `design/decisions/0008_*.md`, `0009_*.md`
- DX steps 0001–0005 artifacts
