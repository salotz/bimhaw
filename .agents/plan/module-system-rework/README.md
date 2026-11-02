# Plan: Module System Rework (profiles compose user modules)

**Status**: Plan Only — Do not execute until explicitly requested

**Date**: 2026-10-23

**Owner**: AI-assisted work (following current tasks in turn context)

**Related**:
- Design: `design/goals.md`, `design/glossary.md`, `design/architecture/overview.md`
- ADRs 0001–0009 (current-state module/profile/config debt)
- Landscape comparison (session): Prezto / Bash-it / Oh My Bash / shprofile / mise
- DX plan: [`.agents/plan/dx-modern-toolchain/`](../dx-modern-toolchain/README.md) — **mise as maintainer toolchain is a different layer** from mise as an *operator* directory-local tool. Do not collapse them.

This document lives under `.agents/plan/module-system-rework/`. It is the design-and-sequencing plan for a makeover of bimhaw’s **module and profile model**, in preparation for an implementation rewrite. Architectural choices made here must become ADRs in `design/decisions/` before code lands.

## Purpose

Replace the current “filename in a category folder, listed in many `config.py` dicts” model with:

1. **Modules as user-authored packages** (directory + manifest + slot files).
2. **Profiles as ordered compositions of those modules** (with `extends`, not duplicated lists).
3. **A generated, phase-aware loader** that still hides POSIX/bash startup.
4. **No shipped plugin catalogue.** Users (and their agents) write modules. bimhaw ships **skills**, not modules.
5. **A hard boundary with directory-local tool managers** (mise, and direnv only if the user is not using mise activate). Global `env` / `autocomplete` modules must not pretend project-local tools are global.

This is a product-model change. It is **not** the DX toolchain plan, **not** a multi-shell port, and **not** “become Oh My Bash.”

**Implementation of steps 0002+ is gated** on [testing-harness](../testing-harness/README.md) (comprehensive-makeover Phase B). Step 0001 (ADRs) may run in parallel. See [comprehensive-makeover](../comprehensive-makeover/README.md).

## Non-goals

- Shipping a community module/plugin registry, contrib tree, or “git clone this git module.”
- In-session profile switching / unload hooks (activation remains `active` symlink + new shells).
- First-class zsh/fish (sh + bash stay the product).
- Replacing mise/direnv. bimhaw will not grow a per-directory tool version manager.
- Running direnv and mise activate in the same shell (mise documents this as unsupported).
- Live-generating completions at every prompt for every tool (too slow, not our job).
- Changing the runtime-directory / symlink-indirection story except as needed by the new loader.
- Executing this plan until the user says to.

## Constraints (locked)

| Constraint | Meaning |
|---|---|
| User `lib/` is the only module source | No bundled `modules/git`, no pmodule-dirs for other people |
| Agents write modules | bimhaw ships **skills** that teach layout, slots, phases, mise-safety |
| Profiles remain the activation unit | One `active` profile; modules are composition units |
| Categories become **slots**, not the identity of a module | A `git` module may fill `aliases` + `funcs` + `autocomplete` |
| sh-inheritance stays | bash sources a module’s `sh/` files then `bash/` files |
| Generation stays | User intent in config; tool-owned startup in templates |
| Startup modes are loader business | User config must not be a spreadsheet of login vs interactive |
| Directory-local tools are not bimhaw modules | PATH, version, versioned completion, project `[env]` belong to mise (or direnv) |

## Current baseline (the thing being replaced)

Today a “module” is a **file in a role directory**:

```
lib/sh/envs/dev.sh
lib/sh/aliases/git.sh
lib/bash/autocomplete/git.completion.bash
lib/bash/prompts/salotz_dark.bash
```

A profile is many dictionaries keyed by profile × shell × startup mode × category (`SH_LOGIN_ENVS`, `BASH_INTERACTIVE_ENVS`, …). Generation inlines `for lib in $libs; do . …`. There is no manifest, no validation, no loader, no phases after prompt, no profile inheritance.

That model cannot express “git is one unit,” cannot hide login/interactive, and cannot tell a global `kubectl` completion from the kubectl that mise just put on PATH for this repo.

## Target model

### Module = directory + manifest + optional slot files

User library (source of truth, usually outside `~/.bimhaw`, symlinked in as today):

