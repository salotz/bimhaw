# Step 0008: Verify the makeover

**Status**: Not started — execution pending explicit user request

**Dependencies**: 0002–0007 as landed; this step may run incrementally

## Context

The **v1 harness** already exists after [testing-harness](../testing-harness/README.md). This step adds **v2** tests on that floor: resolver, migrate, generated phase order (post-prompt present), doctor. Not a full interactive bash matrix.

Keep using `mise exec -- uv run pytest`. Update or replace v1 snapshots in the same changes as 0002–0003; do not delete v1 config tests until migrate (0006) is proven.

## Concrete actions

1. Resolver tests: extends, exclude/reorder, cycles, missing module, sh then bash file pick.
2. Snapshot or substring tests of generated scripts: phase order, empty post-prompt, no baked-in `mise activate`.
3. Migrate fixture from v1 example_config + tiny lib.
4. Doctor fixtures for stale gen and mise/direnv XOR.
5. Manual checklist (document in this file after execution):
   - init → write one user module → gen → load → new bash has aliases
   - add a user mise post-prompt module → `cd` into a project with `mise.toml` changes PATH (if operator has mise)
   - recovery profile without mise still starts
6. Update `design/architecture/overview.md` from “target” to “current” when behavior matches.
7. Cross-link `AGENTS.md` / contributing only if those files exist and the structure plan allows.

## Expected artifacts

- Tests under `tests/` (or project-standard location)
- Architecture doc catch-up
- This step updated with checklist results at execution time

## Verification

- Tests run via the DX-approved invocation (mise exec + uv), no assumption of shell activate
- Architecture overview no longer describes 14 dicts as current
