# Summary: salotz RFC 24 - Extended XDG Base Directory Specification

Source: https://github.com/salotz/rfcs/tree/master/rfcs/salotz.024_extended_xdg_base_directory

## Purpose
Extends XDG Base Dir Spec with additional user-local dirs using `XDGX_*` env vars. Improves organization, backup policies, and namespace hygiene for agent and general use.

## XDG Base (reminder)
- `XDG_DATA_HOME` → `~/.local/share`
- `XDG_CONFIG_HOME` → `~/.config`
- `XDG_CACHE_HOME` → `~/.cache`
- `~/.local/bin` for executables

## Extensions (with XDGX_ overrides)

### opt (`XDGX_OPT_HOME`)
- Default: `~/.local/opt`
- For ad-hoc, non-package-manager user software installs.
- Symlink/copy executables to `~/.local/bin` instead of adding opt to PATH.
- Recommendation: snapshot for backups.

### tmp (`XDGX_TMP_HOME`)
- Default: `~/.local/tmp`
- User-local equivalent to /tmp (avoids polluting system tmp).
- Suitable for long-running user processes.
- Do **not** snapshot. Can clear on boot.

### scratch (`XDGX_SCRATCH_HOME`)
- Default: `~/.local/scratch`
- Ephemeral batch-process scratch space (distinct from tmp).
- For test suites, short-lived batch jobs.
- All files deletable at any time; schedule cleanups.
- Do **not** snapshot. Can clear on reboot.

### var (`XDGX_VAR_HOME` implied)
- Default: `~/.local/var`
- For persistent/variable data (like FHS /var).
- Many apps misuse `~/.local/share` for this.
- Recommendation: snapshot for backups. Persists across reboots.

## Motivation
- Reduces namespace pollution in $HOME.
- Enables differentiated backup/snapshot/cleanup policies.
- Clear expectations for indexing and storage needs.

Use `xagents/` subdirs (per RFC 23) under these for agent-generated content.

See original RFC for full rationale.
