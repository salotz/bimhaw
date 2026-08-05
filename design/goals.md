# Design Principles

These principles capture the philosophy and values that guided the original development of bimhaw and should continue to guide its evolution.

## 1. Pragmatism Over Purity

- The shell startup environment is inherently messy due to decades of legacy behavior in POSIX, bash, and system profiles.
- We accept that **some ugliness is necessary** to provide a usable abstraction.
- Prefer solutions that work reliably in the real world over theoretically clean but brittle designs.
- The goal is to reduce the cognitive burden on the *user* of the tool, not to achieve perfect purity in the implementation.

## 2. Hide Legacy Complexity

- Users should not need to internalize the full shell startup diagram (login vs non-login, interactive vs non-interactive, sourcing order of `/etc/profile`, `~/.bash_profile`, `~/.bashrc`, `$ENV`, etc.).
- The tool's job is to encapsulate that complexity behind a cleaner model (profiles + modules).
- When the abstraction leaks, it should be rare and well-documented.

## 3. Separation of Concerns

- Configuration should be broken into small, focused, composable pieces ("modules").
- Different kinds of configuration have different lifetimes and scopes:
  - Environment setup
  - Functions
  - Aliases
  - Prompts
  - Autocompletion (shell-specific)
  - Logout actions
- Distinguish portable POSIX `sh` configuration from bash-specific extensions.

## 4. Multiple Environments as a First-Class Concept

- Many users (especially power users and developers) need distinct shell environments:
  - Personal vs work
  - Different machines
  - Experimentation / "ricing"
  - Minimal vs full-featured
  - Fallback / recovery profiles
- The system must make it easy to define, generate, and switch between named **profiles**.

## 5. Generation and Indirection Are Acceptable Costs

- Direct editing of the final dotfiles is fragile and leads to divergence.
- Using templates + generation allows the core logic of the tool to evolve without forcing users to manually update every generated file.
- Layers of symlinks and indirection (`~/.bimhaw/active`, generated profile scripts, symlinked shell dotfiles) are a deliberate trade-off to gain safety, updatability, and profile switching.

## 6. User Configuration Is the Source of Truth

- The primary source of truth lives in the user's `config.py` and `lib/` directory (often kept in a separate dotfiles repo).
- `~/.bimhaw/` is a **build / cache / runtime directory**, not the canonical home for configuration.
- Users should be able to point the tool at external configuration locations.

## 7. Portability Where Practical, Bash Power When Needed

- Provide a strong base of POSIX `sh` compatible modules.
- All `sh` modules are loaded for bash users (inheritance model).
- Bash-specific modules are additive, not replacements.
- This supports both "pure" portable setups and rich interactive bash environments.

## 8. Explicitness and Auditability

- Generated files should be readable and auditable.
- Profile scripts primarily contain lists of modules to source, keeping them as thin orchestration layers.
- The system should make it relatively easy to understand "what is active right now."

## 9. Start Practical, Evolve Deliberately

- The original implementation used pragmatic shortcuts (e.g., `exec` of config.py, manual module lists).
- These are acceptable as long as they are documented as current-state decisions.
- Future changes should be made via explicit Architecture Decision Records rather than ad-hoc improvements.

## 10. Documentation of Intent

- Because the tool adds complexity (indirection, generation), the *why* behind the design must be preserved.
- This `design/` folder exists to make that intent durable across time and across different developers (human or AI).

## Anti-Goals (What We Are Not Trying To Do)

- We are not trying to replace all dotfile managers or become a universal "dotfiles framework."
- We are not trying to eliminate all shell-specific knowledge from the user (some leakage is inevitable).
- We are not optimizing for beginners who have never touched a shell config; the target is intermediate-to-advanced users who are already in pain from manual management.
- We are not aiming for zero runtime dependencies or a single-file solution if it harms maintainability or clarity.
