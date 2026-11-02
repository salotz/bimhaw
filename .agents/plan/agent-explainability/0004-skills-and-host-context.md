# Step 0004: Skills and host-wide context snippets

**Status**: Not started — execution pending explicit user request

**Dependencies**: None for **writing** files in this repo; 0001 for the skill to mention real CLI flags.

## Audience

**Consumers** of a bimhaw-managed *login shell* (Goose on a cluster, agent in a pasted bug). Distinct from module-system 0005 **author** skills.

## Concrete actions

1. In the **bimhaw repo**, author:
   - `.agents/skills/bimhaw-shell/SKILL.md` (or `skills/bimhaw-shell/` if packaging requires) — **global install target** `~/.agents/skills/bimhaw-shell/`
   - `docs/agent-context/shell.md` (or similar) — RFC 23 snippet to copy to `~/.config/agents/shell.md`
2. Skill frontmatter (Goose / agentskills.io):
   - `name: bimhaw-shell`
   - `description:` must include: bimhaw, `~/.bimhaw`, structured bash PS1, pasted prompts, `user@host`, troubleshooting bashrc, `bimhaw explain`
3. Skill body:
   - When you see a dense PS1 or `~/.bimhaw`, this shell is bimhaw-managed
   - Do not edit `~/.bashrc` / generated profiles; edit user `lib/` + config, then `profile gen/load`
   - Run `bimhaw explain` / `explain prompt` / `explain profile`
   - Prompt fields: trust `explain prompt` / module `explain.md`; illustrative decode of the ORNL-style example as last resort
   - mise-managed tools are not bimhaw modules
   - For bug reports: ask the user for `bimhaw explain --paste` (or the v1 equivalent until 0005)
   - `@file` in Goose hints is not related to `user@host` in PS1
4. RFC 23 snippet: ≤40 lines, pointers only, no full architecture.
5. Goose hints recipe (in skill): append 5 lines to `~/.config/goose/.goosehints` including `@~/.config/agents/shell.md` **if** that file exists. Do not instruct `@` on generated explain.
6. Do **not** set `GOOSE_MOIM_MESSAGE_*` or customize `system.md`.
7. Repo-level skill is for bimhaw **developers** too if they use Goose in this checkout; global copy is what cluster/desktop sessions need.

## Expected artifacts

- Skill + RFC 23 snippet in-repo
- Cross-link from module-system 0005: “consumer skill is bimhaw-shell”

## Verification

- Skill YAML has `name` and `description`
- Description grep: `bimhaw`, `explain`, `prompt` or `PS1`
- No instruction to use persistent MOIM

## Goose docs cited

- https://goose-docs.ai/docs/guides/context-engineering/using-skills
- https://goose-docs.ai/docs/guides/context-engineering/using-goosehints
- https://goose-docs.ai/docs/guides/context-engineering/using-persistent-instructions
