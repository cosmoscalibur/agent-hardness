# Agent Hardness Plugin

Antigravity plugin that packages agent readiness evaluation, a global
behavioral/tooling ruleset, and stage-specific coding methodology skills
(planning, implementation, review, commit, pull requests) into a single global
package.

## What's Included

### Rules (always-on)

A single `AGENTS.md` file holds the behavior that must apply regardless of which
skill is active: guard duty and scope control, documentation currency,
conversational register, CLI tooling preferences (see
[CLI Tools Required](#cli-tools-required) below), and the rules for when each
workflow skill gets invoked in an autonomous flow (e.g., running `review`
automatically once `implementation` completes). Detailed, stage-specific
procedures live in the `planning`, `implementation`, `review`, `commit`, and
`pull-requests` skills below instead of in this file.

`AGENTS.md` is a consolidated file rather than a set of separate per-topic rule
files, so origins are not tracked per rule — they are noted here as inspiration
instead:

- In-house practices, refined by systematically interrogating Claude about its
  training biases at each stage of the development flow and writing
  counterweight rules against them.
- [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills)
  — Karpathy-inspired execution discipline.
- [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) —
  YAGNI-driven decision ladder.
- [juliusbrussee/caveman](https://github.com/juliusbrussee/caveman) — concise,
  professional prose compression.

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

### MCP & LSP (Claude Code)

`scripts/sync.py` installs these official plugins from the
`claude-plugins-official` marketplace alongside this one; they are specific to
Claude Code. On Antigravity the repo manages only the core rules and skills —
MCP and LSP are not set up there. This flow is developed and tested against
Claude Code only.

| Plugin                | Kind | Source                    | Purpose                                                                                                          |
| --------------------- | ---- | ------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `chrome-devtools-mcp` | MCP  | `claude-plugins-official` | Drive and inspect a live Chrome browser (automation, performance traces, network/console); requires Chrome 144+. |
| `typescript-lsp`      | LSP  | `claude-plugins-official` | TypeScript / JavaScript language server.                                                                         |
| `pyright-lsp`         | LSP  | `claude-plugins-official` | Python language server (Pyright).                                                                                |
| `rust-analyzer-lsp`   | LSP  | `claude-plugins-official` | Rust language server (rust-analyzer).                                                                            |

## CLI Tools Required

Installation is left to the developer's own environment and package manager.

| Tool                                             | Purpose                                                                | Install                                                                              |
| ------------------------------------------------ | ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| [ast-grep](https://github.com/ast-grep/ast-grep) | Structural code search via AST                                         | [Installation guide](https://ast-grep.github.io/guide/quick-start.html#installation) |
| [RTK](https://github.com/rtk-ai/rtk)             | Terminal output compression (60-90% fewer tokens)                      | [Repository](https://github.com/rtk-ai/rtk)                                          |
| [gh](https://cli.github.com/)                    | GitHub integration and ADRs                                            | [Installation guide](https://github.com/cli/cli#installation)                        |
| [mergiraf](https://mergiraf.org/)                | Syntax-aware git merge driver — auto-resolves AST-equivalent conflicts | [Installation guide](https://mergiraf.org/installation.html)                         |
| [uv](https://github.com/astral-sh/uv)            | Run/manage Python3 (`scripts/sync.py`, any Python)                     | [Installation guide](https://docs.astral.sh/uv/getting-started/installation/)        |

## Global Setup

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
python3 scripts/sync.py
```

Copies `rules/AGENTS.md` to `~/.claude/CLAUDE.md` and installs the plugin's
skills plus the MCP/LSP plugins listed above. It is idempotent — re-run after
every update to this repo, then restart Claude Code to apply. See
[`docs/installation.md`](docs/installation.md) for what it does internally and
for the manual (script-free) install.

### Antigravity

Installs directly from the repo — no script needed, because `agy` auto-discovers
`rules/`, `skills/`, and `plugin.json` by convention:

```bash
# From local path
agy plugin install /path/to/agent-hardness

# From GitHub
agy plugin install https://github.com/cosmoscalibur/agent-hardness
```

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
