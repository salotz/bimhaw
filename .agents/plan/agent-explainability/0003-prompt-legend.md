# Step 0003: Prompt legend (`explain prompt`)

**Status**: Not started — execution pending explicit user request

**Dependencies**: 0001–0002

## Context

User PS1 example (not shipped):

```
*** salotz@dtn101.ccs.ornl.gov [/lustre/orion/bip294/proj-shared/workflow_execution_cd1-2]
{Fri Oct 23 11:50:05} !1034 #41 [2] 128:
-->
```

bimhaw must **not** hardcode a decoder for this. The prompt **module** owns `explain.md` as the legend.

## Concrete actions

1. `bimhaw explain prompt`:
   - names the active prompt module / v1 prompt filename (`BASH_PROMPT` / `SH_PROMPT`)
   - prints shipped one-liner: PS1 is not from distro bashrc; it is this module
   - dumps that module’s `explain.md`
   - if missing: template of headings (`user@host`, `cwd`, `time`, `hist`, `cmdcount`, `jobs`, `exit`, `other`) for the user to fill
2. Optional env `BIMHAW_PROMPT_ID` documented; if set, prefer it over config when they diverge (warn).
3. Skill `bimhaw-shell` includes the ORNL-like example as **one user’s** layout with a guessed legend clearly marked **illustrative** — agents must prefer `explain prompt` over the guess.
4. Do not change prompt templates except a comment pointer `# legend: bimhaw explain prompt`.

## Expected artifacts

- `explain prompt` behavior
- Heading template for empty legend
- Skill example paragraph (in 0004)

## Verification

- Switching `BASH_PROMPT` in isolated config changes which explain file is used
- No regex of PS1 in Python
