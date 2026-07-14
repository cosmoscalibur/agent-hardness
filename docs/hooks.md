# Hooks (Claude Code)

This plugin ships one hook: a `PostToolUse` hook that formats and lint-fixes
Python files with Ruff after each edit. Hooks are set up on Claude Code only.
They live entirely under [`hooks/`](../hooks/) — `hooks.json` plus the
`ruff_fix.py` it invokes — so the whole hook installs with the plugin.
Antigravity supports hooks too, but this flow does not target it.

## Why a hook and not a second LSP

Claude Code runs **one language server per language**. The Python LSP
(`basedpyright`) gives type intelligence but does not format code or apply lint
autofixes, and a second Python LSP can't be added to cover that. Ruff fills the
gap as a `PostToolUse` hook: after Claude writes or edits a `.py`/`.pyi` file,
the hook runs `ruff check --fix` then `ruff format` on it.

## Structure

A plugin declares hooks in `hooks/hooks.json` at the plugin root (or inline as a
`hooks` key in `plugin.json`; a standalone file keeps them out of the
version-bumped manifest). The shape mirrors Claude Code's user hooks:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "uv run --no-project \"${CLAUDE_PLUGIN_ROOT}/hooks/ruff_fix.py\""
          }
        ]
      }
    ]
  }
}
```

- **Event** (`PostToolUse`) fires after a tool call succeeds. Other lifecycle
  events exist (`PreToolUse`, `SessionStart`, `UserPromptSubmit`, …).
- **`matcher`** is a regex over **tool names**, not file paths — `Write|Edit`
  matches both edit tools. There is no way to match on the edited file's type
  here, so a hook that should act on one language must receive every edit and
  filter by extension itself (which `ruff_fix.py` does).
- **`hooks[].type: "command"`** runs a shell command; Claude Code passes the
  tool payload as JSON on its stdin. Python is invoked through `uv run` per the
  project's `uv`-only rule, and `--no-project` keeps the run isolated from any
  surrounding project environment.
- **`${CLAUDE_PLUGIN_ROOT}`** resolves to the installed plugin's root directory
  — always reference bundled files through it, never a relative path.

[`hooks/ruff_fix.py`](../hooks/ruff_fix.py) (Python stdlib) reads the stdin
payload, takes `tool_input.file_path`, and returns immediately unless it's a
`.py`/`.pyi` file. For Python it runs Ruff via `uvx`, which fetches Ruff on
demand (cached after first use), so uv is the only prerequisite. Ruff runs with
`check=False`, so a lint failure is swallowed rather than blocking the edit.

### Adding another hook

Add an entry under the appropriate event in `hooks/hooks.json`, put any script
in `hooks/` (not `scripts/`, which is for one-off tooling like the installer),
and reference it via `${CLAUDE_PLUGIN_ROOT}`. Invoke Python through `uv run` and
keep the script stdlib-only so it needs no environment setup. Editing `hooks/`
is a patch bump (see the repo's `CLAUDE.md` versioning rules).

## Ruff

The hook runs Ruff through `uvx` (`uv tool run`), so nothing beyond `uv` needs
installing — the first run fetches Ruff into uv's cache. To also have `ruff` on
your `PATH` for manual use, install it as a uv tool:

```zsh
uv tool install ruff
```
