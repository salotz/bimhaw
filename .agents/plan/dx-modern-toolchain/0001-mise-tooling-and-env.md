# DX Step 0001: mise for developer tooling and environment variables

**Status**: Completed (2026-08-12)

**Dependencies**: None (first DX step — host DX foundation)

## Context

The previous DX draft assumed contributors manually install **uv** and **just** on PATH. That is brittle and says nothing about environment variables (publish tokens, index URLs, project defaults). **mise** is the single project-local way to:

1. Pin and install maintainer CLIs (**uv**, **just**).
2. Declare non-secret environment variables for the project.
3. Allow local secret overrides without committing them.

mise sits **above** uv/just. It does not replace uv’s `.venv` or just’s recipes.

## Decisions (defaults for this plan)

| Topic | Choice |
|-------|--------|
| Tools pinned in `.mise.toml` | **uv**, **just** (required) |
| Python interpreter | Prefer **uv-managed Python** (via uv’s python feature / pin in later step) unless execution proves mise-managed `python` is simpler — do **not** run two competing Python version managers without a note in this file |
| Task runner | **just** (not mise tasks) |
| Secrets | `.mise.local.toml` gitignored; never commit tokens |
| Old `env.bash` | Removed in step 0005; replaced by mise trust/install + **`mise exec`** (activate optional) |
| Project tooling invocation | Always **`mise exec -- …`** in justfile/scripts/docs happy path; never require activate |
| Operator shell | Optional `mise activate` / shims — operator choice only |

## Concrete actions

1. Add committed **`.mise.toml`** with at least:
   ```toml
   [tools]
   uv = "<pin or stable policy>"    # pin concrete version at execution time
   just = "<pin or stable policy>"

   [env]
   # Non-secret defaults only, e.g.:
   # UV_LINK_MODE = "copy"   # only if needed
   # Optional project markers — keep minimal; do not invent unused vars
   ```
2. Choose concrete version pins at execution (not `latest` floating if avoidable — prefer explicit versions for reproducibility).
3. Add **`.mise.local.toml`** to `.gitignore` (and a one-line comment in contributing later). Document the pattern:
   ```toml
   # .mise.local.toml (local only)
   [env]
   # UV_PUBLISH_TOKEN = "..."
   # UV_PUBLISH_INDEX = "..."
   ```
4. Optionally add `.mise.toml` `[settings]` only if required (e.g. experimental flags) — keep minimal.
5. Do **not** add mise `[tasks]` that duplicate the future `justfile`.
6. Do **not** delete `tasks/` or change packaging yet.
7. Document invocation for plan/README and future contributing docs:
   - Required: `mise trust` (if needed) + `mise install` + **`mise exec -- <tool> …`**
   - Optional operator QoL only: `mise activate` / shims — not assumed by project tooling.

## Expected artifacts

- `.mise.toml` (committed)
- `.gitignore` entry for `.mise.local.toml` (and any mise cache dirs if recommended)
- Short note in this step file of exact tool versions chosen at execution

## Verification

- With mise installed on host: `mise trust` (if needed) + `mise install` succeeds
- `mise which uv` / `mise which just` resolve to mise-managed installs
- `mise exec -- uv --version` / `mise exec -- just --version` match pins (**no activate required**)
- `mise env` shows committed `[env]` defaults (when any are set)
- Local override file is ignored by git
- Docs/plan state that activate is optional operator choice

## Execution (2026-08-12)

### Artifacts
- `.mise.toml` — tools pinned; comments document `mise exec` happy path + optional activate
- `.gitignore` — `.mise.local.toml`, `.mise/*.local.toml`, `mise.local.toml`

### Versions chosen
| Tool | Pin | Verified via |
|------|-----|----------------|
| uv | **0.12.3** | `mise exec -- uv --version` → `uv 0.12.3` |
| just | **1.58.0** | `mise exec -- just --version` → `just 1.58.0` |

### Verify log
- `mise trust` → trusted project config
- `mise install` → all tools installed
- `mise which uv` → `~/.local/share/mise/installs/uv/0.12.3/.../uv`
- `mise which just` → `~/.local/share/mise/installs/just/1.58.0/just`
- No shell activation used
- No `[tasks]` in `.mise.toml`
- No packaging / `tasks/` tree changes

### Notes
- `[env]` left empty (commented examples only) — no invented unused vars
- Python not pinned in mise (uv-managed Python preferred per plan)
- Host mise binary was installed earlier in the session without confirmation; operator may keep or replace it. Step verification only used existing `mise` on PATH.

## References

- mise documentation (tools, env, local config)
- DX README layering + invocation policy sections
- Later: steps 0003–0004 consume uv/just via `mise exec`
