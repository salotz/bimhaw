# Summary: salotz RFC 23 - Local Agent Context

Source: https://github.com/salotz/rfcs/tree/master/rfcs/salotz.023_local-agent-context

## Purpose
Standard for local (host-specific) agent context injection, separate from remote git repo context. Enables operator preferences for installs, tools, shell, etc.

## Configuration Locations (precedence order)
1. `$XDG_CONFIG_HOME/agents` (e.g. `~/.config/agents`)
2. `~/.agents`

Avoid bare `~/AGENTS.md`.

Additional `.agents/` dirs at any level (closer = higher precedence).

## Local Overrides for Remote Repos
- Use `.agents.local.md` (file) or `.agents.local/` (dir) next to repo's `.agents/` or `AGENTS.md`.
- These override repo context for host-specific prefs.

## Agent-Derived Resources (per RFC 24)
Use `xagents` subdir under extended XDG locations (e.g. `~/.cache/xagents`, `~/.local/share/xagents`).

- `xagents` is for *agent-generated* resources (distinct from operator context in `AGENTS.md` / `.agents`).

## Precedence & Behavior
- Closest local context wins.
- On contradictions: explicitly ask operator for feedback before acting.
- Chain references upward in repo context files.

## Recommended Home Structure
```
~/.config/agents/
├── configuration.md
├── installations.md
└── shell.md
```

Drop reference snippet from RFC into project `.agents/context/` for easy adherence.

See original for full template and examples.
