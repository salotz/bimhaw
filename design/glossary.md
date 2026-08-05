# Glossary

**Profile** A named, self-contained collection of shell configuration intended for a particular context or environment.

Examples include `personal`, `work`, `minimal`, `demo`, and `recovery`.

Profiles are the primary unit of selection and switching. A user activates one profile at a time via the `active` symlink.

**Module** A small, focused shell script that provides a specific piece of configuration.

Modules are organized by shell family (`sh/` for POSIX-compatible or `bash/` for bash-specific) and by category.

All `sh/` modules are sourced for bash users in addition to any `bash/` modules (see **sh inheritance**).

**Category** The functional grouping of modules.

Common categories include `envs`, `funcs`, `aliases`, `prompts`, `logouts`, and `autocomplete`.

**sh inheritance** When bash is active, all applicable `sh/` modules are loaded first (in their categories), followed by `bash/` modules.

**Dotfile** Traditional name for hidden configuration files in `$HOME` that start with a dot.

Examples include `.bashrc`, `.profile`, and `.bash_profile`.

**Rice** Slang in the Unix/Linux community for heavily customizing and theming one's desktop or shell environment, often for aesthetics or personal workflow.

bimhaw supports having dedicated profiles for "rice" setups versus minimal or production setups.

**Fallback Profile** A deliberately minimal profile intended to be usable even when the main configuration is broken.

Useful for debugging or after a bad change. Also called a Recovery Profile.