```
lib/
  git/
    module.toml
    README.md                 # optional
    sh/
      aliases.sh
      funcs.sh
    bash/
      completion.bash         # only if git is a *global* install
  prompt-salotz-dark/
    module.toml
    bash/
      prompt.bash
  mise/
    module.toml
    bash/
      activate.bash           # eval "$(mise activate bash)" — post-prompt only
  core/
    module.toml
    sh/
      env.sh                  # BIMHAW_* helpers live in tool runtime, not here
```

**bimhaw does not ship `lib/git` or `lib/mise`.** The trees above are what a skill would *write for the user*. The tool may ship a tiny **runtime** (`env.sh` helpers, generated `load_module`) that is not a user module.

Suggested `module.toml`:

```toml
name = "git"
summary = "git aliases and functions"
shells = ["sh", "bash"]
slots = ["aliases", "funcs"]     # no autocomplete: git version may be project-local
after = ["core"]
# optional:
# scope = "global"               # default; see directory-local section
```

Missing slot files for declared slots are a generation error. Extra files are ignored or warned. `name` must match the directory.

### Profile = name + extends + ordered modules + options

Replace the 14 dictionaries with something the user (or agent) can actually maintain:

```python
PROFILES = {
  "common": {
    "modules": ["core", "git", "mise"],
    "prompt": "prompt-salotz-dark",
    "options": {
      "mise": {"mode": "activate"},   # not shims; see 0004
    },
  },
  "work": {
    "extends": "common",
    "modules": ["ssh-work"],
  },
  "recovery": {
    "modules": ["core"],
    "prompt": None,
  },
}
```

Resolution rules (to be ADR’d):

- `extends` is single-parent for v2 (mixins later if needed).
- Child module list **appends** unless a module is listed again (reorder) or prefixed with `-name` / `exclude` (drop). Exact syntax is an ADR; do not invent three ways.
- `prompt` is a module that fills the `prompt` slot, not a parallel type. Scalar in profile config is sugar for “load this module in the prompt phase.”
- Options are data injected at generation (env vars or a generated `module.options.sh`). Modules must tolerate missing options.

Login vs interactive vs logout **do not appear in this file.**

### Slots and phases (loader vocabulary)

**Slots** are what a module *contains* (the old categories, plus one hole from ADR-0009):

| Slot | Typical content | Default phase |
|---|---|---|
| `env` | exports, PATH for *global* tools, umask | login + nonlogin env (idempotent) |
| `funcs` | shell functions | interactive (and login-interactive) |
| `aliases` | `alias` | interactive |
| `prompt` | PS1 / prompt command setup | prompt |
| `post_prompt` | wrappers that must run *after* prompt (mise activate, direnv, Eat, history `-a`) | post-prompt |
| `autocomplete` | bash completion for **globally installed** commands | autocomplete (after post-prompt) |
| `logout` | logout actions | logout |

**Phases** are when the generated profile sources those files, and are owned by templates:

1. env (login and/or nonlogin, as the invocation requires)
2. funcs
3. aliases
4. prompt
5. **post-prompt**
6. autocomplete
7. logout (logout path only)

`after` in the manifest orders modules *within* a phase. It does not let a module jump phases.

sh-inheritance: for bash, each module contributes `sh/` then `bash/` for the slots that apply to this invocation.

### Generated loader (keep generation, stop inlining 15 loops)

Generated profile scripts stay thin and auditable, but they call a small `bimhaw_load` rather than string-splitting lists.

Runtime helpers live in the generated/`env.sh` runtime (tool-owned, not a user module):

- `bimhaw_have cmd` — must not treat a mise **shim** as “the tool is installed” (`command -v` lies when shims are on PATH)
- `bimhaw_is_interactive` / `bimhaw_is_login`
- `bimhaw_log debug|warn|error`
- `bimhaw_load <module> <slot>` — test `-f`, source once, record in `BIMHAW_LOADED`

Search path for v2: **user `lib/` only.** Extra dirs are out of scope unless a later ADR needs a user’s own overlay (still not sharing).

### What bimhaw ships vs what the user writes

| Shipped in the **tool** | Written in the **user lib** (by human or agent) |
|---|---|
| CLI, templates, generation, `env.sh` runtime helpers | Every module |
| `bimhaw doctor` / `module list` / `profile show` | `config.py` (or successor) |
| **Agent skills** describing how to write modules, wire profiles, stay mise-safe | Optional per-user README in a module |
| Default empty profile + empty `lib/` on init | Prompts, aliases, mise activate snippet |

