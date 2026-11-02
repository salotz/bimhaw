# Plan: Testing Harness (gate before module-system implementation)

**Status**: Plan Only — Do not execute until explicitly requested

**Date**: 2026-10-23

**Owner**: AI-assisted work

**Umbrella**: [comprehensive-makeover](../comprehensive-makeover/README.md) Phase B  
**Depends on**: DX remaining bits that let `mise exec -- uv run pytest` work (uv.lock, dev group, just `test` recipe).  
**Blocks**: [module-system-rework](../module-system-rework/README.md) implementation (0002+). ADRs (rework 0001) may proceed in parallel.

## Purpose

Give bimhaw a **small, isolated pytest harness** that characterizes **current (v1)** behavior so the module makeover cannot land untested.

This is **not** the jubeo scaffold (`inv tests_unit` → `tests/tests/test_unit`). Those paths never existed in this repo. Do not recreate tox, benchmarks, lizard, or `pytest -m interactive` playgrounds.

## Current baseline

- No `tests/` directory on master.
- `tasks/modules/py.py` (jubeo) defines `tests_unit` / `tests_integration` / `tests_benchmarks` / `tests_tox` against missing trees. Delete with DX 0005; do not port.
- `CONFIG_DIR = expanduser("$HOME/.bimhaw")` is set at **import** in `src/bimhaw/__init__.py`. `config.py` `exec`s `$HOME/.bimhaw/config.py`. CLI `link_shells` writes `$HOME/.profile` etc. Tests will destroy a developer’s real setup unless isolation is first.
- Templates and `write_profile` are pure enough to unit-test once config is injectable.
- DX 0001–0002 done (`.mise.toml`, `pyproject.toml`). No `uv.lock`, no `justfile`, no pytest dep.

## Non-goals

- Full POSIX login vs non-login vs SSH vs GUI matrix
- Driving a real interactive bash with a PTY
- Testing the operator’s actual `~/.bimhaw`
- Coverage gates, mutation testing, CI (nice later)
- Testing mise hook-env / packslip (out of product scope)
- Porting jubeo quality/benchmark tasks

## Design

### Isolation (mandatory, tiny product change)

Add an env override **before** any makeover:

```python
# src/bimhaw/__init__.py (sketch)
CONFIG_DIR = osp.expanduser(osp.expandvars(
    os.environ.get("BIMHAW_DIR", "$HOME/.bimhaw")
))
```

Name: `BIMHAW_DIR` matches `env.sh`’s `BIMHAW_DIR`. Document: tests and power users may set it; default remains `~/.bimhaw`.

`link-shells` still uses `$HOME/.profile`. Integration tests that would call it must either:

- skip, or
- pass a fake `HOME` for the whole process (`tmp_path` as HOME, plus `BIMHAW_DIR`).

Prefer **not** calling `link-shells` in v1 tests.

`bimhaw.config` execs `CONFIG_DIR/config.py` at import. Tests that need `write_profile` must:

1. write a config into the isolated dir, **then**
2. import / reload `bimhaw.config`, **or**
3. (better, small refactor) load config via a function `load_config(path) -> namespace` instead of module-level `exec`.

The function extract is allowed in harness work: it is testability, not the module makeover. Keep the public `bimhaw.config.PROFILES` module globals if the CLI still expects them, populated by `load_config()`.

### Layout

```
tests/
  conftest.py              # isolated BIMHAW_DIR, tmp HOME option, fixtures
  fixtures/
    v1_lib/                # tiny lib matching current LIB_DIRS
    v1_config.py           # subset of docs/example_config.py with real names
  test_unit/
    test_profile_data.py
    test_gen_profile.py
    test_format_profile_data.py
  test_generation/
    test_write_profile.py  # tmp dest, snapshot or substring
  test_cli/
    test_init.py
    test_profile_commands.py
  test_shell/              # optional in B4
    test_source_order.py
```

pytest `testpaths = ["tests"]`. No nested `tests/tests/`.

### How to run

After Phase A:

```
mise exec -- uv run pytest
mise exec -- just test
```

No `mise activate`. Python from uv. pytest from the `dev` group.

### What v1 must lock in (characterization)

These are the behaviors the makeover is allowed to change **only with new tests**:

1. **Config surface**: `PROFILES` and the 14 dicts; missing profile name → KeyError at gen (today).
2. **Generation**: templates render space-delimited lists; `NONE_PROFILE` sentinel for prompts; output tree `profiles/<name>/shells/{sh,bash}/…`.
3. **sh inheritance in templates**: bash login sources `sh/login.sh` then extra lists; bash interactive sources sh funcs/aliases/nonlogin_env then bash interactive envs → prompt → autocomplete.
4. **Init**: creates `shell_dotfiles/`, `lib/` with `LIB_DIRS`, `config.py`, `env.sh`, `profiles/`. `--config` / `--lib` symlink.
5. **profile load**: gen + `active` symlink to `profiles/<name>`.
6. **lib link**: gen also `ln -T` lib into the profile dir (see `main.py`).
7. **Post-prompt absence**: current `interactive.bash.j2` has **no** post-prompt step (ADR-0009). Snapshot this so 0003 is a visible diff, not an accident.

### Shell tests (B4, optional but useful)

Not a login-matrix. Pattern:

- Isolated dir with generated profile
- `bash --noprofile --norc -c 'BIMHAW_DIR=...; source env.sh; source active/shells/bash/interactive.bash; type some_func'`
- Fixture modules that only `TEST_LOADED="$TEST_LOADED foo"` so order is assertable

Skip if `bash` missing. Do not use the developer’s rc files.

## Steps

See numbered files in this folder.

| Step | Focus |
|---|---|
| [0000](0000-dx-prerequisite.md) | Point at DX 0003–0005 + pytest exception; do not duplicate DX |
| [0001](0001-isolate-config-dir.md) | `BIMHAW_DIR` + `load_config()` so imports are testable |
| [0002](0002-pytest-skeleton.md) | `tests/`, conftest, pyproject pytest config, just test |
| [0003](0003-v1-unit-and-snapshots.md) | Unit + generation snapshots of current templates |
| [0004](0004-cli-integration.md) | init / gen / load / current / ls against tmp dir |
| [0005](0005-shell-source-order.md) | Optional bash source-order |
| [0006](0006-gate.md) | Checklist: harness green → module implementation unblocked |

## Success (gate)

- `mise exec -- uv run pytest` exits 0 without `mise activate`.
- No test reads or writes the real `~/.bimhaw` or real `~/.bashrc`.
- Snapshots (or substring assertions) exist for generated `login.sh`, `interactive.bash`, `login.bash`.
- CLI init+gen+load covered.
- Documented in this README that module-system-rework 0002+ must keep these tests green or deliberately rewrite them in the same change.

## Relationship to module-system-rework 0008

Rework 0008 adds **v2** tests (resolver, migrate, doctor). It does not replace this harness. This plan is the floor.
