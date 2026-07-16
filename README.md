# Agent Hardness Plugin

Antigravity and Claude Code plugin that packages agent readiness evaluation, a
global behavioral/tooling ruleset, and stage-specific coding methodology skills
(planning, implementation, review, commit, pull requests) into a single global
package. On Claude Code it also wires up language servers, Ruff and rumdl
auto-format hooks, and the chrome-devtools MCP server.

The CLI tools and language servers below are prerequisites — install them
first, then install the hardness itself ([Installation](#installation)). The
detailed inventory of what the plugin contains is in
[What's Included](#whats-included) and the [`docs/`](docs/) reference.

## CLI Tools Required

Installation is left to the developer's own environment and package manager;
[`docs/cli-tools.md`](docs/cli-tools.md) has concrete install commands.

| Tool                                             | Purpose                                                                | Install                                                                              |
| ------------------------------------------------ | ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| [ast-grep](https://github.com/ast-grep/ast-grep) | Structural code search via AST                                         | [Installation guide](https://ast-grep.github.io/guide/quick-start.html#installation) |
| [RTK](https://github.com/rtk-ai/rtk)             | Terminal output compression (60-90% fewer tokens)                      | [Repository](https://github.com/rtk-ai/rtk)                                          |
| [gh](https://cli.github.com/)                    | GitHub integration and ADRs                                            | [Installation guide](https://github.com/cli/cli#installation)                        |
| [mergiraf](https://mergiraf.org/)                | Syntax-aware git merge driver — auto-resolves AST-equivalent conflicts | [Installation guide](https://mergiraf.org/installation.html)                         |
| [uv](https://github.com/astral-sh/uv)            | Run/manage Python3 (`scripts/sync.py`, the Ruff hook, any Python)      | [Installation guide](https://docs.astral.sh/uv/getting-started/installation/)        |

### Language Servers (Claude Code)

The plugin declares its language servers internally (in `.lsp.json`); the
binaries are a prerequisite you install **before** the Claude setup. See
[`docs/lsp.md`](docs/lsp.md) for the install command for each and how to add a
new server.

| Language          | Server                        | Binary                        |
| ----------------- | ----------------------------- | ----------------------------- |
| Python            | basedpyright                  | `basedpyright-langserver`     |
| Markdown          | marksman                      | `marksman`                    |
| Bash              | bash-language-server          | `bash-language-server`        |
| TypeScript / JS   | typescript-language-server    | `typescript-language-server`  |
| HTML              | vscode-langservers-extracted  | `vscode-html-language-server` |
| CSS / SCSS / Less | vscode-langservers-extracted  | `vscode-css-language-server`  |
| Rust              | rust-analyzer                 | `rust-analyzer`               |

Python formatting and lint-autofix run through a Ruff `PostToolUse` hook, not a
second LSP — Claude Code allows one language server per language, and the Python
LSP doesn't format. See [`docs/hooks.md`](docs/hooks.md).

## Installation

### rtk

`rules/AGENTS.md` §4 says to route supported commands (`git`, `find`, `grep`,
`ls`, `read`, ...) through `rtk` — but that's a text rule the agent has to
remember on every command. `rtk` also ships a hook that intercepts those
commands automatically at the client level, so enforcement doesn't depend on
per-command discipline. Install it once per client, globally:

```bash
# Claude Code (default agent)
rtk init -g

# Gemini CLI — also covers Antigravity 2, which shares Gemini's
# configuration format (don't use the separate `--agent antigravity` target)
rtk init -g --gemini
```

Check `rtk config` afterward to confirm the hook is installed (it warns
`No hook installed` otherwise). Later, `rtk session` shows adoption per session
and `rtk discover` lists specific commands still bypassing it.

### git & mergiraf

Configure git to favor linear history and enable
[mergiraf](https://mergiraf.org/) as a syntax-aware merge driver, so conflicts
that are only formatting differences (AST-equivalent) resolve automatically
instead of landing on the agent:

```bash
git config --global pull.rebase true
git config --global merge.ff only
git config --global merge.conflictStyle diff3
git config --global merge.mergiraf.name mergiraf
git config --global merge.mergiraf.driver 'mergiraf merge --git %O %A %B -s %S -x %X -y %Y -p %P -l %L'
```

Apply mergiraf to all files globally by adding this line to git's global
attributes file (`~/.config/git/attributes`, git's default — no extra config
needed):

```
* merge=mergiraf
```

### Claude Code

```bash
uv run scripts/sync.py
```

Copies `rules/AGENTS.md` to `~/.claude/CLAUDE.md` and installs the plugin
(skills, the bundled language servers, the Ruff/rumdl hooks, and — as a
declared dependency — the chrome-devtools MCP server). Re-run after every
update to this repo, then restart Claude Code to apply.

### Antigravity

Installs directly from the repo — no script needed, because `agy` auto-discovers
`rules/`, `skills/`, and `plugin.json` by convention:

```bash
# From local path
agy plugin install /path/to/agent-hardness

# From GitHub
agy plugin install https://github.com/cosmoscalibur/agent-hardness
```

## What's Included

### Rules (always-on)

A single consolidated `rules/AGENTS.md` holds the behavior that applies
regardless of which skill is active — guard duty and scope control,
documentation currency, conversational register, CLI tooling preferences, and
the rules for when each workflow skill is invoked. Detailed, stage-specific
procedures live in the skills instead.

Origins are not tracked per rule — they are noted here as inspiration instead:

- In-house practices, refined by systematically interrogating Claude about its
  training biases at each stage of the development flow and writing
  counterweight rules against them.
- [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills)
  — Karpathy-inspired execution discipline.
- [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) —
  YAGNI-driven decision ladder.
- [juliusbrussee/caveman](https://github.com/juliusbrussee/caveman) — concise,
  professional prose compression.

See [`docs/rules-and-skills.md`](docs/rules-and-skills.md) for how to extend the
ruleset and add a skill.

### Skills

| Skill             | Source                                                          | License | Description                                                                                                                                                                 |
| ----------------- | --------------------------------------------------------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `agent-readiness` | [Factory AI](https://www.factory.ai/agent-readiness)            | MIT     | Scores a repository's readiness for autonomous AI agent development across 9 pillars with a phased plan; adapted from Factory AI's framework to modern tooling conventions. |
| `ast-grep`        | [ast-grep/agent-skill](https://github.com/ast-grep/agent-skill) | MIT     | Guides structural, AST-based code search and rule authoring; used as-is, no adaptation.                                                                                     |
| `planning`        | Own                                                             | MIT     | Produces the pre-implementation plan: scope, design decisions, and which of them need developer approval vs. autonomous resolution.                                         |
| `implementation`  | Own                                                             | MIT     | Governs how code gets written against an approved plan: paradigm choice, over-engineering discipline, idiomaticity, verbosity, and the task completion checklist.           |
| `review`          | Own                                                             | MIT     | Runs standard, adversarial, over-engineering, and performance review passes; auto-invoked after `implementation`.                                                           |
| `commit`          | Own                                                             | MIT     | Governs commit message structure and file grouping; never runs without an explicit developer request.                                                                       |
| `pull-requests`   | Own                                                             | MIT     | Governs PR title/body conventions; never runs without an explicit developer request.                                                                                        |

See [`docs/rules-and-skills.md`](docs/rules-and-skills.md) for the skill
authoring format and how each client (Antigravity vs. Claude Code) deploys rules
and skills.

### MCP & LSP (Claude Code)

Claude Code-only, and set up by `scripts/sync.py`. On Antigravity the repo
manages only rules and skills (full plugin, no MCP/LSP); use Antigravity's
native Chrome DevTools instead of the MCP server.

- **MCP**: `chrome-devtools-mcp` (official `claude-plugins-official` plugin) —
  drive and inspect a live Chrome browser; requires Chrome 144+. Declared as a
  plugin `dependencies` entry, so it installs automatically with
  `agent-hardness`. See [`docs/mcp.md`](docs/mcp.md).
- **LSP**: language servers for Python, Markdown, Bash, TypeScript/JavaScript,
  HTML/CSS, and Rust, declared internally in `.lsp.json`. See
  [`docs/lsp.md`](docs/lsp.md) and the
  [Language Servers](#language-servers-claude-code) prerequisites above.
- **Hooks**: `PostToolUse` hooks format and lint-fix Python (Ruff) and
  Markdown (rumdl) on edit. See [`docs/hooks.md`](docs/hooks.md).

## Design Decisions

### Global vs Project-Level

All rules in this plugin are **generic** — they apply to any project, not just
repos created from a specific template. This avoids:

- Copying identical files into every repository.
- Per-repo maintenance when upstream rules update.
- Loading redundant skill content on every agent session.

Cross-cutting agent context (doc references, readiness triggers, behavioral
directives, and skill orchestration) is consolidated into a single globally
available `AGENTS.md` rule. Stage-specific procedures (planning, implementation,
review, commit, pull requests) live in their own skills so they load only when
relevant, instead of being always-on.

### `review` vs. a platform's own code-review command

Claude Code (and possibly other clients) may ship its own generic code-review
capability (e.g. a `/code-review` command with low/medium/high/max/ultra effort
levels, `--fix`, `--comment`). Its description overlaps with this plugin's own
`review` skill — both review "the current diff" — so an ambiguous, unnamed
request ("review this") could resolve to either. There's no structural
precedence between skills from different plugins/platforms; resolution is driven
by how each is named or described, not by a priority setting.

Two mitigations, at the two points this plugin controls:

- `AGENTS.md`'s automatic post-`implementation` trigger names the fully
  qualified `agent-hardness:review` — a direct reference, not a fuzzy match, so
  that call site is deterministic regardless of what else is installed.
- For any other request, name the skill explicitly at the console:
  `/agent-hardness:review` forces this plugin's methodology-specific pass
  (adversarial/over-engineering/performance passes against this repo's own
  rules); `/code-review` forces the platform's generic, effort-scaled one.
  Explicit naming always wins over an unnamed, ambiguous ask.