Init still scaffolds `lib/` directories (or the new layout) and a stub config. It does **not** copy a git/kubectl/docker module in.

## Directory-local tools (mise, direnv)

This is a first-class design problem, not a footnote. Current `env` and `autocomplete` modules assume a command is the same binary every directory. That is false once mise (or direnv+asdf, or nix-direnv) is in play.

### What mise actually does (operator shell)

Documented by mise (see [research note](research-mise-directory-local.md)):

| Mechanism | PATH / version | Project `[env]` | Completions follow version | Hooks (enter/leave) | When to use |
|---|---|---|---|---|---|
| `eval "$(mise activate bash)"` | Real tool dirs, updated on cd/prompt via `hook-env` | Yes | Packslip tools: yes, if activated | Yes | **Interactive shell (recommended)** |
| `mise activate --shims` / shims on PATH | Shim resolves version **per invocation cwd** | **No** (child sees env, shell does not) | Weak | **No** | Editors, programs that never read rc files |
| `mise exec -- cmd` / `mise run` | For that command | For that command | n/a | n/a | Scripts, CI, **project tooling** (bimhaw’s own DX plan already requires this) |

Further facts that constrain bimhaw:

- Completions for **mise itself**: `mise completion bash --install` (or print + source). Independent of tool versions.
- Completions for **packslip-backend tools**: follow the version active in the current directory. With activate, mise registers a loader and swaps scripts on cd. Without activate, `mise completion bash --tool TOOL --install` writes a **stub that asks mise at completion time**.
- Project-specific shell snippets (source a completion, set a shopts): mise `[hooks.enter] script = '...'` with `shell = "bash"`, and a matching `leave` to undo. mise does **not** undo scripts for you.
- **direnv + mise activate together is unsupported.** If a user wants directory-local env without mise, direnv is the alternative — not a second hook beside mise.
- Shims make `command -v node` succeed even when node is not installed. Any bimhaw `have` helper that uses `command -v` will mis-detect tools.

Packslip versioned completions are the only mise-native answer to “this project’s kubectl is 1.29, that one is 1.31, don’t source a global completion file.” Tools **not** installed via packslip do not get this for free; they get PATH (activate) and whatever `kubectl completion bash` emits **now**, which is only correct if you run it **after** hook-env for this directory — i.e. at completion time or in an enter hook, not at shell startup.

### The architectural split

```
bimhaw profile (global, per-user identity)
  ├── aliases, functions, prompt, logout
  ├── env for truly global things (EDITOR, umask, locale, user PATH prefixes)
  ├── autocomplete for truly global commands (or dynamic stubs)
  └── a single "activate directory-local manager" module  →  post-prompt
        │
        ▼
mise activate / direnv hook   (per-directory)
  ├── tool versions on PATH
  ├── project [env]
  ├── version-matched completions (packslip or --tool stubs)
  └── optional enter/leave scripts for project-only shell state
```

**bimhaw composes the user’s shell. mise/direnv compose the project’s toolchain.** A bimhaw module that `source <(kubectl completion bash)` at startup is a bug once kubectl is project-local.

### Solutions available (ranked)

**1. Strict layering (v2 default — do this)**

- bimhaw never installs, versions, or completes project-local tools.
- The user’s `mise` module (written via skill, not shipped) only:
  - ensures `mise` is on PATH at interactive start (absolute path if needed, as mise’s own shell-setup warns),
  - `eval "$(mise activate bash)"` in **post-prompt** (so it cannot be clobbered by prompt `PROMPT_COMMAND` assignment),
  - does **not** use `--shims` for the interactive shell.
- Autocomplete slot in bimhaw is documented as **global-only**.
- Skills tell agents: if the tool is in `mise.toml` `[tools]`, do not write a bimhaw `autocomplete` file for it; use mise activate + packslip/`--tool` stubs / enter-hook.
- Project-only aliases that depend on a tool version belong in mise `[hooks.enter] script` or mise shell-aliases, not in bimhaw `aliases`.

This matches mise’s own split and matches this repo’s DX plan (project recipes use `mise exec`, operator activate is optional). bimhaw’s job is to make the *optional operator activate* correct and phase-safe.

