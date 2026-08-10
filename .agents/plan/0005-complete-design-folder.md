# Plan Step 0005: Complete the `design/` Folder for Full Conformance

**Status**: Not Started

**Dependencies**: 0001–0004 (plan, AGENTS.md, contributing, .agents references will be added)

## Context

From project `design/README.md` (current structure section):

```
design/
├── README.md
├── goals.md
├── glossary.md
├── architecture/
│   └── overview.md
├── decisions/
│   ├── 0000_adr-template.md  # Template (MISSING)
│   └── 0001_*.md
├── diagrams/
└── research/  # optional, mentioned but absent
```

Current gaps:
- `decisions/0000_adr-template.md` is referenced but does not exist.
- `design/README.md` does not document `.agents/plan/`, `contributing/`, or `.agents/`.
- No `research/` placeholder.
- References to external agent-guidelines are only in the cached `.agents/references/agent-guidelines/`, not yet integrated into design/ docs.
- `design/glossary.md` may need new terms (e.g., "plan step", "agent context", "bootloader").
- No ADR yet recording the adoption of the guidelines (see step 0007).

RFC 22 requires:
- ADR template using Nygard style.
- design/README explaining the folder.
- Glossary using subheading format.

Project hints and turn context require ensuring design/ is complete.

## Concrete Actions

1. Use `summarize` + `analyze` on existing ADRs and `design/README.md` to capture exact current state and template style.
2. Create `design/decisions/0000_adr-template.md`:
   - Use the Nygard style exactly as in existing ADRs (Status, Date, Deciders, Context, Decision, Consequences, Related, References).
   - Include instructions for authors.
3. Edit `design/README.md`:
   - Update the Directory Structure diagram to include:
     - `.agents/plan/` (agent-specific plans)
     - `contributing/` (top-level)
     - `.agents/` (top-level agent context, with subdirs)
   - Add a section "Relationship to Agent Guidelines and Plans" explaining how `.agents/plan/`, `.issues/`, `.agents/`, and cached references (under `.agents/references/agent-guidelines/`) work.
   - Mention that `.agents/references/agent-guidelines/` holds compacted/cached copies.
4. Optionally create `design/research/` with a `design/research/README.md` placeholder noting it is for background research.
5. Update `design/glossary.md` if needed (add project terms introduced by this structure upgrade).
6. Ensure all references in design/ use the compacted inlining pattern (point to summaries).
7. Use only `write`/`edit` + read tools. Verify with `tree` and `summarize`.

## Expected Artifacts

- `design/decisions/0000_adr-template.md`
- Updated `design/README.md`
- `design/research/README.md` (if added)
- Possibly updated `design/glossary.md`
- Cross-links in other design files if appropriate

## Verification

- `tree design`
- `summarize design/README.md`
- `summarize design/decisions/0000_adr-template.md`
- Confirm structure matches RFC 22 expectations.

## Related

- Step 0007 will add the adoption ADR (probably 0010 or next number).
- Step 0006 will create issues for this work.
- Step 0008 audit will re-verify.

## References

- Current `design/README.md`
- Existing ADRs (for template style)
- `.agents/references/agent-guidelines/rfcs/salotz.022_ai-coding-structure/README.md` (Design section)
- Turn context: "Ensure design/ is complete (add missing ADR template 0000, update README for .agents/plan/, contributing...)"
