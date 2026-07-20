# MCP servers

The MCP side of this plugin on Claude Code: what ships, and how it is installed
and updated.

## What ships as MCP

Two MCP servers, Claude Code only. They ship by two different mechanisms:

| Server                | Mechanism                                     | Purpose                                                                                                          |
| --------------------- | --------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `chrome-devtools-mcp` | Cross-marketplace `dependencies` entry (`chrome-devtools-mcp@claude-plugins-official`) | Drive and inspect a live Chrome browser (automation, performance traces, network/console); requires Chrome 144+. |
| `notion`              | Bundled in this repo's `.mcp.json`            | Read and write Notion content (pages, databases, search). Uses Claude's native `"type": "http"` remote transport — no `mcp-remote` proxy; OAuth on first connection, no static secret in the file. |

`notion` has no bundled plugin in `claude-plugins-official`, so it is declared
inline in the root `.mcp.json`, which Claude Code auto-discovers when the plugin
installs — no manifest reference needed.

## Install and update

`chrome-devtools-mcp` is declared in `.claude-plugin/plugin.json` as a
cross-marketplace `dependencies`
entry, so a fresh install of `agent-harness` resolves and installs it
automatically — no separate step in `scripts/sync.py`. The cross-marketplace
resolution itself requires `.claude-plugin/marketplace.json` to list
`claude-plugins-official` under `allowCrossMarketplaceDependenciesOn`; without
it, install fails with a `cross-marketplace` error.

For an `agent-harness` install that predates this dependency, `claude plugin
update agent-harness@agent-harness` is not confirmed to resolve it — Claude
Code's docs only name a fresh `install`, `/reload-plugins`, or background
auto-update as ways to pick up a newly declared dependency. If `update` alone
doesn't bring it in, re-run `claude plugin install agent-harness@agent-harness`
or `/reload-plugins`.

To install or update it standalone, outside of the `agent-harness` flow:

```zsh
claude plugin install chrome-devtools-mcp@claude-plugins-official
claude plugin update chrome-devtools-mcp@claude-plugins-official
```

`update` errors if the plugin was never installed, so pick by whether it's
already present (`claude plugin list`). Restart Claude Code to apply.

`notion` needs no separate install step: it ships in the root `.mcp.json` and
loads with the plugin. On first use Claude Code opens the Notion OAuth flow;
nothing is stored in the repo.
