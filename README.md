# Agent Hardness Plugin

Antigravity plugin that packages agent readiness evaluation, a global
behavioral/tooling ruleset, and stage-specific coding methodology skills
(planning, implementation, review, commit, pull requests) into a single
global package.

## What's Included

### Rules (always-on)

A single `AGENTS.md` file holds the behavior that must apply regardless of
which skill is active: guard duty and scope control, documentation currency,
conversational register, CLI tooling preferences (see
[CLI Tools Required](#cli-tools-required) below), and the rules for when each
workflow skill gets invoked in an autonomous flow (e.g., running `review`
automatically once `implementation` completes). Detailed, stage-specific
procedures live in the `planning`, `implementation`, `review`, `commit`, and
`pull-requests` skills below instead of in this file.

`AGENTS.md` is a consolidated file rather than a set of separate per-topic
rule files, so origins are not tracked per rule — they are noted here as
inspiration instead:

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

| Skill             | Source                                                           | License | Description                                                                                                                                                                  |
| ------------------ | ----------------------------------------------------------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `agent-readiness` | [Factory AI](https://www.factory.ai/agent-readiness)             | MIT     | Scores a repository's readiness for autonomous AI agent development across 9 pillars with a phased plan; adapted from Factory AI's framework to modern tooling conventions. |
| `ast-grep`        | [ast-grep/agent-skill](https://github.com/ast-grep/agent-skill)  | MIT     | Guides structural, AST-based code search and rule authoring; used as-is, no adaptation.                                                                                      |
| `planning`        | Own                                                              | MIT     | Produces the pre-implementation plan: scope, design decisions, and which of them need developer approval vs. autonomous resolution.                                        |
| `implementation`  | Own                                                              | MIT     | Governs how code gets written against an approved plan: paradigm choice, over-engineering discipline, idiomaticity, verbosity, and the task completion checklist.           |
| `review`          | Own                                                              | MIT     | Runs standard, adversarial, over-engineering, and performance review passes; auto-invoked after `implementation`.                                                           |
| `commit`          | Own                                                              | MIT     | Governs commit message structure and file grouping; never runs without an explicit developer request.                                                                      |
| `pull-requests`   | Own                                                              | MIT     | Governs PR title/body conventions; never runs without an explicit developer request.                                                                                        |

## CLI Tools Required

Installation is left to the developer's own environment and package manager.

| Tool                                                | Purpose                                           | Install                                                                              |
| --------------------------------------------------- | ------------------------------------------------- | ------------------------------------------------------------------------------------ |
| [ast-grep](https://github.com/ast-grep/ast-grep)    | Structural code search via AST                    | [Installation guide](https://ast-grep.github.io/guide/quick-start.html#installation) |
| [RTK](https://github.com/rtk-ai/rtk)                | Terminal output compression (60-90% fewer tokens) | [Repository](https://github.com/rtk-ai/rtk)                                          |
| [gh](https://cli.github.com/)                       | GitHub integration and ADRs                       | [Installation guide](https://github.com/cli/cli#installation)                        |
| [gcloud](https://cloud.google.com/sdk/docs/install) | Google Cloud operations                           | [Installation guide](https://cloud.google.com/sdk/docs/install)                      |
| [uv](https://github.com/astral-sh/uv)               | Run/manage Python3 (`scripts/sync.py`, any Python) | [Installation guide](https://docs.astral.sh/uv/getting-started/installation/)        |

## RTK Global Setup

`rules/AGENTS.md` §4 says to route supported commands (`git`, `find`,
`grep`, `ls`, `read`, ...) through `rtk` — but that's a text rule the agent
has to remember on every single command. `rtk` also ships a hook that
intercepts those commands automatically at the client level, so enforcement
doesn't depend on the agent's per-command discipline. Install it once per
client, globally:

```zsh
# Claude Code (default agent)
rtk init -g

# Gemini CLI — also covers Antigravity 2, which shares Gemini's
# configuration format (don't use the separate `--agent antigravity` target)
rtk init -g --gemini
```

Check `rtk config` afterward to confirm the hook is installed (it warns
`No hook installed` otherwise). Later, `rtk session` shows adoption per
session and `rtk discover` lists specific commands still bypassing it.

## Global Rules Setup

This plugin handles methodology and behavioral guidelines. The user's
`~/.gemini/GEMINI.md` should contain only environment-specific configuration.

### Template for `~/.gemini/GEMINI.md`

Adjust to your environment and write to `~/.gemini/GEMINI.md`:

```markdown
# Global rules

## Context & Environment

- OS: [Your OS, e.g.: Manjaro].
- Shell: [Your shell syntax, e.g.: Use zsh syntax exclusively].
- Script preference: [Your preferences, e.g.: Python3 (with UV), ZSH].
```

## Installation

`scripts/sync.py` installs this plugin's rules, skills, and MCP servers (see
[MCP Servers](#mcp-servers) below) into a target IDE. It's a plain-stdlib
Python3 script — always invoke it through `uv`, never a bare `python3`:

```zsh
uv run scripts/sync.py <antigravity|claude>
```

| Target        | Rule (`rules/AGENTS.md` →) | Skills (`skills/` →)                                      | MCP                                                             |
| ------------- | --------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------------- |
| `antigravity` | auto-discovered by `agy`    | auto-discovered by `agy`                                    | none (Antigravity's own native Chrome DevTools covers it)        |
| `claude`      | `~/.claude/CLAUDE.md`       | via `claude plugin install agent-hardness@agent-hardness`   | via the official `chrome-devtools-mcp@claude-plugins-official` plugin |

- **`antigravity`**: shells out to `agy plugin install <repo-path>`, same as
  installing directly (below) — Antigravity reads `rules/`, `skills/`, and
  `plugin.json` by convention, so no copy step is needed.
- **`claude`**: copies `rules/AGENTS.md` to `~/.claude/CLAUDE.md`, adds this
  repo as a Claude plugin marketplace (or updates it, if already added) and
  installs its plugin (or updates it, if already installed — skills, see
  [Claude Plugin](#claude-plugin) below), then installs the official
  `chrome-devtools-mcp@claude-plugins-official` plugin. A directory-sourced
  marketplace doesn't auto-refresh and `install` is a no-op once already
  installed, so this always runs an explicit `marketplace update` +
  `plugin update` too — otherwise a local change (e.g. a version bump)
  never reaches the installed plugin. Restart Claude Code to apply an
  update.

Re-run after every update to this repo to pick up changes — `claude`
overwrites the previous sync rather than merging stale content.

Zed is not supported: this plugin targets Antigravity and Claude Code only.

### Direct Antigravity Install

Equivalent to `uv run scripts/sync.py antigravity`, without the script:

```zsh
# From local path
agy plugin install /path/to/agent-hardness

# From GitHub
agy plugin install https://github.com/cosmoscalibur/agent-hardness
```

### Claude Plugin

This repo, as committed, is directly installable as a Claude Code plugin
marketplace (`.claude-plugin/marketplace.json` + `.claude-plugin/plugin.json`)
without running the sync script:

```zsh
claude plugin marketplace add /path/to/agent-hardness
claude plugin install agent-hardness@agent-hardness
```

This installs `skills/` only — `rules/AGENTS.md` stays separate and is
synced to `~/.claude/CLAUDE.md` by `uv run scripts/sync.py claude` (or copy
it by hand).

## MCP Servers

This repo bundles no MCP config file — chrome-devtools is installed via
`scripts/sync.py claude` (Claude Code's official plugin) or is already
native (Antigravity). See [`docs/mcp-servers.md`](docs/mcp-servers.md) for
details.

## Design Decisions

### Global vs Project-Level

All rules in this plugin are **generic** — they apply to any project, not just
repos created from a specific template. This avoids:

- Copying identical files into every repository.
- Per-repo maintenance when upstream rules update.
- Loading redundant skill content on every agent session.

Cross-cutting agent context (doc references, readiness triggers, behavioral
directives, and skill orchestration) is consolidated into a single globally
available `AGENTS.md` rule. Stage-specific procedures (planning,
implementation, review, commit, pull requests) live in their own skills so
they load only when relevant, instead of being always-on.

### `review` vs. a platform's own code-review command

Claude Code (and possibly other clients) may ship its own generic
code-review capability (e.g. a `/code-review` command with
low/medium/high/max/ultra effort levels, `--fix`, `--comment`). Its
description overlaps with this plugin's own `review` skill — both review
"the current diff" — so an ambiguous, unnamed request ("review this") could
resolve to either. There's no structural precedence between skills from
different plugins/platforms; resolution is driven by how each is named or
described, not by a priority setting.

Two mitigations, at the two points this plugin controls:

- `AGENTS.md`'s automatic post-`implementation` trigger names the fully
  qualified `agent-hardness:review` — a direct reference, not a fuzzy
  match, so that call site is deterministic regardless of what else is
  installed.
- For any other request, name the skill explicitly at the console:
  `/agent-hardness:review` forces this plugin's methodology-specific pass
  (adversarial/over-engineering/performance passes against this repo's own
  rules); `/code-review` forces the platform's generic, effort-scaled one.
  Explicit naming always wins over an unnamed, ambiguous ask.
