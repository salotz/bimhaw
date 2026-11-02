# Step 0000: DX prerequisite (run pytest via mise exec)

**Status**: Not started — execution pending explicit user request

**Dependencies**: DX 0001–0002 already done on master (`.mise.toml`, `pyproject.toml`)

## Context

The testing harness cannot be the thing that invents uv/just. It also cannot wait for full DX 0006/0007 docs.

The original DX plan listed “adding a test suite” as a **non-goal**. The comprehensive makeover **overrides** that for a small pytest group and a `just test` recipe.

## Concrete actions (prefer editing DX step files as you execute them)

1. DX 0003: `[dependency-groups] dev = ["pytest"]`; `uv.lock` committed; `.venv/` gitignored if not already.
2. DX 0004: `justfile` with `test` in addition to clean/build/publish/tag.
   ```
   test:
       uv run pytest
   ```
   Public: `mise exec -- just test` and `mise exec -- uv run pytest`.
3. DX 0005: delete `tasks/` and `env.bash` **after** just recipes exist so `inv tests_*` cannot be mistaken for the harness.
4. Do not add tox, coverage gates, or `tests/tests/` nesting.

If DX 0003–0005 are executed as part of this step rather than the DX folder, still mark those DX files complete and keep commands `mise exec`-first.

## Expected artifacts

- `uv.lock`
- `justfile` including `test`
- pytest in the uv dev group
- no `tasks/` (once 0005 is done)

## Verification

- Without activate: `mise exec -- uv run pytest --collect-only` (may collect 0 until 0002)
- `mise exec -- just test` once tests exist
