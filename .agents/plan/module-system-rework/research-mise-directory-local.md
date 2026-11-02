# Research: mise / direnv vs bimhaw env and autocomplete

**Date**: 2026-10-23  
**Status**: Supporting note for the module-system rework plan  
**Upstream**: mise v2026.10.x docs (GitHub `jdx/mise` `docs/`)

This is not an ADR. Decisions go in the plan README and later `design/decisions/`.

## Problem

bimhaw `env` and `autocomplete` modules are sourced once at shell startup from a **global** profile. Directory-local version managers change the meaning of “the kubectl on PATH” after `cd`. Static `source /usr/share/bash-completion/completions/kubectl` or `source <(kubectl completion bash)` at startup binds completions (and often PATH assumptions) to whatever was true in `$HOME`, not in the project.

## mise’s three invocation modes

From `docs/dev-tools/shims.md` and `docs/shell-setup.html` / `docs/cli/activate.md`:

1. **PATH activation** (`eval "$(mise activate bash)"`)  
   Hook (`hook-env`) runs on prompt and (bash) directory change. Puts **real** install dirs on PATH. Sets project `[env]`. Runs hooks. Packslip completions follow the active version.

2. **Shims** (`mise activate --shims` or `PATH` += `~/.local/share/mise/shims`)  
   Each *command* resolves version from cwd. **Does not** export project `[env]` into the interactive shell. **Does not** run enter/leave hooks. `command -v tool` succeeds even if the tool is not installed (`not_found_auto_install` may install on first run).

3. **`mise exec` / `mise run` / `mise env`**  
   No shell hook. Correct for scripts, CI, and this repo’s **project tooling** policy (DX plan: always `mise exec --`).

mise’s own recommendation: activate the **interactive** shell; use exec for scripts; use shims for editors that never read rc files.

## Completions (the sharp edge)

### Completions for mise itself

`mise completion bash --install` writes `~/.local/share/bash-completion/completions/mise`. Completes mise’s CLI, tools, versions, **and project task names** by asking mise at Tab time. Requires bash-completion enabled.

This is a reasonable **global** bimhaw autocomplete *or* a one-time `--install` the mise module can document. It is not version-of-kubectl.

### Completions for tools (packslip backend)

From `docs/dev-tools/packslip-resources.md` and `docs/cli/completion.md`:

- Only tools installed with the **packslip:** backend declare man/completions/skills per release.
- **With activate:** mise registers a loader; Tab reads the publisher script for the **currently active version**; leaving the project unregisters it. No reinstall after `cd`.
- **Without activate:** `mise completion bash --tool TOOL --install` writes a **stub that calls mise at completion time**, so the next Tab after `cd` / `mise use` uses that directory’s version.
- Generation may run the tool (`exec` source) on demand, cached per version; not at shell startup.
- Other backends (core, asdf, aqua, ubi, …) **do not** get this resource channel.

So: version-correct completions are a **mise feature for packslip tools**, not something bimhaw should duplicate. For `core:node` / aqua kubectl / etc., PATH is versioned under activate; completion scripts are not, unless the user uses a lazy generator after hook-env.

### Completions for everyone else

Typical user mistake (current bimhaw):

```bash
# lib/bash/autocomplete/kubectl.completion.bash — sourced at startup
source <(kubectl completion bash)
```

After `cd` into a project whose mise kubectl is a different major, bash still has the old completion functions. `complete -p kubectl` does not automatically refresh.

Available fixes (none of which bimhaw should fully own in v2):

| Approach | Who | Notes |
|---|---|---|
| Packslip + activate | mise | Best when the tool publishes packslip resources |
| `mise completion --tool` stub | mise | Manual; stub asks mise each Tab |
| `[hooks.enter] script = 'source <("$MISE_PROJECT_ROOT/bin/foo" completion bash)'` | project mise.toml | User/project owned; needs leave to `complete -r` if swapping |
| Lazy bimhaw helper at Tab time | possible later | High cost, per-tool generators |
| Static global completion | bimhaw module | **Only** if the binary is not directory-versioned |

## Hooks that run *in the current shell*

From `docs/hooks.md`:

```toml
[hooks.enter]
shell = "bash"
script = 'source "$MISE_PROJECT_ROOT/completions.sh"'

[hooks.leave]
shell = "bash"
script = 'complete -r foo 2>/dev/null; unset PROJECT_READY'
```

- `script` + `shell = "bash"` is injected into the activated shell (not a subprocess).
- mise **does not undo** script side effects; leave is mandatory for exports/complete.
- `run` / `shell = "bash -c"` is a **subprocess** and cannot change the interactive shell (useless for completions).
- Needs `mise activate`. Shims do not run these.

This is the supported escape hatch for project-only shell state. It is **not** a bimhaw module.

## direnv

From `docs/direnv.md`:

- mise can replace direnv for env/PATH/dotenv.
- **Running direnv and mise together is unsupported.** Hooks fight over PATH restore.
- `use mise` inside `.envrc` is deprecated and will be removed (mise 2027.10.4).
- If a user insists on direnv instead of mise: bimhaw’s post-prompt slot holds `eval "$(direnv hook bash)"` **xor** mise activate, never both.

direnv does not version tools by itself; people pair it with asdf/nix. Same layering rule: bimhaw does not parse `.envrc`.

## `command -v` / “is this installed?”

Shims: `command -v node` is true whenever the shim exists. PATH activation: `command -v` is true when that project’s (or global mise) node is actually on PATH.

bimhaw helpers used in **global** modules:

- Prefer `bimhaw_have` that resolves the real binary (readlink through shim, or `mise which` if mise is active) if we need “installed.”
- For “safe to source completion at startup,” the rule is simpler: **don’t**, if the name is a mise-managed tool.

## What other shells do (context only)

- Prezto/OMB/Bash-it: all assume global tools; none solve directory-local completions.
- Environment Modules / Lmod: load/unload **named software stacks**, not cwd. Different job.
- nix-direnv: another per-directory env; same XOR with mise activate.

## Implications for bimhaw v2 (summary)

1. Directory-local PATH/env/versioned completion is **mise’s (or direnv’s) job**.
2. bimhaw’s only first-class integration is a **post-prompt activate/hook line** in a *user-written* module, plus doctor warnings.
3. Autocomplete slot = global commands, or explicit lazy stubs, never “I assume kubectl is /usr/bin/kubectl.”
4. Do not grow a cwd watcher.
5. Skills must encode this so agents stop generating v1-style completion files for mise tools.

## Cached upstream paths

Fetched 2026-10-23 from `https://raw.githubusercontent.com/jdx/mise/main/docs/`:

- `shell-setup.md`
- `cli/activate.md`
- `cli/completion.md`
- `hooks.md`
- `direnv.md`
- `dev-tools/shims.md`
- `dev-tools/packslip-resources.md`

If those files move, prefer the live docs at https://mise.jdx.dev/ and update this note.
