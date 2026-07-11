#!/usr/bin/env python3
"""Install this plugin's rules and skills into a target IDE.

Run through uv, never a bare interpreter: `uv run scripts/sync.py <ide>`.
"""

import argparse
import json
import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
HOME = Path.home()

PLUGIN_ID = "agent-hardness@agent-hardness"

# Official plugins installed alongside this one - see docs/mcp-servers.md.
CLAUDE_PLUGINS = ["chrome-devtools-mcp@claude-plugins-official"]


def sync_antigravity() -> None:
    # Antigravity auto-discovers rules/ and skills/ by convention from
    # plugin.json's location, and ships its own native Chrome DevTools
    # integration - see docs/mcp-servers.md - so no MCP setup is needed here.
    subprocess.run(["agy", "plugin", "install", str(REPO_ROOT)], check=True)


def _is_plugin_installed(plugin_id: str) -> bool:
    result = subprocess.run(
        ["claude", "plugin", "list", "--json"],
        check=True,
        capture_output=True,
        text=True,
    )
    return any(p["id"] == plugin_id for p in json.loads(result.stdout))


def sync_claude() -> None:
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


SYNC_FUNCS = {
    "antigravity": sync_antigravity,
    "claude": sync_claude,
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ide", choices=sorted(SYNC_FUNCS))
    args = parser.parse_args()
    SYNC_FUNCS[args.ide]()


if __name__ == "__main__":
    main()