**2. Dynamic completion stub (optional later, not v2-blocking)**

A helper `bimhaw_complete_lazy cmd` that at **Tab time** locates `cmd` on the current PATH (post-hook-env) and invokes that binary’s completion generator, or falls back to a cached script keyed by `$(command -v cmd)` realpath.

- Pros: works for non-packslip tools whose completion is version-specific.
- Cons: every tool has a different generator CLI; slow; easy to get wrong; duplicates what packslip already does for participating tools.
- Decision: document as a possible user-module pattern / later helper; **do not** build a completion framework in v2.

**3. mise enter-hook for project shell files (escape hatch, user-owned)**

For a repo that really needs `source "$MISE_PROJECT_ROOT/extras.bash"`:

```toml
# in the *project* mise.toml — not bimhaw
[hooks.enter]
shell = "bash"
script = 'source "$MISE_PROJECT_ROOT/completions.sh"'

[hooks.leave]
shell = "bash"
script = '# undo if you exported anything'
```

bimhaw does not generate these. Skills should mention the pattern so agents do not stuff project files into `lib/`.

**4. Shims-only operator (supported but second-class)**

If the user refuses activate: shims give versioned **executables**, not versioned **shell state**. Completions sourced at bimhaw startup will still be the global/first-on-PATH ones. Doctor should warn: “profile has static autocomplete for X and mise shims are on PATH.”

**5. Rejected: project-local bimhaw overlays**

A `.bimhaw/` in the repo, or “modules from mise.toml,” would make bimhaw a worse direnv. Out of scope. Profiles are per-user environment, not per-repo.

**6. Rejected: bimhaw reimplements hook-env**

Do not watch cwd, do not parse `mise.toml`, do not mutate PATH on cd.

### Consequences for slots

| Slot | Global (bimhaw module) | Directory-local (mise/direnv) |
|---|---|---|
| `env` | EDITOR, locale, user bin, `BIMHAW_*` | `mise.toml` `[env]`, tool install dirs |
| `autocomplete` | commands guaranteed global (or lazy stub) | packslip / `mise completion --tool` / enter script |
| `post_prompt` | **the activate/hook line** | hook-env runs from here on |
| `aliases` / `funcs` | user workflow, tool-agnostic or global tools | project-only: mise shell-aliases or enter script |
| `prompt` | user prompt | may *read* project env (git, mise env) but should not assume a tool version |

`scope = "global"` in the manifest is documentation and doctor-fodder, not a runtime sandbox. Doctor can warn if an `autocomplete` module names a binary that is also a known mise shim.

### Interaction with this repo’s DX plan

`.agents/plan/dx-modern-toolchain` already decided: **in-repo tooling uses `mise exec`**, operator activate is optional. The product rework must not require activate for bimhaw *development*. It **may** help users who *choose* activate as their interactive setup, which is the common case this section exists for.

## Agent skills (instead of modules)

Ship skills with the bimhaw repo / package (e.g. `.agents/skills/` in this project, and/or packaged skill files the user can copy into their own agent dir). Skills are documentation-for-agents, not shell code.

Minimum set (step 0006):

| Skill | Teaches |
|---|---|
| `bimhaw-write-module` | Directory layout, `module.toml`, which slots to use, sh vs bash, idempotent `env` |
| `bimhaw-edit-profile` | Add/remove/reorder modules, `extends`, options, regen + load |
| `bimhaw-mise-safe` | Strict layering; post-prompt activate; never static-complete mise tools; `bimhaw_have` vs shims |
| `bimhaw-migrate-v1-lib` | Map `lib/sh/aliases/git.sh` → `lib/git/sh/aliases.sh` + stub manifest |
| `bimhaw-doctor` | How to interpret `bimhaw doctor` / `profile show` |

Consumer-facing “this shell is bimhaw / prompt legend / `bimhaw explain`” is **not** this list. See [agent-explainability](../agent-explainability/README.md) (`bimhaw-shell`).

Skills must say **do not invent a shared module ecosystem**. If the user wants git aliases, write them in *their* `lib/git`.

## Config representation

ADR-0007 (`exec` of `config.py`) is still allowed as a **loader** in v2 if the *shape* of the file changes. Prefer:

