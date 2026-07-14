# MCP servers

The MCP side of this plugin on Claude Code: what ships, and how it is installed
and updated.

## What ships as MCP

One MCP server, and only on Claude Code — an official plugin from the
`claude-plugins-official` marketplace, not bundled into this repo:

| Plugin                | Install id                                    | Purpose                                                                                                          |
| --------------------- | --------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `chrome-devtools-mcp` | `chrome-devtools-mcp@claude-plugins-official` | Drive and inspect a live Chrome browser (automation, performance traces, network/console); requires Chrome 144+. |

## Install and update

Install it, or update it once installed:

```zsh
claude plugin install chrome-devtools-mcp@claude-plugins-official
claude plugin update chrome-devtools-mcp@claude-plugins-official
```

`update` errors if the plugin was never installed, so pick by whether it's
already present (`claude plugin list`). Restart Claude Code to apply.
`scripts/sync.py` automates this alongside the plugin's own install.

## Antigravity

Antigravity is not set up with this MCP server; it ships its own native Chrome
DevTools integration, which is what to use there. MCP is Claude Code-only, which
is where this flow is developed and tested.
