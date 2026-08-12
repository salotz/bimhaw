# DX Step 0007: Verify modern DX toolchain

**Status**: Not Started

**Dependencies**: 0001–0006

## Context

Confirm the migration meets success criteria without reintroducing jubeo scaffolding or claiming missing test/docs flows work.

## Verification checklist

### mise (tools + env)

- [ ] `.mise.toml` present; pins **uv** and **just**
- [ ] `mise install` succeeds on clean machine story (mise itself preinstalled)
- [ ] `mise which uv` / `mise which just` resolve to mise-managed tools
- [ ] Committed `[env]` defaults visible via `mise env` (if any)
- [ ] `.mise.local.toml` gitignored; documented for secrets
- [ ] No `env.bash`; shell story is mise activate (or `mise exec`)

### Packaging

- [ ] `pyproject.toml` present; hatchling is build backend
- [ ] `setup.py` gone (or justified stub only)
- [ ] `uv.lock` present and committed
- [ ] Loose requirements files gone or clearly non-authoritative
- [ ] Version single-sourced; `bimhaw.__version__` matches distribution intent
- [ ] Wheel contains non-Python package data — `uv build` + list wheel contents

### Install & entry points

- [ ] `uv sync` works on clean checkout (under mise-activated shell)
- [ ] `uv run bimhaw` — help or expected invoke CLI behavior
- [ ] `uv run bimhaw_init` — click CLI help
- [ ] Runtime: `import invoke` still available in env (until CLI migration)
- [ ] No `import tasks` / no `tasks/` directory

### Task runner

- [ ] `just --list` shows only bare-minimum recipes
- [ ] `just clean` removes dist/build caches without deleting source
- [ ] `just build` succeeds via uv
- [ ] publish recipes documented; dry-run or --help path safe (no accidental real PyPI upload)

### Docs

- [ ] `contributing/development.md` is mise-first; matches actual commands
- [ ] Structure plan step 0003 aligned
- [ ] ADR recorded (mise + uv + hatch + just)
- [ ] DX plan README success criteria checked off

### Process

- [ ] Prefer task-specific tools for file inspection; shell OK for mise/uv/just verification
- [ ] No new test/docs/env scaffolding invented “to fill the gap”
- [ ] No secrets committed

## Concrete actions

1. Run through checklist; capture failures in this file or issues.
2. Fix gaps with minimal edits (tooling/docs only).
3. Mark DX plan README status complete when green.
4. Optionally open `.issues/` items for follow-ups (product CLI off invoke; tests).

## Expected artifacts

- Completed checklist (this file updated)
- DX README status → Complete (or “Complete with known follow-ups”)

## References

- DX README success criteria
- All prior DX step files
