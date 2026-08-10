# Upgrade Plan: Conform bimhaw to Agent Guidelines

**Status**: Plan Only — Step 0002 Complete; Remaining Execution Pending Explicit User Request

**Date**: 2026-08-10

**Owner**: AI-assisted work (following current tasks in turn context)

This document lives under the `.agents/plan/` folder (agent-specific context).

It captures the concrete steps required to upgrade the **bimhaw** repository to full conformance with the agent-guidelines defined at the cached references:

- `.agents/references/agent-guidelines/generic-agent-guidelines.md`
- `.agents/references/agent-guidelines/rfcs/salotz.022_ai-coding-structure/README.md` (RFC 22: AI Coding Repository Structures)
- `.agents/references/agent-guidelines/rfcs/salotz.023_local-agent-context/README.md` (RFC 23)
- `.agents/references/agent-guidelines/rfcs/salotz.024_extended_xdg_base_directory/README.md` (RFC 24)
- Supporting: `.agents/references/agent-guidelines/glossary.md`, cached summaries, `agents_md_template.md`, and `contributing/` snippets.

See also the project's own `AGENTS.md`, `design/README.md`, `design/goals.md`, and `design/glossary.md`.

## Purpose

bimhaw's current `AGENTS.md` is a minimal project description. The `design/` folder is mostly complete but incomplete per RFC 22 (missing template, references to `.agents/plan/`, `contributing/`). There is no top-level `contributing/`, no `.agents/` agent-specific context directory, and no `plan/` folder (it will live under `.agents/plan/`).

The goal of this upgrade is to:

- Provide proper "bootloader" + progressive disclosure for AI agents (and humans).
- Follow RFC 22 project layout exactly (AGENTS.md + design/ + contributing/ + .agents/).
- Incorporate host/local context guidance from RFC 23/24.
- Use compacted inlining and cached remote resources (now under `.agents/references/agent-guidelines/`).
- Prefer task-specific tools (write, tree, analyze, summarize, edit, todo, etc.) over shell.
- Document plans here; track actionable work as individual issues in `.issues/`.

All changes must be done while following the guidelines themselves (no unnecessary shell, use analyze/tree/summarize first, etc.).

## Current Conformance Gaps (Baseline)

- Root `AGENTS.md`: Short custom text, not using `agents_md_template.md`.
- No `.agents/plan/` folder (this document creates the location for plan steps under agent context).
- No top-level `contributing/` (RFC 22 prefers folder + README.md over root CONTRIBUTING.md).
- No `.agents/` (for skills/, agents/, context/ per RFC 22; local overrides per RFC 23).
- `design/`:
  - Missing `decisions/0000_adr-template.md` (referenced in design/README.md).
  - design/README.md does not yet reference `.agents/plan/`, `contributing/`, or `.agents/`.
  - No `research/` (optional but mentioned).
  - References to agent-guidelines are not yet fully documented inside design/.
- `.issues/` exists with one example but not yet used for this plan.
- Other potential: host naming (RFC 24), full glossary updates, verification steps.
- No ADR yet recording the decision to adopt these guidelines.

See ADR-0009 for broader current-state limitations (some overlap with structure).

## Plan Steps

Plan steps are documented as individual files in this directory following a naming convention similar to ADRs (index_name.md). Each step file contains:

- Context / motivation
- Concrete actions (preferring task-specific tools)
- Expected artifacts / verification
- Links to related design docs, issues (to be created), and references
- Status

The steps below are the initial set. They may be refined, split, or superseded via updates here + new ADRs.

See the individual step documents:

- [0001-create-plan-folder.md](0001-create-plan-folder.md) — Establish the `.agents/plan/` location and this baseline document (self-referential bootstrap step).
- [0002-update-root-agents-md.md](0002-update-root-agents-md.md) — Replace/update `AGENTS.md` to follow the official `agents_md_template.md` (customized for bimhaw) and point to `.agents/plan/`, `design/`, `contributing/`, `.agents/`. (Completed)
- [0003-create-contributing-dir.md](0003-create-contributing-dir.md) — Create top-level `contributing/` with `README.md` (and optional `AGENTS.md`). Base on RFC 22 and cached snippets from `.agents/references/agent-guidelines/contributing/`. Add initial role/workflow docs as needed.
- [0004-create-agents-dir.md](0004-create-agents-dir.md) — Create `.agents/` per RFC 22 for agent-specific context. Include `context/`, stubs for `skills/`, and any host-specific notes per RFC 23. Place discoverable context files here.
- [0005-complete-design-folder.md](0005-complete-design-folder.md) — Finish `design/` conformance:
  - Add `decisions/0000_adr-template.md` (Nygard style from RFC 22).
  - Update `design/README.md` to document full layout including `.agents/plan/`, `contributing/`, `.agents/`, and how to use for plans.
  - Consider adding `research/` placeholder.
  - Update `design/glossary.md` for new terms (plan step, agent context, etc.) if project-specific.
  - Ensure all external references use compacted summaries under `.agents/references/agent-guidelines/`.
