# Architecture Overview

This document provides a high-level view of bimhaw's architecture as it exists today. It describes the major components, their relationships, and the flow of configuration from user source to active shell environment.

## Goals of the Architecture

- Abstract away the legacy complexity of POSIX and bash shell startup sequences.
- Support multiple distinct, switchable shell environments ("profiles").
- Encourage modular, maintainable configuration through small focused scripts ("modules").
- Separate user configuration (source of truth) from generated runtime artifacts.
- Allow the core tool logic to evolve without forcing users to manually edit generated files.

## Major Layers

```
User Source of Truth
    │
    ▼
Configuration (config.py + lib/ tree)
    │
    ▼
Generation (templates + bimhaw profile gen)
    │
    ▼
~/.bimhaw/ (build / runtime directory)
    │   ├── profiles/<name>/
    │   ├── active -> profiles/<name>
    │   └── shell_dotfiles/
    │
    ▼
Symlinked User Dotfiles (~/.profile, ~/.bashrc, etc.)
    │
    ▼
Shell Process (sh / bash)
    │
    ▼
Sourced Modules (in correct order for login/non-login, interactive, etc.)
```

## Key Components

### 1. User Configuration (Source of Truth)

- `config.py` — Defines profiles and assigns modules to them for different categories and shell modes.
- `lib/` — Directory tree containing the actual module source files:
  - `lib/sh/` — POSIX-compatible modules (always loaded)
  - `lib/bash/` — Bash-specific modules (additive)

The user is expected to keep this configuration in version control (often as part of a larger dotfiles repository) and point bimhaw at it.

### 2. Generation Layer

- Jinja2 templates located inside the bimhaw package.
- The `bimhaw profile gen` command renders these templates for a specific profile.
- Output goes into `~/.bimhaw/profiles/<name>/`.
- Generated files are thin: they mostly contain ordered lists of modules to source, plus some bootstrap logic.

Generation allows the tool's internal logic to be updated without users having to hand-edit their runtime scripts.

### 3. Runtime Directory (~/.bimhaw)

This directory is **not** the source of truth. It is a managed build/cache area.

Important contents:
- `profiles/<name>/` — Generated scripts for each profile
- `active` — Symlink to the currently selected profile directory
- `shell_dotfiles/` — The versions of `profile`, `bash_profile`, `bashrc`, `bash_logout` that will be symlinked into `$HOME`

### 4. Activation and Indirection

- `bimhaw profile load --name <name>` updates the `active` symlink.
- The symlinked user dotfiles (installed via `bimhaw link-shells`) source from `~/.bimhaw/active`.
- This allows switching profiles without touching the actual dotfiles again.

### 5. Module System

Modules are the atomic units of configuration.

**Organization**:
- By shell family: `sh` vs `bash`
- By category: `envs`, `funcs`, `aliases`, `prompts`, `logouts`, `autocomplete`

**Loading rules** (current design):
- For a pure POSIX `sh` shell: only `sh/` modules are used.
- For bash: `sh/` modules are loaded first (in their categories), then `bash/` modules are loaded.
- This implements "sh inheritance."

Within each category, the order in `config.py` determines the sourcing order.

### 6. Shell Dotfile Layer

Traditional dotfiles are replaced (via symlink) with thin wrappers provided by bimhaw:

- `~/.profile`
- `~/.bash_profile`
- `~/.bashrc`
- `~/.bash_logout`

These wrappers contain logic to:
- Detect login vs non-login
- Source the appropriate generated script from the active profile
- Handle `$ENV` / `$BASH_ENV` for non-interactive cases

The wrappers are intentionally kept simple and are generated or provided by the tool.

### 7. CLI Entry Points

- `bimhaw` — Main CLI (`bimhaw.cli`)
  - Profile management (`gen`, `load`, `current`, etc.)
  - Linking dotfiles
- `bimhaw_init` — One-time initialization of a bimhaw configuration area

## Startup Flow (Conceptual)

1. User opens a shell (login or non-login, interactive or not).
2. The real dotfile (e.g. `~/.bashrc`) is a symlink to bimhaw's version.
3. Bimhaw's dotfile determines the appropriate generated script based on shell type and mode.
4. It sources from `~/.bimhaw/active/...`.
5. The generated script sources the modules listed for the active profile, in the defined order, respecting sh/bash layering.
6. The user's environment is now configured according to the selected profile.

## Data Flow

```
config.py (profiles + module lists)
        + lib/ (actual module files)
                │
                ▼
        bimhaw profile gen
                │
                ▼
~/.bimhaw/profiles/<name>/ (generated .sh files)
                │
                ▼
~/.bimhaw/active (symlink)
                │
                ▼
symlinked ~/.bashrc etc.
                │
                ▼
shell sources modules
```

## Current Limitations Visible in the Architecture

- Configuration is expressed as large, explicit dictionaries in `config.py` (manual and verbose).
- Loading of `config.py` uses `exec()` (pragmatic but not ideal).
- There is no strong validation or schema for the configuration.
- Distinction between login/non-login and interactive modes is still exposed in the configuration structure, even though the goal is to hide it from the user.
- No built-in support for "inheritance" or "composition" between profiles yet.
- The system is heavily oriented around bash; other shells are not first-class.

These are documented as current-state observations in the ADRs.

## Diagrams

See `design/diagrams/` for:
- Traditional shell startup complexity (`manpage_shell_startup.dot`)
- Logical layered model (`logical.dot`)

These were part of the original documentation and illustrate the problem being solved.
