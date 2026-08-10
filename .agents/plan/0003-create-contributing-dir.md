# Plan Step 0003: Create Top-Level `contributing/` Directory

**Status**: Not Started

**Dependencies**: 0001, preferably after or alongside 0002 (AGENTS.md will reference it)

## Context

Per RFC 22 (`.agents/references/agent-guidelines/rfcs/salotz.022_ai-coding-structure/README.md`):

- "This information is housed in the `contributing/` folder or for smaller projects a `CONTRIBUTING.md` file. If the `contributing/` folder is present the `CONTRIBUTING.md` file should not be present."
- Must contain `README.md` (and optional `AGENTS.md`) with generic considerations.
- Additional files for specific work processes / roles (e.g. `releases.md`, `role_engineer.md`).
- Processes should be exposable as agent skills.

Current repo has none. The agent-guidelines repo provides snippets under `.agents/references/agent-guidelines/contributing/` (collation.md, editing.md).

Project turn context explicitly requires:
> Create top-level contributing/ folder with README.md (and AGENTS.md) etc. following RFC22

The project's own `.agents/references/agent-guidelines/AGENTS.md` says:
> See the [contributing](./contributing/) directory for roles and workflows to run.

(Note: This plan step describes future work. The `contributing/` will be at the project root, while the plan itself lives under `.agents/plan/`.)

## Concrete Actions

1. Read the cached contributing snippets and RFC 22 using summarize/analyze.
2. Create `contributing/README.md`:
   - Explain purpose (dual-use for humans and agents).
   - List current processes and roles.
   - Link to RFC 22.
   - Reference the agent-guidelines collation/editing as examples.
   - Point to how to add new process docs.
3. Optionally create a minimal `contributing/AGENTS.md` if specific agent instructions for contributing are needed (or keep empty for now).
4. Seed with initial files based on project needs:
   - At minimum: `contributing/README.md`
   - Possibly `contributing/editing.md` or `contributing/collation.md` adapted if useful (or reference the cached ones).
   - For bimhaw specifically, consider initial process docs like `contributing/role_agent.md` or `contributing/process_upgrade-structure.md` (link to this plan).
5. Use `write` tool (creates parents).
6. Update design/README.md (in later step) and root AGENTS.md to reference it.
7. No root CONTRIBUTING.md should be added; remove if one appears later.

## Expected Artifacts

- `contributing/README.md`
- Possibly `contributing/AGENTS.md`
- Initial process/role files (at least one to demonstrate)
- Updated references in other docs (cross-step)

## Verification

- `tree contributing`
- `summarize contributing/README.md`
- Confirm no bare shell used.

## Related

- Will create corresponding `.issues/` entry (step 0006).
- Later steps will populate more process docs.
- Adoption ADR (0007) may reference this.

## References

- `.agents/references/agent-guidelines/rfcs/salotz.022_ai-coding-structure/README.md`
- `.agents/references/agent-guidelines/contributing/collation.md`
- `.agents/references/agent-guidelines/contributing/editing.md`
- Project `design/README.md` (current structure section)
- Turn context requirements
