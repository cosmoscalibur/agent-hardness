#!/usr/bin/env python3
"""Install this plugin's rules, skills, and MCP/LSP plugins into Claude Code.

Run with Python 3 (stdlib only, no dependencies): `python3 scripts/sync.py`.

Antigravity needs no script — it installs directly from the repo with
`agy plugin install <repo>` (see README "Global Setup").
"""

import json
import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
HOME = Path.home()

PLUGIN_ID = "agent-hardness@agent-hardness"

# Official plugins installed alongside this one: the chrome-devtools MCP
# server plus the TypeScript, Pyright, and rust-analyzer language servers.
CLAUDE_PLUGINS = [
    "chrome-devtools-mcp@claude-plugins-official",
    "typescript-lsp@claude-plugins-official",
    "pyright-lsp@claude-plugins-official",
    "rust-analyzer-lsp@claude-plugins-official",
]


def _is_plugin_installed(plugin_id: str) -> bool:
    result = subprocess.run(
        ["claude", "plugin", "list", "--json"],
        check=True,
        capture_output=True,
        text=True,
    )
    return any(p["id"] == plugin_id for p in json.loads(result.stdout))


def main() -> None:
    claude_dir = HOME / ".claude"
    claude_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(REPO_ROOT / "rules" / "AGENTS.md", claude_dir / "CLAUDE.md")

    subprocess.run(
        ["claude", "plugin", "marketplace", "add", str(REPO_ROOT)], check=True
    )
    # A directory-sourced marketplace doesn't auto-refresh - update
    # explicitly so a local repo change (e.g. a version bump) is visible
    # before the install-vs-update check below.
    subprocess.run(
        ["claude", "plugin", "marketplace", "update", "agent-hardness"], check=True
    )
    # `install` is idempotent (no-op if already installed) but `update`
    # fails outright if the plugin was never installed - so branch instead
    # of relying on call order to avoid that failure.
    if _is_plugin_installed(PLUGIN_ID):
        subprocess.run(["claude", "plugin", "update", PLUGIN_ID], check=True)
    else:
        subprocess.run(["claude", "plugin", "install", PLUGIN_ID], check=True)
    for plugin in CLAUDE_PLUGINS:
        subprocess.run(["claude", "plugin", "install", plugin], check=True)


if __name__ == "__main__":
    main()
