#!/usr/bin/env python3
"""Install this plugin's rules, skills, and MCP plugin into Claude Code.

Stdlib only: `uv run scripts/sync.py`. Antigravity needs no script.
"""

import json
import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
HOME = Path.home()

# This plugin (directory-sourced) plus the official chrome-devtools MCP server.
# Both install and update the same way once their marketplaces are registered.
PLUGINS = [
    "agent-hardness@agent-hardness",
    "chrome-devtools-mcp@claude-plugins-official",
]


def _installed_plugin_ids() -> set:
    result = subprocess.run(
        ["claude", "plugin", "list", "--json"],
        check=True,
        capture_output=True,
        text=True,
    )
    return {p["id"] for p in json.loads(result.stdout)}


def main() -> None:
    claude_dir = HOME / ".claude"
    claude_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(REPO_ROOT / "rules" / "AGENTS.md", claude_dir / "CLAUDE.md")

    # Idempotent; `update` below reads plugin content live from this directory.
    subprocess.run(
        ["claude", "plugin", "marketplace", "add", str(REPO_ROOT)], check=True
    )

    # `install` is idempotent but `update` fails if the plugin was never
    # installed - branch per plugin so both stay current on re-runs.
    installed = _installed_plugin_ids()
    for plugin in PLUGINS:
        action = "update" if plugin in installed else "install"
        subprocess.run(["claude", "plugin", action, plugin], check=True)


if __name__ == "__main__":
    main()
