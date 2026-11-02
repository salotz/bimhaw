# Comprehensive Makeover Sequence

**Status**: Plan Only — Do not execute until explicitly requested

**Date**: 2026-10-23

**Owner**: AI-assisted work

This is the **umbrella** for the product makeover. Child plans keep the detail; this file is the order of work, the gates, and what “done” means.

## Child plans (do not collapse)

| Plan | Role |
|---|---|
| [DX: mise + uv + hatch + just](../dx-modern-toolchain/README.md) | How *this repo* is built and run (`mise exec`). Incomplete: no `uv.lock`, no `justfile`, `tasks/` still present. |
| [Testing harness](../testing-harness/README.md) | **Gate.** Characterize **current** bimhaw before rewriting it. |
| [Module system rework](../module-system-rework/README.md) | Product model: user modules as packages, profiles with `extends`, phases, skills, mise boundary. |
| [Structure / agent-guidelines](../README.md) | RFC 22 layout. Orthogonal; do not block the makeover on contributing/ docs polish. |
| [Agent explainability](../agent-explainability/README.md) | **Separate.** `bimhaw explain` + prompt/module legends + host/Goose consumer skill. Not a makeover gate. |

**mise appears twice on purpose:**

- DX: pin uv/just; **project recipes use `mise exec`**. Never require operator `mise activate`.
- Product: optional user snippet `eval "$(mise activate bash)"` in **post-prompt**. bimhaw does **not** own per-directory tool versions, PATH, or completions for mise-managed tools (global *or* project `mise.toml`).

## Locked product conclusions (do not reopen in implementation)

1. **No shipped module catalogue.** Users and their agents write `lib/`. bimhaw ships **skills**, not git/kubectl/mise modules.
2. **mise-managed tools** (user global config or project `mise.toml`) do not get bimhaw `env` / `autocomplete` modules. Workflow aliases that *call* those tools are fine.
3. The only bimhaw-side mise work is: **post-prompt hook point**, doctor warnings, shim-aware `have`, a skill with a copy-paste activate snippet.
4. direnv XOR mise activate. No cwd watcher. No project `.bimhaw/` overlay.
5. Profiles stay the activation unit (`active` symlink, new shells). No live unload.
6. sh + bash only. Generation + runtime dir + symlink indirection stay.

## Why tests first

There is **no test suite on master**. What exists:

- Jubeo leftover recipes in `tasks/modules/py.py` pointing at `tests/tests/test_{unit,integration,benchmarks}` and `pytest -m 'not interactive'` — **directories never created** in this repo.
- Worktrees named `test` / `test2` are the DX-plan commit, not a harness.
- DX plan **non-goal** was “do not add a test suite.” That non-goal is **overridden** for this makeover: a small harness is required before implementation.
- ADR-0009 already recorded “no automated tests.”
- `CONFIG_DIR` is `$HOME/.bimhaw` at import time — tests cannot run safely until the runtime dir is injectable.

Rewriting generation/config without characterization tests means we cannot tell a loader bug from “it always did that.”

**Gate:** module-system-rework implementation (steps 0002+) does not start until the testing-harness plan’s “v1 characterization green” criterion is met.

ADRs (module-system-rework 0001) may be written in parallel with the harness; they do not mutate `src/` except the tiny `CONFIG_DIR` override needed for tests.

## Sequence (execution later)