- Still Python (no new DSL), but one `PROFILES` mapping + maybe `DEFAULTS`.
- Validate against a schema after `exec` (pydantic or a small dataclass layer). Typos in module names fail at `profile gen`, not at the next login.
- Do not require TOML for profiles unless an ADR argues it; manifests as TOML is enough new syntax.

## Migration

v1 layout remains readable for one major version:

- Generator accepts old `lib/sh/aliases/foo.sh` **or** new `lib/foo/sh/aliases.sh`.
- `bimhaw migrate lib` (or a skill-guided edit) rewrites the tree and synthesizes `module.toml` from which directories had files.
- Old `config.py` dicts: a one-shot convertor groups names by stem (`git` in aliases + autocomplete → one module with two slots). Ambiguous stems stay as separate modules; do not guess.
- After migration, old keys are rejected with a pointer to the skill.

## CLI additions (product, not DX)

Keep existing: `profile gen`, `profile load`, `link-shells`, init.

Add:

- `bimhaw doctor` — active profile, config vs generated hash, missing slot files, symlink health, **mise/direnv conflict**, static autocomplete vs shims
- `bimhaw module list` — scan user `lib/`
- `bimhaw profile show [--name]` — resolved module list after `extends`

No `bimhaw enable git`. There is nothing to enable in a catalogue.

## ADRs to write before implementation (step 0001)

1. **Module as user package** — directory + manifest + slots; no shipped modules.
2. **Profile composition** — `extends`, ordered modules, options; hide login/interactive.
3. **Phases and post-prompt** — including why mise/direnv/Eat live there.
4. **Directory-local boundary** — strict layering with mise; direnv XOR mise activate; no project overlays.
5. **Skills not plugins** — what the tool ships for agents.
6. **Config schema** — successor to ADR-0007’s temporary `exec` dicts (may still `exec`, must validate).

## Implementation sequence (execution later)

See numbered steps in this folder. Summary:

| Step | Focus |
|---|---|
| [0001](0001-adrs.md) | Write ADRs; freeze vocabulary in `design/glossary.md` (**allowed during harness work**) |
| [0002](0002-config-and-layout.md) | New layout + profile schema + validation — **after testing-harness gate** |
| [0003](0003-loader-and-phases.md) | Templates + `bimhaw_load` + post-prompt; sh-inheritance; **update v1 snapshots** |
| [0004](0004-directory-local-boundary.md) | Doctor checks; skill + docs for mise; helpers shim-aware |
| [0005](0005-agent-skills.md) | Author the skills; no example modules that look “official” |
| [0006](0006-migration.md) | v1 → v2 lib/config convertor; keep v1 tests until this is proven |
| [0007](0007-doctor-and-show.md) | Introspection CLI |
| [0008](0008-verify.md) | **v2** tests (resolver, migrate, doctor) on top of the harness; no full shell matrix |

Steps 0002–0003 are the makeover. 0004 is the mise contract. 0005 is the substitute for a plugin dump. 0006 unblocks existing user libs (`~/.salotz.d`).

## Risks

- **Over-manifesting.** Keep `module.toml` tiny. If a slot file exists, that is enough to fill the slot; the manifest is identity + `after` + declared shells.
- **Agents writing global kubectl completions anyway.** The mise-safe skill and doctor warning are the mitigation; the tool cannot stop a user module from sourcing things.
- **PROMPT_COMMAND races.** Post-prompt must be generated even if no module uses it, so mise/direnv have a stable hook point.
- **Double activate.** If the user also added `eval "$(mise activate bash)"` to a raw bashrc that bimhaw replaced, fine; if they add it *inside* a bimhaw `env` slot *and* post-prompt, doctor should detect duplicate activate.

## References

- This folder: [research-mise-directory-local.md](research-mise-directory-local.md)
- mise: [Shell setup](https://mise.jdx.dev/shell-setup.html), [activate](https://mise.jdx.dev/cli/activate.html), [shims](https://mise.jdx.dev/dev-tools/shims.html), [hooks](https://mise.jdx.dev/hooks.html), [packslip resources](https://mise.jdx.dev/dev-tools/packslip-resources.html), [direnv migration](https://mise.jdx.dev/direnv.html)
- Prezto `pmodload` / `.zpreztorc` pmodule list (module-as-package, not catalogue)
- Bash-it load phases / doctor (operability, not plugins)
- ADR-0009 post-prompt hole

---
*Plan only. Create `.issues/` items and ADRs when execution is requested.*
