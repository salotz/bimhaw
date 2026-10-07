# Plan: Shared “Project management & tooling” section in agent-guidelines

**Status**: Completed (2026-08-12)

**Date**: 2026-08-12

**Scope**: Upstream **agent-guidelines** (shared generic guidelines), not bimhaw product code.

**Canonical repo (edited)**: `/home/salotz/tree/personal/devel/agent-guidelines`

**Do not** treat bimhaw’s `.agents/references/agent-guidelines/` as source of truth (older/partial cache). Cache refresh left optional (collation/`cacher`).

## Goal

Add a **new shared top-level section (file)** in agent-guidelines for **project management and tooling**, link it from the hub files, and keep it independently loadable.

## Execution (2026-08-12)

### Artifacts (canonical repo)

| Path | Change |
|------|--------|
| `shared/project-management-and-tooling.md` | **Created** — content-focused config, layered tooling, `mise exec`-style entrypoints, secrets, host-install confirmation, agent checklist |
| `shared/generic-agent-guidelines.md` | Replaced long inline “Project Tooling” block with thin link to the new file |
| `README.md` | Shared guideline groups index entry |
| `shared/README.md` | Contents index entry |
| `AGENTS.md` | Note that shared topic docs are independently referenceable |
| `shared/glossary.md` | Terms: **content-focused config**, **project tooling entrypoint** |
| `contributing/editing.md` | Checklist: new shared topics get own file + hub link |
| `~/.config/agents/AGENTS.md` | Load-list example includes `project-management-and-tooling.md` |

### bimhaw follow-ups

- DX step 0006 notes point at the devel checkout path for the shared baseline.
- Did **not** bulk-refresh `.agents/references/agent-guidelines/` (layout mismatch with current `shared/` + `personal/`; prefer devel checkout or cacher later).
- bimhaw config files left content-focused (no usage preambles reintroduced).

## Success criteria

- [x] New file exists and is loadable on its own
- [x] Hubs link without inlining the full text
- [x] Config content-focused + contributing-for-usage + exec-vs-activate rules stated generically
- [x] RFC 22/23/24 referenced, not duplicated
- [ ] bimhaw cache updated — **deferred** (optional; checkout is preferred)
- [x] No long preambles reintroduced into bimhaw config files

## References

- `/home/salotz/tree/personal/devel/agent-guidelines/shared/project-management-and-tooling.md`
- bimhaw `.agents/plan/dx-modern-toolchain/` (invocation policy; config content-focused)
