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
| `planning`        | Own (from `AGENTS.md`, see [Rules](#rules-always-on) above)      | MIT     | Produces the pre-implementation plan: scope, design decisions, and which of them need developer approval vs. autonomous resolution.                                        |
| `implementation`  | Own (from `AGENTS.md`, see [Rules](#rules-always-on) above)      | MIT     | Governs how code gets written against an approved plan: paradigm choice, over-engineering discipline, idiomaticity, verbosity, and the task completion checklist.           |
| `review`          | Own (from `AGENTS.md`, see [Rules](#rules-always-on) above)      | MIT     | Runs standard, adversarial, over-engineering, and performance review passes; auto-invoked after `implementation`.                                                           |
| `commit`          | Own (from `AGENTS.md`, see [Rules](#rules-always-on) above)      | MIT     | Governs commit message structure and file grouping; never runs without an explicit developer request.                                                                      |
| `pull-requests`   | Own (from `AGENTS.md`, see [Rules](#rules-always-on) above)      | MIT     | Governs PR title/body conventions; never runs without an explicit developer request.                                                                                        |

## CLI Tools Required

Installation is left to the developer's own environment and package manager.

| Tool                                                | Purpose                                           | Install                                                                              |
| --------------------------------------------------- | ------------------------------------------------- | ------------------------------------------------------------------------------------ |
| [ast-grep](https://github.com/ast-grep/ast-grep)    | Structural code search via AST                    | [Installation guide](https://ast-grep.github.io/guide/quick-start.html#installation) |
| [RTK](https://github.com/rtk-ai/rtk)                | Terminal output compression (60-90% fewer tokens) | [Repository](https://github.com/rtk-ai/rtk)                                          |
| [gh](https://cli.github.com/)                       | GitHub integration and ADRs                       | [Installation guide](https://github.com/cli/cli#installation)                        |
| [gcloud](https://cloud.google.com/sdk/docs/install) | Google Cloud operations                           | [Installation guide](https://cloud.google.com/sdk/docs/install)                      |

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
- Python3: Ever use with UV.
```

## Installation

Install as an Antigravity plugin from a local path or repository URL:

```zsh
# From local path
agy plugin install /path/to/agent-hardness

# From GitHub
agy plugin install https://github.com/cosmoscalibur/agent-hardness
```

### Manual Sync (Zed / Claude Code)

For editors without Antigravity plugin support, `scripts/sync-configs.sh`
copies the same rule and skills into each editor's own config locations:

| Editor      | Rule (`rules/AGENTS.md` →) | Skills (`skills/` →) |
| ----------- | --------------------------- | --------------------- |
| Zed         | `~/.config/zed/AGENTS.md`   | `~/.agents/skills/`   |
| Claude Code | `~/.claude/CLAUDE.md`       | `~/.claude/skills/`   |

```zsh
./scripts/sync-configs.sh
```

It copies files (`cp`), so it does not remove skills already present in the
destination that no longer exist in this repo — re-run after every update to
this plugin to pick up changes.

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
