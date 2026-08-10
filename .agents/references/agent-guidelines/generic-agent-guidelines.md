## Generic Agent Guidelines

Generic advice for any agent-assisted work.

### RFC and Standard References

This repo is focused specifically on guidelines that do not have a practical means for more strict standardization.

Guidelines here however should make use of such standards through reference and compacted "inlining".

Sources of standards can be official standard bodies like the [Agentic AI Foundation (AAIF)](https://aaif.io/) ([summary](./summaries/aaif.md)), community or organizational standards (e.g. [Google Style Guides](https://google.github.io/styleguide/) ([summary](./summaries/google-style-guides.md))), or personal standards (e.g. [salotz RFCs](https://github.com/salotz/rfcs) ([summary](./summaries/salotz-rfcs-overview.md))).

Recommendations in this repo should explicitly reference these standards with extensions or modifications.

### Project Layout

When working on projects agents should obey [salotz RFC 22](https://github.com/salotz/rfcs/tree/master/rfcs/salotz.022_ai-coding-structure) ([summary](./summaries/salotz-rfc-022-ai-coding-structure.md)).

### Host System Interaction

When interacting with host local context agents should obey [salotz RFC 23](https://github.com/salotz/rfcs/tree/master/rfcs/salotz.023_local-agent-context) ([summary](./summaries/salotz-rfc-023-local-agent-context.md)) for loading operator defined context and [salotz RFC 24](https://github.com/salotz/rfcs/tree/master/rfcs/salotz.024_extended_xdg_base_directory) ([summary](./summaries/salotz-rfc-024-extended-xdg-base-directory.md)) for agent generated content.

### Remote Resource Caching

When agents refer to external resources like repositories as part of context loading they should prefer making locally cached copies of them.

Inspired from [this skill](https://github.com/mitsuhiko/agent-stuff/tree/main/skills/librarian) ([summary](./summaries/librarian-skill-mitsuhiko.md)).

Should obey other guidelines for [host system interaction](#host-system-interaction).

### Compacted Inlining

When writing guidelines (such as these documents) if reference is made to an extensive external standard or guideline it should be good practice to provide a compacted version of that resource "inline" with this project.

For instance if you refer to and request adherence to a particular style guide you should provide a compacted summary of that style guide for immediate loading to context.

Agents should first check for compacted versions of resources before fetching and reading the larger ones. If additionally context is needed for specifics from larger standards this can be done incrementally and ideally in sub-agents.

### Tool Preference

#### Prefer task specific tools over shell

Whenever possible agents should prefer specific tools over use of a generic "shell" tool.

This prevents unnecessary privilege escalation as a generic shell tool can do anything on a system. By using specific tools the human (or other agents) interacting with an agent can more easily understand both the intention of the agent as well as auditing potentially dangerous, disruptive, or risky calls to shells.

For example if agents want to only read a particular file they should use a specific "read" tool or agent harness extension over `cat myfile.txt`.

Coding agents should also provide useful help and guidance to their controller if they are utilizing broader capability tools like shell when they could use more constrained tools. For example if the operator has not installed the necessary tools for an agent to follow this behavior (e.g. a `read-file` tool or extension) the agent should make this known to the operator and suggest solutions to installing more fine-grained tools.

### Naming Things

When naming things (esp. files, folders, etc.) follow [salotz RFC 24](https://github.com/salotz/rfcs/tree/master/rfcs/salotz.024_extended_xdg_base_directory) ([summary](./summaries/salotz-rfc-024-extended-xdg-base-directory.md)).

### Reading the web

When possible find a non-HTML source to read on the web, as it is much more context-efficient.

This includes the markdown sources for a website (e.g. in github) or using the [llms.txt](https://llmstxt.org/) ([summary](./summaries/llms-txt-standard.md)) standard when available.
