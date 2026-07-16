#!/usr/bin/env python3
"""PostToolUse hook: run rumdl (fix, then format) on an edited Markdown file.

Reads the hook payload as JSON on stdin and acts only on .md files.
"""

import json
import subprocess
import sys

MARKDOWN_SUFFIXES = (".md",)


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return

    file_path = payload.get("tool_input", {}).get("file_path")
    if not file_path or not file_path.endswith(MARKDOWN_SUFFIXES):
        return

    subprocess.run(["uvx", "rumdl", "check", "--fix", "-q", file_path], check=False)
    subprocess.run(["uvx", "rumdl", "fmt", "-q", file_path], check=False)


if __name__ == "__main__":
    main()
