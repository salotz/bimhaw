# Local Agent Context

- nexp :: `salotz.023_local-agent-context`
- long name :: Local Agent Context
- executive summary :: Provides a standard for specifying local AI agent context injection. Includes standardization of standard linux style home directories and mechanisms for local overrides of git repo context.

## Goals

The goal of this RFC is to provide a common structure for defining local context to provide to coding agents.

By "local" this document means context that is derived from the current host computer and not from git repositories or otherwise remote fetched content.

For instance agents may act to install software or write configuration. You may have preferences for how this occurs that the agent would otherwise not know. This specification provides a means for communicating that to agents.

Additionally, if you have remote content (git repos) that have policy and context you may want to augment that with local preferences (e.g. installation locations, additional temporary working directories, etc.).

## Configuration Directories

The primary locations for local "home" configuration are in order of precedence and preference:

- `$XDG_CONFIG_HOME/agents` (i.e. `~/.config/agents`) or equivalents on non-linux systems
- `~/.agents`

You should not use a bare `~/AGENTS.md`.

Additional `.agents/` directories can be placed at any level of directories and take precedence the closer to the current working remote directories.

This RFC is compatible with RFC 22, which mandates a similar `.agents` directory in remote sourced directories. To support local context in remote directories use the `.agents.local.md` file and/or the `.agents.local` directory.

Because of the challenges of indexing arbitrary depths of context directories this specification only requires explicit discovery of the "home" context and context directories one level above the current project.

Implementations and users are encouraged then to explicitly chain context references upward in the directory hierarchy.

For example on a machine a user might configure the home directory with:

```
~/.config/agents
├── configuration.md
├── installations.md
└── shell.md
```

Where they set preferences for configuration, installing new packages, and shell preferences.

This should be referenced by your in repo context referring to this RFC.

Additionally for a project at the location `~/dev/projects/my-project`
you can have the possible configuration:

```
~/dev
└── projects
    ├── .agents
    │   └── projects.md
    └── my-project
        ├── .agents
        │   └── context
        │       └── project-details.md
        ├── .agents.local.md
        └── AGENTS.md
```

### Precedence

Precedence is towards the local configuration closest to the project. For instance if the home context in `~/.agents/installation.md` recommends installing ad hoc tools into `~/opt` but a project or directory local context (e.g. `~/dev/projects/.agents/projects.md`) recommends installing in `~/software` the agent should obey the `~/dev/projects/.agents/projects.md` advice.

When there are contradictions agents should explicitly ask for feedback and make it clear to the user before taking action.

## Agent Derived Resources

A common pattern is for agents to fetch or generate additional resources on a host for use within multiple projects.

For instance an agent skill might implement caching of repositories to the host to avoid excessive network calls. Or an agent might provide an outline of a users host machine resources for later reference.

This is similar to classical software which has long had standards for organizing this data. One can look at the POSIX standards for system-wide directories under `/` or the [XDG Base Directory Specification](https://specifications.freedesktop.org/basedir/latest/) as examples.

We leverage the additional level of specification for user local layouts from the XDG Base Directory Specification extension in [RFC 24](../salotz.024_extended_xdg_base_directory/README.md).

Under RFC 24 agents should use a sub-directory in the appropriate locations with the name `xagents` (for 'eXtended Agents'). This avoids using the plain `agents` which is a plain english word and ambiguous, despite some efforts at standardization elsewhere.

For example you might have skills that use the cache directory like this:

```markdown
/home/salotz/.cache/xagents
├── papers
│   ├── d5np00041f.pdf
│   ├── HSA-Runtime-1.2.pdf
│   └── mmc2.pdf
└── repos
    └── rfcs
```

Otherwise agents should utilize the meanings of the directories from the other specifications. Many of them will not be for agent actions and for generated software.

Note that the `xagents` directories are specifically for agent generated resources compared to operator based resources in `AGENTS.md` and `.agents` directories.

### Motivation

The utility of such organization is:

#### Namespace Pollution

By providing sub-namespaces it limits the "pollution" of common "namespaces" like a users `$HOME` directory with dozens or hundreds of application specific directories (e.g. `.emacs`, `.tmux.conf`, etc.).

Pollution of common namespaces can make tool usage complex. For instance if you wanted to get the disk usage of all configuration or cache directories you would need to distinguish between content directories in `$HOME` and which configuration directories have cache data.

#### Content Indexing

Create clear expectations for where to look for specific kinds of information which will have have vastly different indexing requirements.

For instance you may want to include PDFs stored in a content repository under `~/.local/share` to be indexed by system wide search but not cached (`~/.cache`) or operational data (`~/.local/var`).

#### Storage Needs

Different types of data have different storage needs.

For example you would want to include regular snapshotting of configuration directories (`~/.config`) but not cached data (`~/.cache`).

Users should be able to easily configure filesystems to match these requirements using the standardized directories.

This is difficult or impossible if all applications use their own custom directories for this content which can lead to system stability problems if left unconfigured.


## Template Context

Drop the following snippet into your remote repo context (per RFC 22, recommended path: `.agents/context/local-agent-context.md`) so that agents and humans can easily adhere to this standard.

```markdown
# Local Agent Context (per RFC 23)

This project uses local (host-specific) agent context.

## Discovery Order (highest precedence first)
- `$XDG_CONFIG_HOME/agents` (e.g. `~/.config/agents`) or platform equivalents
- `~/.agents`

Do not rely on a bare `~/AGENTS.md`.

## Precedence
Precedence favors the local configuration closest to the project.

For example, if the home context in `~/.agents/installation.md` recommends installing tools into `~/opt` but a project or directory local context (e.g. `~/dev/projects/.agents/projects.md`) recommends `~/software`, the agent must obey the closer context.

When there are contradictions, agents should explicitly ask for feedback and make it clear to the user before taking action.

## Local Overrides for Remote Repos
- Use `.agents.local.md` (single file) or `.agents.local/` (directory) next to the repo's `.agents/` or `AGENTS.md`.
- These take precedence over repo context for local preferences (install locations, temp dirs, shell prefs, etc.).

## Recommended Placement
- Home-level preferences: `~/.config/agents/{configuration,installations,shell}.md`
- Per-parent-dir: `~/dev/.agents/` (applies to all projects under it)
- Per-project local override: `<project>/.agents.local.md`

## Chaining
Explicitly reference upward context files from repo AGENTS.md / `.agents/context/*.md` so agents discover them.
```
