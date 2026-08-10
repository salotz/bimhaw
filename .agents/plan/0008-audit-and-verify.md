# Plan Step 0008: Audit and Verify Conformance Using Task-Specific Tools

**Status**: Not Started

**Dependencies**: 0001–0007 (core structure changes in place)

## Context

Per the generic agent guidelines (`.agents/references/agent-guidelines/generic-agent-guidelines.md`):

> Prefer task-specific tools over shell

> Use task-specific tools (write, tree, analyze, summarize, edit)

The turn context explicitly requires:

> Use task-specific tools (write, tree, analyze, summarize, edit); avoid shell

> Verify conformance after changes using tree/analyze/summarize

After structural changes, a full audit must be performed **without** relying on shell for reads, listings, or edits. This demonstrates and enforces the guideline during the upgrade itself.

Current state may still have gaps (e.g. references, cross-links, naming).

## Concrete Actions

1. **Do not use `shell`** for any directory listing, file reading, or editing during this step. Use only:
   - `tree`
   - `analyze`
   - `summarize`
   - `read_image` (if needed, but unlikely)
   - `write` / `edit` (only for fixes found)
   - `todo__todo_write`
   - `load` if applicable

2. Perform a systematic audit:
   - Root level: `tree` on `.` (or specific depths)
   - Confirm presence and structure of:
     - `AGENTS.md`
     - `.agents/plan/`
     - `contributing/`
     - `.agents/`
     - `design/` (full tree)
     - `.issues/`
   - Use `analyze` on key directories for code/structure if relevant (though this is mostly docs).
   - Use `summarize` (with question for "full verbatim" where needed) on:
     - `AGENTS.md`
     - `.agents/plan/README.md` and each plan step
     - `contributing/README.md`
     - `.agents/context/` files
     - `design/README.md`
     - `design/decisions/0000_adr-template.md`
     - `design/decisions/00XX_adopt-....md` (from step 0007)
     - `design/glossary.md`
     - All cached references under `.agents/references/agent-guidelines/`
   - Check for:
     - Correct links (relative where possible)
     - Use of compacted summaries (e.g. "([summary](./...))")
     - No root `CONTRIBUTING.md` (only `contributing/`)
     - Naming follows nexp guidance where practical (RFC 24 summary)
     - Plan steps reference their issues and vice versa
     - No unnecessary duplication

3. For any gaps found, use `edit` or `write` to fix immediately (still using task tools).

4. Update the TODO and this plan step with findings.

5. Optionally run `analyze` on source if needed to check for any agent-related code/docs.

## Expected Artifacts

- Audit log / notes captured in this plan step file (or a separate verification log if preferred).
- Any fixes applied via task tools.
- Final "conformant" state confirmed.

## Verification (self-referential)

- The audit itself uses only allowed tools.
- After fixes: re-run `tree`, `analyze`, `summarize` on critical paths.
- Confirm in plan/README or this file that "Verified with task tools only."

## Related

- Step 0006 (issues for this verification)
- Step 0010 (ongoing process)
- Adoption ADR

## References

- `.agents/references/agent-guidelines/generic-agent-guidelines.md` (Tool Preference section)
- Turn context checklist
- All plan steps 0001-0007
