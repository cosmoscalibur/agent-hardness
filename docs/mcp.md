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

`.claude-plugin/plugin.json` declares it as a cross-marketplace `dependencies`
entry, so a fresh install of `agent-hardness` resolves and installs it
automatically — no separate step in `scripts/sync.py`. The cross-marketplace
resolution itself requires `.claude-plugin/marketplace.json` to list
`claude-plugins-official` under `allowCrossMarketplaceDependenciesOn`; without
it, install fails with a `cross-marketplace` error.

For an `agent-hardness` install that predates this dependency, `claude plugin
update agent-hardness@agent-hardness` is not confirmed to resolve it — Claude
Code's docs only name a fresh `install`, `/reload-plugins`, or background
auto-update as ways to pick up a newly declared dependency. If `update` alone
doesn't bring it in, re-run `claude plugin install agent-hardness@agent-hardness`
or `/reload-plugins`.

To install or update it standalone, outside of the `agent-hardness` flow:

```zsh
claude plugin install chrome-devtools-mcp@claude-plugins-official
claude plugin update chrome-devtools-mcp@claude-plugins-official
```

`update` errors if the plugin was never installed, so pick by whether it's
already present (`claude plugin list`). Restart Claude Code to apply.

## Antigravity

Antigravity is not set up with this MCP server; it ships its own native Chrome
DevTools integration, which is what to use there. MCP is Claude Code-only, which
is where this flow is developed and tested.
