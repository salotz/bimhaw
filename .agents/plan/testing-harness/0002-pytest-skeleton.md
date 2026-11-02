# Step 0002: pytest skeleton and fixtures

**Status**: Not started — execution pending explicit user request

**Dependencies**: 0000 (pytest installed), 0001 (BIMHAW_DIR)

## Concrete actions

1. `tests/conftest.py`:
   - session/function fixture `bimhaw_home` = `tmp_path`
   - set `BIMHAW_DIR` (and optionally `HOME`) via `monkeypatch`
   - reload `bimhaw` / `bimhaw.config` after env is set **or** call `load_config` explicitly in tests
2. `tests/fixtures/v1_lib/` matching current `LIB_DIRS` with 1–2 dummy modules per interesting slot (`envs`, `aliases`, `funcs`, `prompts`, `autocomplete`).
3. `tests/fixtures/v1_config.py` with two profiles (`bimhaw`, `common`) listing those dummy names — not empty lists so generation is observable.
4. `[tool.pytest.ini_options]` in `pyproject.toml`: `testpaths = ["tests"]`, `addopts = "-q"`.
5. Empty-or-one smoke test so `pytest` is green (e.g. `CONFIG_DIR` equals the monkeypatched dir).
6. `just test` already from 0000; confirm it collects `tests/`.

## Expected artifacts

- `tests/` tree
- fixtures
- one smoke test

## Verification

- `mise exec -- uv run pytest` green
- Running pytest does not create `~/.bimhaw` if it was absent (assert in smoke test or doctor the real home)
