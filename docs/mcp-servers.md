# MCP Servers

This repo does not bundle or sync any MCP server config — chrome-devtools
setup is native to each supported IDE:

## chrome-devtools

Drives and inspects a live Chrome browser (automation, performance traces,
network/console inspection). See the
[chrome-devtools-mcp repo](https://github.com/ChromeDevTools/chrome-devtools-mcp).
Requires Chrome 144+; no secret needed.

- **Claude Code**: `uv run scripts/sync.py claude` installs the official
  `chrome-devtools-mcp@claude-plugins-official` plugin alongside this one —
  no config file needed. To install it standalone instead:

  ```zsh
  claude plugin install chrome-devtools-mcp@claude-plugins-official
  ```

- **Antigravity**: ships its own native Chrome DevTools integration. Enable
  that instead of installing this server — adding it on top would duplicate
  functionality already built in.
