# Plan Step 0002: Update Root `AGENTS.md` to Follow Official Template

**Status**: Not Started

**Dependencies**: 0001 (plan folder established)

## Context

Current root `AGENTS.md` is a short custom file:

```
# Project Description
...
# Agent Guidelines
This project follows the guidelines at https://github.com/salotz/agent-guidelines.
...
```

Per RFC 22 (see `.agents/references/agent-guidelines/rfcs/salotz.022_ai-coding-structure/README.md` and the template in `.agents/references/agent-guidelines/rfcs/salotz.022_ai-coding-structure/agents_md_template.md`):

- `AGENTS.md` is the **bootloader**.
- For larger projects it should be a compact table-of-contents pointing to `design/`, `contributing/`, `.agents/`, `plan/`, etc.
- The official `agents_md_template.md` should be used/adapted.

The project's own `.agents/references/agent-guidelines/AGENTS.md` and generic guidelines also reference pointing to `contributing/`.

The project hints in the turn context explicitly require:
> Update AGENTS.md to follow agents_md_template + point to plan/design/contributing/.agents

## Concrete Actions

1. Read the template and current AGENTS.md using task tools (summarize or equivalent read).
2. Adapt the template for bimhaw:
   - Fill "Project Description" with content from current AGENTS.md + design/ (brief).
   - Update "How to Use", "Project Intent" (link to design/goals.md), "Terminology" (design/glossary.md).
   - Add sections pointing to:
     - .agents/plan/ (this upgrade plan, under agent context)
     - design/ (full)
     - contributing/ (to be created)
     - .agents/ (to be created)
   - Reference cached guidelines under .agents/references/agent-guidelines/ (correct agent-specific location, not under design/).
   - Mention RFC 22/23/24 adoption.
3. Use `write` or `edit` to replace the content of `AGENTS.md` (prefer write for clean replacement, or edit for precision).
4. Keep it small and human-readable while effective for agents (incremental disclosure).
5. Update any cross-references if needed.

Do **not** use shell `cat`/`cp` for the edit.

## Expected Artifacts

- Updated `AGENTS.md` at project root conforming to template.
- Possibly a small diff or note in plan step.

## Verification

- Use `tree` and `summarize` on `AGENTS.md` to confirm.
- Re-read via summarize to verify links and structure.
- Later full audit in step 0008.

## Related Issues

Will have a corresponding issue created in `.issues/` (see step 0006).

## References

- `.agents/references/agent-guidelines/rfcs/salotz.022_ai-coding-structure/agents_md_template.md` (full template)
- `.agents/references/agent-guidelines/generic-agent-guidelines.md`
- Current `AGENTS.md`
- Project `design/README.md`, `design/goals.md`, `design/glossary.md`
- Turn context explicit requirement

## Notes

After update, the bootloader will guide future agents to the right places, including this `.agents/plan/`.

Important: All plan work happens under `.agents/plan/`. The references to agent-guidelines are under `.agents/references/agent-guidelines/`.