- [0006-populate-issues-from-plan.md](0006-populate-issues-from-plan.md) — As we go along, create individual issues in `.issues/` (using the YAML frontmatter style from existing `.issues/0001-export-profiles.md`). One issue per actionable plan step or sub-task. Do not put implementation details in issues; link back to plan steps and design/.
- [0007-add-adoption-adr.md](0007-add-adoption-adr.md) — Record the decision to adopt the agent-guidelines / RFC 22/23/24 structure as a new ADR in `design/decisions/`.
- [0008-audit-and-verify.md](0008-audit-and-verify.md) — Use only task-specific tools (tree, analyze, summarize, read via tools) to audit the entire repo against the guidelines. Update any remaining gaps. Verify no bare shell used for routine reads/edits.
- [0009-update-other-docs.md](0009-update-other-docs.md) — Cross-updates: project README.org, design/goals.md, existing ADRs, glossary, etc. to reference the new structure where appropriate. Ensure naming follows RFC 24 / nexp guidance where applicable.
- [0010-followup-and-maintenance.md](0010-followup-and-maintenance.md) — Establish ongoing process: future plans go in `.agents/plan/`, issues in `.issues/`, use of cached references, tool preference. Possibly expose processes as skills under `.agents/skills/`.

## Execution Guidelines (for this and future plans)

- **Always read guidelines first**: Load relevant files from `.agents/references/agent-guidelines/` and `design/` before editing.
- **Tool preference**: Use `tree`, `analyze`, `summarize`, `write`, `edit`, `todo__todo_write`, `load` etc. Avoid `shell` for reads, directory creation (write creates parents), etc. Only use shell when no task-specific tool exists and with explicit justification.
- **Cache first**: Any new remote reference must be cached locally under `.agents/references/` with a summary.
- **Compacted inlining**: When referencing verbose standards, point to summaries.
- **Incremental disclosure**: AGENTS.md stays small (TOC). Load specifics only when needed.
- **Issues vs Plans**: High-level planning and rationale live in `.agents/plan/`. Concrete, trackable work items (with status, priority, labels) live as individual files in `.issues/`.
- **ADRs for decisions**: Structural or architectural choices go through `design/decisions/` (Nygard format). This plan itself may lead to ADRs.
- **Verification**: After changes, re-run tree/analyze/summarize to confirm.
- **Host context (RFC 23/24)**: Respect local overrides via `.agents.local*` if/when present on a host. Use extended XDG paths for generated agent content (`xagents/` etc.) if relevant.
- Update this README and individual step files as progress is made. Use todo tool for tracking during sessions.

## Relationship to Other Documentation

- `AGENTS.md` (root) — Bootloader / entry point. Will point here.
- `design/` — Why and how of the system + this structure adoption.
- `contributing/` (future) — Human + agent processes and roles.
- `.agents/` (future, this location) — Pure agent harness context, skills, extra files, and plans/references.
- `.issues/` — Issue tracker (lightweight file-based).
- `.agents/plan/` — This folder. For upgrade/refactor/feature plans and their steps.

## Next Actions (When User Requests Execution)

Do not execute any of the steps below until the user explicitly says to start (e.g., "start executing the plan" or "execute step 0002").

When authorized:
1. Create corresponding issues in `.issues/`.
2. Proceed step-by-step using only preferred task tools.
3. Add the adoption ADR in `design/decisions/`.
4. Audit with tree/analyze/summarize.

All references below (and in step files) use the correct locations: `.agents/plan/`, `.agents/references/agent-guidelines/`.

See individual step files for details and dependencies.

---
*This plan follows the spirit of RFC 22 by providing structured, discoverable context for agents.*

