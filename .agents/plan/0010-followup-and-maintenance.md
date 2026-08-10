# Plan Step 0010: Establish Follow-up and Maintenance Process

**Status**: Not Started

**Dependencies**: All prior steps (0001–0009)

## Context

Once the initial upgrade is complete, the project must have a sustainable process so that the structure does not bit-rot and future work (by humans or agents) continues to follow the guidelines.

This includes:
- Future plans are always written under `.agents/plan/`.
- Actionable work is tracked in `.issues/`.
- References under `.agents/references/agent-guidelines/` are kept current (using collation process).
- Tool preference (task-specific over shell) is enforced.
- New contributors/agents are guided by the updated `AGENTS.md`, `contributing/`, and `.agents/`.
- Local host context (RFC 23) and naming (RFC 24) are respected.
- Processes can be exposed as agent skills under `.agents/skills/`.

Per RFC 22, contributing docs should be dual-use and processes exposable as skills.

The project's `.agents/references/agent-guidelines/contributing/collation.md` describes the role of keeping summaries up to date.

Turn context and project hints require following RFC22/23/24 on an ongoing basis.

## Concrete Actions

1. Create or update process documentation in `contributing/`:
   - `contributing/process_plans-and-issues.md` (or similar descriptive name): How to start a new plan, write steps, create corresponding issues, link everything.
   - `contributing/role_agent.md` or `contributing/role_contributor.md`: Guidelines for AI agents and humans (tool preference, read guidelines first, cache remote resources, use compacted inlining, update plan/README when executing, etc.).
   - Reference the collation and editing snippets from `.agents/references/agent-guidelines/contributing/`.

2. Optionally expose the plan process as a skill:
   - Create `.agents/skills/process-plan-step.md` (or follow agentskills.io format once defined) that describes the workflow for agents.
   - Or place a pointer in `.agents/context/`.

3. Update `.agents/plan/README.md` (the upgrade plan overview) with a "Maintenance" section describing the ongoing process.

4. Add a note in root `AGENTS.md` (if not already) under contributing or general guidance.

5. Document how to update cached references:
   - Copy new versions to `.agents/references/`.
   - Create or update summaries.
   - Follow collation guidelines.

6. For host-specific items: document use of `.agents.local/` overrides in the contributing doc or a `.agents/context/` file.

7. Use only task-specific tools for all of the above.

8. Create a corresponding issue in `.issues/` for this step (per 0006).

## Expected Artifacts

- New file(s) in `contributing/` describing the process.
- Skill or context file(s) under `.agents/`.
- Updated `.agents/plan/README.md`.
- Possibly minor updates to AGENTS.md.
- Evidence that collation process is understood (maybe a note).

## Verification

- `tree contributing`
- `tree .agents`
- `summarize contributing/process_plans-and-issues.md`
- Confirm references in plan/README.md and AGENTS.md.
- Re-audit with task tools (step 0008 style) focused on process docs.

## Related

- Step 0006 (issues)
- Step 0008 (audit)
- Step 0009 (doc updates)
- Adoption ADR (0007)

## References

- `.agents/references/agent-guidelines/rfcs/salotz.022_ai-coding-structure/README.md` (contributing processes as skills)
- `.agents/references/agent-guidelines/contributing/collation.md`
- `.agents/references/agent-guidelines/generic-agent-guidelines.md` (caching, tool preference, compacted inlining)
- RFC 23/24 summaries
- Project `AGENTS.md` (post-update)
- Turn context ongoing requirements

## Notes

This step closes the initial upgrade loop and sets the project up for continued agent-assisted development following the guidelines.