```
Phase A  Finish DX enough to run tools
         dx 0003 uv.lock + dev group
         dx 0004 justfile  (+ test recipe — exception to original DX 0004)
         dx 0005 delete tasks/ env.bash
         (0006 docs only as needed for mise exec + just test)
              │
              ▼
Phase B  Testing harness  ← GATE
         (see testing-harness/)
         B0  BIMHAW_DIR / CONFIG_DIR override (minimal product change)
         B1  pytest layout, fixtures, just test
         B2  v1 unit + generation snapshots
         B3  isolated-HOME CLI integration (init, gen, load, current)
         B4  optional shell sourcing of generated scripts (no full login matrix)
              │
              ▼
Phase C  Module-system ADRs + glossary  (rework 0001)
         may overlap B if no src/ churn beyond B0
              │
              ▼
Phase D  Module-system implementation
         rework 0002–0007 against the harness
         extend tests as behavior changes (do not delete v1 snapshots until migrate is proven)
              │
              ▼
Phase E  Skills, docs, architecture “current” catch-up
         rework 0005, 0008, DX 0006 leftover, structure plan leftovers as convenient
```

Do **not** wait on: Sphinx, tox, benchmarks, CI, zsh, product CLI invoke→click (follow-up), RFC 22 contributing polish.

## Phase A — DX remainder (only what tests need)

Original DX non-goals included “no test suite.” Amend:

- Add `[dependency-groups] dev` with `pytest` (and pytest-cov only if cheap; skip coverage gates).
- Commit `uv.lock`.
- `justfile` recipes: original clean/build/publish/tag **plus** `test` → `uv run pytest`.
- Public entrypoint remains `mise exec -- just test` / `mise exec -- uv run pytest`.
- Then delete `tasks/` so nobody thinks `inv tests_unit` is the harness.

Stop DX 0006/0007 from blocking Phase B: contributing docs can lag.

Details stay in the DX step files; this umbrella only changes the **test** exception and the **gate**.

## Phase B — Harness (summary)

Full design: [testing-harness/README.md](../testing-harness/README.md).

Must-haves before D:

| Layer | What |
|---|---|
| Isolation | Override runtime dir (`BIMHAW_DIR` or test monkeypatch). Never touch the developer’s `~/.bimhaw`. |
| Unit | `get_profile_data`, `format_profile_data`, `gen_profile`, `write_profile` on tmp paths |
| Snapshots | Generated sh/bash scripts from `docs/example_config.py` + a tiny fixture lib |
| CLI | `bimhaw_init`, `profile gen/load/ls/current` against isolated dir |
| Shell (thin) | `bash -c 'source generated; …'` for “lists are sourced in order” — not a POSIX login-matrix |

Out of harness v1: live `link-shells` against real `$HOME`, interactive prompt, actual mise cd, benchmarks, tox.

## Phase C–E — Module rework

Unchanged in intent from [module-system-rework/README.md](../module-system-rework/README.md). Implementation order there becomes:

1. ADRs (0001) — allowed during B
2. Layout + schema (0002) — **after B green**; add resolver tests first in the same PR if possible
3. Loader + post-prompt (0003)
4. Directory-local doctor rules (0004) — no mise client
5. Migrate v1 lib/config (0006) — keep v1 snapshots until migrate tests pass
6. Doctor / show (0007)
7. Skills (0005) — can trail code if they match shipped behavior
8. Verify (0008)

## Success criteria (makeover)

- `mise exec -- just test` (or `uv run pytest`) is green on a clean checkout **without** `mise activate`.
- v1 characterization tests exist **before** profile/config dicts disappear.
- New config is `PROFILES` + module packages; login/interactive not in user config.
- Generated interactive bash has an empty-or-filled **post-prompt** phase after prompt, before autocomplete.
- No `src/bimhaw` tree of example modules; skills exist for write-module / mise-safe / migrate.
- Doctor (or tests) encode: no direnv+mise activate together; static autocomplete is global-only.
- User `~/.salotz.d`-style lib can migrate mechanically (0006).

## Explicitly not in this makeover

- Community plugins
- zsh/fish
- In-session profile switch
- Replacing mise
- `bimhaw_complete_lazy` product
- Dropping runtime invoke from the product CLI
- Full RFC 22 contributing/ tree

## Execution rule

Nothing in Phases A–E runs until the user explicitly asks (e.g. “start Phase A”, “execute testing-harness 0001”). Prefer finishing A+B in order; do not start D without B green.
