# Plan Step 0006: Populate `.issues/` from Plan Steps

**Status**: Not Started

**Dependencies**: 0001–0005 (plan steps documented; some may be in progress)

## Context

The turn context and project instructions state:

> As we go along we will write out specific issues in the `.issues` directory as individual issues.
> Later: write individual issues for each plan step in .issues/ (e.g. using similar frontmatter to existing)

Current `.issues/` has one example:

```yaml
---
id: 1
title: Export profiles
status: open
priority: medium
labels:
    - enhancement
created: "2026-08-04"
updated: "2026-08-04"
---
```

This lightweight file-based tracker is used alongside the `plan/` for detailed steps.

RFC 20 (cached in rfcs) mentions repo issue trackers, but we follow the existing pattern here.

Each plan step should have a corresponding issue for trackable work.

## Concrete Actions

1. Use `summarize` on `.issues/0001-export-profiles.md` to confirm exact frontmatter format.
2. For each major plan step (0001 through 0010, or the actionable ones), create a new file in `.issues/`:
   - Use sequential IDs starting from 2 (or next available).
   - Frontmatter with: id, title, status (open), priority (medium/low), labels (e.g. `structure`, `documentation`, `agent-guidelines`), created/updated dates.
   - Body: Brief description linking back to the plan step file (e.g. `.agents/plan/000X-....md`).
   - Do **not** duplicate the full plan step rationale in the issue; keep issues concise.
3. Use `write` tool to create each issue file (e.g. `0002-update-agents-md.md`).
4. Optionally group or create sub-issues if a plan step is large.
5. Update the plan step documents to reference their issue ID.
6. After creation, use `tree .issues` and `summarize` to verify (no shell).

## Expected Artifacts

- Multiple new files in `.issues/`, one per plan step or major task.
- Cross-references updated in `.agents/plan/` files.
- Possibly an index or just rely on filenames + frontmatter.

## Verification

- `tree .issues`
- `summarize .issues/00XX-....md` for each
- Confirm frontmatter matches existing style exactly.

## Related

- This is the "as we go along" mechanism.
- Issues can later be used by humans or other tools.
- Step 0010 may define process for future plans.

## References

- Existing `.issues/0001-export-profiles.md`
- Turn context notes
- `.agents/references/agent-guidelines/rfcs/salotz.020_repo-issue-tracker.md` (if needed for future)
- `.agents/plan/README.md`
