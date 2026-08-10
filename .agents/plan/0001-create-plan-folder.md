# Plan Step 0001: Establish `.agents/plan/` Folder and Baseline Document

**Status**: Completed (2026-08-10)

**Related**:
- RFC 22 (via cached summary)
- Project `design/README.md` (mentions plans implicitly)
- This plan's `.agents/plan/README.md`

**Execution**:
- Directory `.agents/plan/` asserted (pre-existed from planning; write tool creates parents when used).
- `.agents/plan/README.md` (re)written via `write` tool containing:
  - Purpose and scope of the upgrade effort.
  - Baseline conformance gaps analysis.
  - Numbered list of concrete plan steps.
  - Execution guidelines (tool preference, caching, issues vs plans, etc.).
  - Links to references under `.agents/references/agent-guidelines/`.
- All via task-specific tools (`write`, `edit`, `tree`, `summarize`, `todo__todo_write`); no unnecessary shell.
- Cross-checked against RFC 22 summary: `.agents/plan/` is the correct location under agent-specific context (per RFC 22's `.agents/` for progressive disclosure).
- Session TODO updated throughout.
- Verified post-write with `tree` on `.agents/plan/` and root.
- Step files already present; this step bootstraps the plan location.

## Context

According to the agent guidelines (RFC 22), larger projects should have structured context. The turn context and project hints explicitly require agent-specific plans and references to live under `.agents/`.

The `.agents/plan/` folder (under agent context) is the location for upgrade/refactor/feature plans. It is distinct from:
- `design/decisions/` (ADRs for *why* a decision was made)
- `.issues/` (trackable individual issues with frontmatter)
- `contributing/` (processes)

This step documents the establishment of the correct location under `.agents/plan/`.

## Decision / Actions (to be executed later)

- Create the directory `.agents/plan/` (via task-specific `write` which creates parents).
- Write `.agents/plan/README.md` containing:
  - Purpose and scope of the upgrade effort.
  - Baseline conformance gaps analysis.
  - Numbered list of concrete plan steps.
  - Execution guidelines (tool preference, caching, issues vs plans, etc.).
  - Links to references under `.agents/references/agent-guidelines/`.

- All content written using `write` / `edit`.

- Update session TODO (for tracking the plan).

## Expected Artifacts

- `.agents/plan/` directory (correct location)
- `.agents/plan/README.md` (complete)
- Subsequent numbered step files under `.agents/plan/`
- Updated TODO entry

## Verification

Use `tree` (task tool) on `.agents/plan/` and root to confirm structure.

Cross-check against RFC 22: plans belong under agent context (`.agents/plan/`).

## Follow-up / Dependencies

This documents the bootstrap. Later steps (when authorized) will:
- Update root AGENTS.md (0002)
- Create corresponding issues in `.issues/`

## References

- `.agents/references/agent-guidelines/rfcs/salotz.022_ai-coding-structure/README.md`
- `.agents/references/agent-guidelines/generic-agent-guidelines.md`
- Project `AGENTS.md`, `design/README.md`, turn context notes
- `.agents/references/agent-guidelines/summaries/salotz-rfc-022-ai-coding-structure.md`

## Notes

This step file documents the requirement to place plan steps under `.agents/plan/` (agent-specific context), not at the top level or under `design/`.

Subsequent steps are documented here for later execution.
