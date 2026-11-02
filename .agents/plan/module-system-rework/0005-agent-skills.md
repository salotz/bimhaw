# Step 0005: Agent skills (no shipped modules)

**Status**: Not started — execution pending explicit user request

**Dependencies**: 0001 (vocabulary); ideally 0002–0004 so skills match reality

## Context

The user does not want a shareable module ecosystem. The replacement for “how do I configure git / mise / a prompt” is **skills** that an agent reads, then writes files in *that user’s* `lib/`.

Skills live with the project (RFC 22 `.agents/skills/` or `skills/`). Optionally later package them for install into a user’s agent dir — not required for v2.

## Concrete actions

1. Decide location: prefer `.agents/skills/bimhaw-*/SKILL.md` (agentskills.io-style) so Goose/other agents can load them; add a one-line index in `AGENTS.md` only after structure-plan allows.
2. Author skills:
   - **bimhaw-write-module** — layout, `module.toml` fields, slots vs phases, sh vs bash, idempotent env, “do not add autocomplete for directory-local tools.”
   - **bimhaw-edit-profile** — `PROFILES` shape, extends, regen (`profile gen` / `load`), never edit generated files.
   - **bimhaw-mise-safe** — strict layering; post-prompt activate snippet as an example to *copy*; XOR direnv; packslip vs static completion; `mise exec` for scripts.
   - **bimhaw-migrate-v1-lib** — mapping old paths → new; when to split/merge stems.
   - **bimhaw-doctor** — how to read doctor/profile show.
3. Each skill states: **do not publish or depend on third-party bimhaw modules; write them in the user’s lib.**
4. Example snippets in skills must be incomplete enough or clearly “paste into `$USER_LIB/mise/`” so they cannot be mistaken for shipped product modules.
5. No `src/bimhaw/lib/git` or similar.

## Expected artifacts

- Skill directories with `SKILL.md`
- This plan README skill table updated if names differ

## Verification

- `tree` on skills dir
- Skills mention post-prompt + mise XOR direnv
- `src/bimhaw/` still contains no user-module tree
