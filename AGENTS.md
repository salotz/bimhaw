# Project Description

Guidance for AI agents (and humans) working on the **bimhaw** codebase.

bimhaw is a tool for managing shell configuration using **profiles** and **modules**. It generates thin shell scripts from templates and uses symlinks + indirection to support multiple environments without duplicating logic or editing raw dotfiles.

# Agent Guidelines

This project follows the guidelines at https://github.com/salotz/agent-guidelines.

- Read generic-agent-guidelines.md (or equivalent) for agent-assisted work.
- Prefer task-specific tools over shell.
- Follow salotz RFC 22 (project layout), RFC 23/24 (host context).
- Cache remote resources locally when possible.
- Use compacted inlining for referenced standards.

See the glossary for term definitions.
