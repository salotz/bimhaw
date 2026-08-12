# DX Step 0005: Remove invoke task runner and jubeo `tasks/`

**Status**: Not Started

**Dependencies**: 0004 (`justfile` covers bare minimum); 0001–0003 so build does not need setuptools scripts from tasks

## Context

`tasks/` is jubeo-style invoke scaffolding. Most tasks are broken or assume missing trees. Maintainer surface is mise → just + uv. **Product CLI still imports invoke** — do not remove runtime dependency or rewrite `bimhaw.main` in this step.

`env.bash` only enabled inv completion; **mise activation** is the replacement for developer shell setup.

## Delete list

- Entire directory `tasks/`
- `env.bash` (inv completion only)
- Any docs/comments that instruct `inv …` for **dev** tasks
- Dev-only invoke extras if any were added for running tasks (runtime `[project.dependencies]` keep invoke until CLI migration)

## Do not delete / do not break

- `src/bimhaw/cli.py`, `src/bimhaw/main.py` (product CLI)
- Runtime dep: `invoke` in `[project.dependencies]`
- click-based `bimhaw_init`
- `.mise.toml` / justfile / pyproject / uv.lock

## Concrete actions

1. Confirm `just clean` / `just build` work without `tasks/` under mise-activated shell.
2. Delete `tasks/` tree and `env.bash`.
3. Grep/summarize for remaining `inv ` / `env.bash` **dev** references; fix in step 0006 if not already gone.
4. Ensure no packaging hook still expects `tasks` as a package.
5. Optional note: follow-up plan to move product CLI from invoke → click and then drop runtime invoke.

## Expected artifacts

- No `tasks/` directory
- No `env.bash`
- Runtime invoke still installed with the app via uv
- Developer shell story = mise only

## Verification

- `tree` root — no `tasks/`, no `env.bash`
- `uv run bimhaw` still imports (product)
- `just build` still works
- `python -c "import tasks"` fails (desired)

## References

- DX README scope boundary (runtime vs dev invoke)
- Step 0001 mise replaces env.bash role
