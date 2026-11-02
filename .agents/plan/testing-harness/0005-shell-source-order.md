# Step 0005: Optional bash source-order tests

**Status**: Not started — execution pending explicit user request

**Dependencies**: 0003–0004

## Context

Python snapshots prove template text. A thin bash source proves the loops actually `.` files in order. This is **not** a login-matrix.

## Concrete actions

1. Fixture modules append to `BIMHAW_TEST_LOADED` (e.g. `aliases:git`, `envs:dev`).
2. Generate a profile into isolated dir; write `env.sh` that sets `BIMHAW_DIR` to that dir.
3. Run:
   ```
   bash --noprofile --norc -c 'export BIMHAW_DIR=...; . "$BIMHAW_DIR/env.sh"; . "$BIMHAW_DIR/active/shells/bash/interactive.bash"; printf "%s\n" "$BIMHAW_TEST_LOADED"'
   ```
4. Assert order matches v1 interactive sequence.
5. `pytest.importorskip` / skip if `bash` missing.
6. Do not start login shells, do not use `-l`, do not read `/etc/profile` if avoidable (`--noprofile --norc` on the inner bash).

## Expected artifacts

- `tests/test_shell/test_source_order.py`

## Verification

- Order assertion; skip-on-no-bash documented
