# Step 0005: `--paste` and `--format json`

**Status**: Not started — execution pending explicit user request

**Dependencies**: 0001–0003; doctor facts if rework 0007 has landed (optional section)

## Concrete actions

1. `bimhaw explain --paste`:
   - one markdown document: stack + prompt legend + profile module list + BIMHAW_DIR + active name + “generated vs config stale?” if cheap
   - no env values, no secrets, no full file dumps
   - suitable to paste under a PS1 in a GitHub issue or agent chat
2. `--format json` for the same facts (stable keys: `profile`, `bimhaw_dir`, `prompt_module`, `modules`, `legend_markdown`).
3. Document in bimhaw-shell skill: “if you only have the PS1, ask for this paste.”

## Verification

- JSON parses; paste mode has no ANSI
- Isolated test fixture appears in both formats
