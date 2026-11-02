# Plan: Agent Explainability (`bimhaw explain`, prompt legend, host context)

**Status**: Plan Only — Do not execute until explicitly requested

**Date**: 2026-10-23

**Owner**: AI-assisted work

**Umbrella**: sibling of [comprehensive-makeover](../comprehensive-makeover/README.md), **not** gated on the testing harness except where a new CLI needs tests. Do **not** fold this into module-system-rework 0005 (those skills teach *authors*; these teach *consumers* of a live shell).

**Related**:
- Module packages + `explain.md` on modules: [module-system-rework](../module-system-rework/README.md)
- RFC 23 host context: `~/.config/agents/shell.md` ([summary](../../references/agent-guidelines/summaries/salotz-rfc-023-local-agent-context.md))
- Goose (verified 2026-10-23 against goose-docs.ai): skills, `.goosehints`, `@` includes — see [research-goose-injection.md](research-goose-injection.md)

## Purpose

bimhaw is not a stock `.bashrc`. Agents (Goose `@goose`, paste-into-chat transcripts, other coding agents) see:

1. A **structured PS1** that encodes host/path/time/history/jobs/exit — opaque unless documented.
2. Generated thin scripts + `~/.bimhaw/active` + user `lib/` — they will grep `$HOME` and get lost.
3. Modules with no human-readable contract beyond filenames.

This plan adds **explainability as a product surface**:

- A CLI that prints **generated, current** text (`bimhaw explain …`).
- A place for **users** (and their agents) to write per-module / per-prompt explanations.
- **Host-wide** agent context and a **skill** that say: “this shell is bimhaw; here is the prompt legend; run `bimhaw explain` instead of spelunking rc files.”

bimhaw still ships **no prompt theme** and **no module catalogue**. The ORNL-style prompt in the request is a *user* prompt module; bimhaw ships the *mechanism* to explain whatever is active.

## Non-goals

- Shipping a default rice PS1 or the user’s `*** user@host … -->` format.
- Putting the full legend in PS1 (ugly, token-heavy in every paste).
- Goose persistent instructions (`GOOSE_MOIM_MESSAGE_*`) for this — too expensive per turn.
- Teaching agents to parse PS1 with regex as the primary API (legend + `explain` is the API; regex is a fallback in the skill).
- Replacing `doctor` / `profile show` (those stay machine-oriented; `explain` is prose for humans/agents).
- Auto-injecting into every agent product on earth — ship files agents *can* install; RFC 23 + Goose are the first-class targets.

## Problem split

| What the agent sees | What it needs | Who owns the text |
|---|---|---|
| Prompt like `*** salotz@dtn101… [2] 128:` | Field legend | **Prompt module** `explain.md` (user) + skill that says “look up the active prompt module” |
| “Why is PATH / alias / kubectl completion like this?” | Active profile, modules, phases, mise boundary | **`bimhaw explain`** generated from live config + module explain files |
| “This isn’t `.bashrc`” | 20-line bimhaw map | **Shipped** skill + RFC 23 `shell.md` snippet |
| Pasted snippet in a GitHub issue | Same as prompt + `explain --paste` | CLI |

## Suggestions (locked into this plan)

### 1. Do not decode the prompt in bimhaw core

The example:

```
*** salotz@dtn101.ccs.ornl.gov [/lustre/orion/bip294/proj-shared/workflow_execution_cd1-2]
{Fri Oct 23 11:50:05} !1034 #41 [2] 128:
-->
```

is **user PS1**. Likely fields (for the *skill’s example*, not code): user@host, cwd, timestamp, history `!`, command counter `#`, job count `[n]`, last exit, continuation `-->`. Only the author of that prompt module can confirm (`#41` vs SHLVL, `***` vs profile marker, etc.).

**Product rule:** the active **prompt module** carries `explain.md` (or `legend.md`) written by the user. `bimhaw explain prompt` concatenates:

- shipped one-liner: “PS1 comes from the prompt slot of the active profile, not from `.bashrc`.”
- that module’s `explain.md` if present, else “no legend; add `explain.md` next to the prompt files.”

A skill may include this example as *illustration* clearly marked “one user’s prompt, not bimhaw’s.”

### 2. `bimhaw explain` is the agent API

Commands (names can shift in an ADR; verbs stay):

| Command | Output |
|---|---|
| `bimhaw explain` | Short stack: this is bimhaw; `BIMHAW_DIR`; active profile; how to go deeper |
| `bimhaw explain prompt` | Prompt-module legend |
| `bimhaw explain profile [name]` | Resolved modules (after `extends` once that exists), phases, options |
| `bimhaw explain module <name>` | Manifest + `explain.md` + which slots/files load |
| `bimhaw explain startup` | Login vs interactive vs `$ENV` in **prose**, pointing at generated files not POSIX man |
| `bimhaw explain --paste` | Compact bundle for bug reports: prompt legend + profile + `doctor`-ish facts (no secrets) |

`--format text|md|json`. Default **md** for agents. JSON for tooling. Never dump module *source* unless `--source`.

v1 (current dict config) can still explain: active profile, lists per category, path to lib files. Richer once module packages exist. **Do not wait for the whole makeover** to ship a useful v1 `explain`.

### 3. How users write explanations

Per module directory (v2 layout) or beside v1 files:

```
lib/git/
  module.toml          # summary = "…"  (one line, also used by `module list`)
  explain.md           # agent/human prose: what it does, side effects, mise-safety
  sh/aliases.sh
```

Prompt module:

```
lib/prompt-salotz-dark/
  module.toml
  explain.md           # THE legend for PS1 fields
  bash/prompt.bash
```

v1 fallback: `lib/bash/prompts/foo.explain.md` next to `foo.bash`, or a `explain/` tree. Prefer one convention in v2; v1 migrate copies `*.explain.md`.

