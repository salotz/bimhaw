# Plan Step 0009: Update Other Documentation for Consistency

**Status**: Not Started

**Dependencies**: 0001–0008 (core structure landed and audited)

## Context

After adopting the new layout, other documentation must be updated so the structure is discoverable and consistent:

- Root `README.org` (user-facing)
- `design/goals.md` (may need to mention process/structure goals)
- Existing ADRs (especially ADR-0009 limitations, and the new adoption ADR)
- `design/glossary.md` (new terms)
- Possibly `docs/`, `setup.py`, or other files if they mention structure
- Any mentions of "contributing" or guidelines

RFC 22 encourages that design/ and contributing/ content is dual-use.

Guidelines require using compacted references.

Project hints: "Follow RFC22 project layout... Update AGENTS.md... Create top-level contributing/..."

Cross-references should point to `.agents/plan/`, `contributing/`, `.agents/`, `.agents/references/agent-guidelines/`.

## Concrete Actions

1. Use `summarize` on `README.org` (key sections already partially known from prior work).
2. Use `summarize` on `design/goals.md`, `design/glossary.md`, and relevant ADRs.
3. Identify places that should reference the new structure:
   - In README.org: add a short "For Contributors / AI Agents" section pointing to `AGENTS.md`, `contributing/`, `.agents/plan/`, `design/`.
   - In `design/goals.md`: consider adding a principle or note about following external agent guidelines / professional structure.
   - In `design/glossary.md`: add entries for new terms introduced (e.g. "bootloader", "plan step", "agent context", ".agents", "contributing/").
   - In the new adoption ADR and ADR-0009: ensure cross-links.
   - Check for any hardcoded paths or old assumptions.
4. Make minimal, targeted `edit` or `write` updates. Prefer small precise edits.
5. Add compacted summary references where external standards are mentioned.
6. Use only task tools for inspection and changes.
7. Update this plan step with a summary of changes made.

## Expected Artifacts

- Updated `README.org`
- Updated `design/goals.md` (if applicable)
- Updated `design/glossary.md`
- Possibly minor updates to existing ADRs or other docs
- Log of changes in this step file

## Verification

- `summarize` on the changed files to confirm additions.
- `tree` on root and design/ to confirm no breakage.
- Re-audit key links if needed (step 0008 style).

## Related

- Adoption ADR (0007)
- Full verification (0008)
- Maintenance process (0010)

## References

- `README.org`
- `design/goals.md`, `design/glossary.md`
- RFC 22 summary (dual-use docs)
- Turn context requirements for following RFC22
