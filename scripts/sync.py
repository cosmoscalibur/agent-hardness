#!/usr/bin/env python3
"""Install this plugin's rules, skills, and MCP servers into Claude Code.

Claude Code is the only supported client. The ruleset installs to
`~/.claude/rules/agent-harness.md` — a global rule loaded at session start.
The user's own `~/.claude/CLAUDE.md` is left untouched unless it is a legacy
copy of this ruleset (see `_remove_legacy_claude_md`), which is removed.
Stdlib only: `uv run scripts/sync.py`.
"""

import json
import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
HOME = Path.home()

PLUGIN_ID = "agent-harness@agent-harness"

# Heading of the legacy `~/.claude/CLAUDE.md` that earlier setups created by
# copying the ruleset into global memory, before it shipped as a rule file.
LEGACY_RULESET_HEADING = "Technical Strategy & Execution Rules"


def _installed_plugin_ids() -> set:
    result = subprocess.run(
        ["claude", "plugin", "list", "--json"],
        check=True,
        capture_output=True,
        text=True,
    )
    return {p["id"] for p in json.loads(result.stdout)}


def _remove_legacy_claude_md() -> None:
    """Remove a global `CLAUDE.md` that is only a stale copy of this ruleset.

    Earlier setups copied the ruleset into `~/.claude/CLAUDE.md`; it now
    installs as a rule file, so such a copy just double-loads the same rules. A
    `CLAUDE.md` whose heading is the ruleset title is that copy and is removed;
    a user-authored `CLAUDE.md` (any other heading) is left alone.
    """
    claude_md = HOME / ".claude" / "CLAUDE.md"
    if not claude_md.is_file():
        return
    with claude_md.open() as fh:
        first_line = fh.readline()
    if first_line.lstrip("#").strip() == LEGACY_RULESET_HEADING:
        claude_md.unlink()
        print(f"Removed legacy {claude_md} (ruleset installs as a rule file).")


def main() -> None:
    rules_dir = HOME / ".claude" / "rules"
    rules_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(
        REPO_ROOT / "rules" / "agent-harness.md", rules_dir / "agent-harness.md"
    )
    _remove_legacy_claude_md()

    # Idempotent; `update` below reads plugin content live from this directory.
    subprocess.run(
        ["claude", "plugin", "marketplace", "add", str(REPO_ROOT)], check=True
    )

    # `install` is idempotent but `update` fails if the plugin was never
    # installed - branch so re-runs stay current either way. This also
    # resolves the chrome-devtools-mcp dependency declared in plugin.json.
    action = "update" if PLUGIN_ID in _installed_plugin_ids() else "install"
    subprocess.run(["claude", "plugin", action, PLUGIN_ID], check=True)


if __name__ == "__main__":
    main()