**`summary` is required-enough for doctor; `explain.md` is optional.** Missing explain → `bimhaw explain module git` prints paths and “no explain.md.”

Skills (`bimhaw-write-module`) tell authoring agents to fill `explain.md` when the module affects PATH, completions, or PS1.

Do **not** generate explain.md from the shell script with an LLM at runtime. Authors write it; `explain` only concatenates.

### 4. Host-wide injection (RFC 23 + Goose)

Two layers, both **short pointers**, not a dump of every module:

**A. RFC 23 `~/.config/agents/shell.md`** (host, all agents)

Ship a **snippet** the user (or a `bimhaw context install` later) copies:

- This account’s interactive bash is managed by **bimhaw**, not raw `.bashrc`.
- Do not edit `~/.bashrc` / generated files under `~/.bimhaw/profiles/`.
- Source of truth: user `config.py` + `lib/` (paths as configured).
- Structured PS1: run `bimhaw explain prompt`.
- Troubleshooting: `bimhaw explain`, `bimhaw doctor` (when it exists), `bimhaw explain startup`.
- Directory-local tools: mise/direnv, not bimhaw modules (one sentence + pointer).

**B. Goose-specific**

Verified mechanisms (see research note):

| Mechanism | Use here |
|---|---|
| Global skill `~/.agents/skills/bimhaw-shell/SKILL.md` | **Primary.** Description must mention PS1 patterns, bimhaw, `~/.bimhaw`, pasted prompts, troubleshooting rc files so Goose *loads* it when those appear. |
| Global `.goosehints` `~/.config/goose/.goosehints` | 5–15 lines + `@` include of a **small** static file *or* “run `bimhaw explain`”. Do not `@` a 50 KB generated dump every session. |
| `CONTEXT_FILE_NAMES` | Optional: treat `AGENTS.md` already; do not require Goose-only filenames in `$HOME`. |
| `GOOSE_MOIM_MESSAGE_*` | **Do not use** for explain text. |
| Custom `system.md` | **Do not use** for bimhaw. Too global. |
| Project `.agents/skills/` in the **bimhaw repo** | Skills for *developing* bimhaw (write-module, etc.). Different audience. |

Goose skill `description` is the discovery hook. It should mention: structured prompt, `user@host`, `~/.bimhaw`, “not a normal bashrc”, `bimhaw explain`.

**`@` in Goose hints** includes file content at session start. Use it for a **stable short** `~/.config/agents/shell.md` (RFC 23), not for generated explain output (goes stale when you `profile load`).

Agents in a **pasted transcript** never see goosehints. The **skill description + `explain --paste` habit** covers that: humans paste prompt + `bimhaw explain --paste`.

### 5. Optional: `bimhaw context install`

A later CLI that writes/updates:

- `~/.config/agents/shell.md` (merge or create)
- `~/.agents/skills/bimhaw-shell/SKILL.md` (copy from package data)
- optional append to `~/.config/goose/.goosehints` if that file exists

Idempotent, `--dry-run`. Not Phase 1. Document the copy-paste until then.

### 6. Prompt module convention (for the user’s own lib)

Recommend (in the skill, not enforced):

- Keep PS1 **dense**; keep the legend in `explain.md`.
- If a field is ambiguous, name it in the legend (`#N` = commands this session, not SHLVL).
- Optional: `export BIMHAW_PROMPT_ID=prompt-salotz-dark` so `explain prompt` does not guess.
- Optional: a comment as the first line of `prompt.bash`: `# bimhaw-explain: see explain.md` — agents that open the file get a pointer.

Do not add OSC-8 or hidden PS1 payloads for agents.

## Phasing vs the makeover

| When | What |
|---|---|
| Anytime (even v1) | Shipped skill text + RFC 23 snippet in this repo (`docs/` or `.agents/skills/`) |
| After testing-harness isolation | `bimhaw explain` v1: profile name, dict lists, paths, prompt file path |
| With module packages (rework 0002) | Read `explain.md` / `summary` from module dirs |
| After doctor (rework 0007) | `explain --paste` includes doctor facts |
| Optional later | `bimhaw context install` |

Does **not** block Phase B (tests) or require post-prompt. Complements module-system 0005 (author skills) with **consumer** skills.

## Steps

| Step | Focus |
|---|---|
| [0001](0001-explain-command.md) | `bimhaw explain` v1 CLI + `--format` |
| [0002](0002-module-explain-files.md) | Convention for `explain.md` / `summary`; v1 fallback paths |
| [0003](0003-prompt-legend.md) | `explain prompt`; prompt-module legend; no shipped PS1 |
| [0004](0004-skills-and-host-context.md) | `bimhaw-shell` skill, RFC 23 snippet, Goose hints recipe |
| [0005](0005-paste-and-json.md) | `--paste`, `--format json` |
| [0006](0006-context-install.md) | Optional installer into `~/.config/agents` and `~/.agents/skills` |

0004’s **content** can be written in-repo before 0001 exists (skill can say “run bimhaw explain when available”).

## Success

- An agent given only the PS1 paste + the skill description knows to call `bimhaw explain prompt` / read `explain.md` instead of inventing field meanings.
- An agent debugging “alias missing” is told not to edit `.bashrc` and to use `bimhaw explain profile`.
- Users can document a prompt without bimhaw knowing the glyphs.
- Token cost stays low: hints are short; full explain is on demand.

## Risks

- Stale generated explain files if someone `@`s them in goosehints — **forbid** that in the skill.
- Users never write `explain.md` — CLI still prints paths; doctor can nag only for **prompt** modules.
- Goose skill not loaded because description is vague — spend effort on `description`.
- Secrets in explain.md (tokens in env modules) — skill says never; `explain` does not dump env values.
