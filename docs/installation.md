# Installation internals

Reference for how this plugin gets installed into each supported client. The
README covers the commands to run; this file explains what those commands do,
for maintenance and troubleshooting.

## Claude Code — `python3 scripts/sync.py`

The script targets Claude Code only (Antigravity needs no script — see below).
It runs these steps in order:

1. **Copy the ruleset.** `rules/AGENTS.md` → `~/.claude/CLAUDE.md`. This is a
   plain overwrite, not a merge: re-running replaces the previous copy rather
   than appending to it. `rules/AGENTS.md` is the single source of truth.
2. **Register the marketplace.** `claude plugin marketplace add <repo>` adds
   this repo (via `.claude-plugin/marketplace.json`) as a directory-sourced
   marketplace.
3. **Refresh it explicitly.** `claude plugin marketplace update agent-hardness`.
   A directory-sourced marketplace does **not** auto-refresh, so without this a
   local repo change (e.g. a version bump) would stay invisible to the
   install/update step below.
4. **Install or update the plugin.** `claude plugin install` is idempotent (a
   no-op if the plugin is already installed), but `claude plugin update` fails
   outright if the plugin was never installed. The script checks
   `claude plugin list --json` and branches accordingly, rather than relying on
   call order. This installs the plugin's **skills** only.
5. **Install the official MCP/LSP plugins.** From the `claude-plugins-official`
   marketplace: `chrome-devtools-mcp`, `typescript-lsp`, `pyright-lsp`,
   `rust-analyzer-lsp`. Each `install` is likewise idempotent.

Restart Claude Code to apply an update. Re-run the script after every change to
this repo — because step 1 overwrites and steps 3–4 pull the refreshed
marketplace, stale content is never left behind.

### Manual install (skills only, no script)

This repo is directly installable as a Claude Code plugin marketplace
(`.claude-plugin/marketplace.json` + `.claude-plugin/plugin.json`) without the
script:

```zsh
claude plugin marketplace add /path/to/agent-hardness
claude plugin install agent-hardness@agent-hardness
```

This installs the **skills only**. The ruleset (`rules/AGENTS.md` →
`~/.claude/CLAUDE.md`) and the MCP/LSP plugins are not set up this way — run
`python3 scripts/sync.py` for the full setup, or copy the ruleset by hand.

## Antigravity — direct install, no script

Antigravity installs directly from the repo with `agy plugin install <repo>`
(local path or GitHub URL). `agy` auto-discovers `rules/`, `skills/`, and
`plugin.json` by convention from the plugin root, so there is no copy step and
nothing for a script to add over the single `agy` command. The repo manages
only rules and skills on Antigravity; it does not set up MCP or LSP there —
that flow is Claude Code-only, which is where it is developed and tested.
