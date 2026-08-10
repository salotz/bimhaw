# Plan Step 0004: Create `.agents/` Directory for Agent-Specific Context

**Status**: Not Started

**Dependencies**: 0001, 0002 (AGENTS.md will reference .agents/)

## Context

Per RFC 22 (`.agents/references/agent-guidelines/rfcs/salotz.022_ai-coding-structure/README.md`):

- "Additional agent specific context should be placed in the `.agents/` directory."
- This is for progressive disclosure, harness-specific context, or standardized forms.
- Subdirectories:
  - `skills/`: per agentskills.io
  - `agents/`: custom agents
  - `context/`: arbitrary discoverable context files (extension of bootloader)

Per RFC 23 (local agent context):
- Local overrides: `.agents.local.md` or `.agents.local/` next to repo's `.agents/`.
- Operator context lives in host locations (`~/.config/agents/` or `~/.agents`).
- Agent-derived (generated) resources go under extended XDG `xagents/` (RFC 24).

Current repo has zero `.agents/` (confirmed via tree).

Project turn context requires:
> Create .agents/ for agent-specific context (context/, skills/ etc.)

The root AGENTS.md (after step 0002) will point here.

## Concrete Actions

1. Use `write` (or multiple) to create the directory structure by writing files (write creates parent dirs).
2. Create at minimum:
   - `.agents/README.md` or `.agents/context/README.md` explaining purpose.
   - `.agents/context/` with at least one file, e.g. `agent-guidelines-pointer.md` that points to the cached references under `.agents/references/agent-guidelines/`.
   - `.agents/skills/` (empty or with a placeholder README; processes from contributing/ may later be exposed here).
   - `.agents/agents/` if custom agents are defined (placeholder for now).
3. Add a small discoverable context file that can be loaded to inject the plan/design references without bloating root AGENTS.md.
4. Document in the new file how local overrides work (reference RFC 23 summary).
5. Do not put human process docs here; those go in `contributing/`.
6. Update AGENTS.md and design/README.md to reference `.agents/`.

Prefer creating via `write` calls. Use `tree` and `summarize` to verify (no shell mkdir).

## Expected Artifacts

- `.agents/` directory tree
- `.agents/context/` with at least one context file
- Placeholders for skills/ and agents/
- Updates to cross-references (AGENTS.md, design/README.md)

## Verification

- `tree .agents`
- `summarize .agents/context/<file>.md`
- Confirm structure matches RFC 22 description.

## Related

- Corresponding issue in `.issues/` (per 0006)
- Step 0005 will reference this for design/ updates
- Step 0010 may later populate skills/ from contributing/

## References

- `.agents/references/agent-guidelines/rfcs/salotz.022_ai-coding-structure/README.md`
- `.agents/references/agent-guidelines/rfcs/salotz.023_local-agent-context/README.md`
- `.agents/references/agent-guidelines/rfcs/salotz.024_extended_xdg_base_directory/README.md`
- `.agents/references/agent-guidelines/summaries/...`
- Turn context explicit requirement
