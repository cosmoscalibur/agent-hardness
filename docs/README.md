# Documentation

Maintenance reference for the plugin — the detail the root `README.md` links out
to. Each file is self-contained and cross-references the others inline; this
index is the entry point.

| Doc                                        | Covers                                                                                    |
| ------------------------------------------ | ----------------------------------------------------------------------------------------- |
| [cli-tools.md](cli-tools.md)               | Install commands for the required CLI tools (uv, rtk, ast-grep, mergiraf).                 |
| [rules-and-skills.md](rules-and-skills.md) | How to extend `rules/agent-harness.md` and add skills, and how each client deploys them.         |
| [mcp.md](mcp.md)                           | The chrome-devtools and notion MCP servers: what ships, and how each installs/updates on Claude Code.    |
| [lsp.md](lsp.md)                           | The internally declared language servers, their schema, and how to install or add one.    |
| [hooks.md](hooks.md)                       | How the plugin's hooks work and what ships.                                |
