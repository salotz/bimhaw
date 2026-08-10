# Plan Step 0007: Add Adoption ADR for Agent Guidelines

**Status**: Not Started

**Dependencies**: 0001–0005 (structure in place or planned); ideally before or alongside full verification

## Context

The project has been following agent-guidelines informally (via the short AGENTS.md pointing to github).

To treat this professionally (per design/goals.md and ADR-0009), the decision to adopt RFC 22/23/24 structure, use `plan/`, `contributing/`, `.agents/`, cached references, tool preferences, etc. should be recorded as an Architecture Decision Record.

Per RFC 22: "Specific decisions should be documented. These use the Architecture Decision Record framework."

Existing ADRs are in `design/decisions/` using Nygard style.

This adoption is a significant structural and process decision.

## Concrete Actions

1. Read the ADR template (once created in step 0005) and several existing ADRs using `summarize` to match style exactly.
2. Create a new ADR, e.g. `design/decisions/0010_adopt-agent-guidelines.md` (number to be determined based on sequence; use next available).
   - Title: "Adopt Agent Guidelines (RFC 22/23/24) and Structured Repository Layout"
   - Status: Accepted (or Proposed if done before full implementation)
   - Date: current
   - Deciders: (current agent-assisted session + operator)
   - Context: Current state (minimal AGENTS.md, partial design/, no contributing/, no `.agents/plan/` or `.agents/`), desire to follow guidelines for AI-assisted and human work.
   - Decision: Adopt the structure: root AGENTS.md per template, design/ enhancements, top-level contributing/, .agents/ (with `.agents/plan/` for plans), .issues/ usage, cached references under `.agents/references/agent-guidelines/`, tool preference (no unnecessary shell), compacted inlining, etc.
   - Consequences: Positive (better agent context, reproducibility, professionalism); Negative (added directories, maintenance of references); Risks (over-structuring small project); Mitigations (not all RFC components mandatory).
   - Related Decisions: ADR-0009 (current limitations), future ADRs on config etc.
   - References: Link to cached RFC summaries, generic guidelines, this plan/, turn context.
3. Use `write` to create the file.
4. Update plan step and design/README if needed.
5. Possibly update AGENTS.md or contributing/ to reference the ADR.

## Expected Artifacts

- New ADR file in `design/decisions/`
- References to it from plan/README.md and design/README.md
- Updated status in this plan step

## Verification

- `tree design/decisions`
- `summarize design/decisions/00XX_adopt-....md`
- Confirm it follows exact header and section style from other ADRs.

## Related

- Step 0005 creates the template used here.
- Step 0006 creates an issue for this.
- Step 0008 audit will reference it.

## References

- `design/decisions/0009_current-state-limitations-and-technical-debt.md`
- `.agents/references/agent-guidelines/rfcs/salotz.022_ai-coding-structure/README.md`
- `.agents/references/agent-guidelines/generic-agent-guidelines.md`
- Project `design/README.md` (Contributing to Design section)
